import asyncio
from enum import Enum
from logging import getLogger
from math import pi
from multiprocessing import Process, Value
from typing import Callable, Coroutine, Mapping, Optional, Union

from components.brakes import Brakes
# from components.high_voltage_system import HighVoltageSystem
from components.motors import Motors
from components.pressure_transducer import PressureTransducer
from components.process_encoder import wheel_encoder_process
from components.signal_light import SignalLight

from services.pod_socket_server import PodSocketServer

log = getLogger(__name__)

# EventHandler = Callable[..., None | Coroutine[None, None, None]]
EventHandler = Callable[..., Union[None, Coroutine[None, None, None]]]

TRACK_FEET = 70
INCH_PER_FEET = 12
WHEEL_DIAMETER = 3  # in
WE_RESOLUTION = 16
STOP_THRESHOLD = TRACK_FEET * INCH_PER_FEET / (WHEEL_DIAMETER * pi) * WE_RESOLUTION

ADDRESS_PT_DOWNSTREAM = 0x40


class State(Enum):
    INIT = 0
    SERVICE = 1
    RUNNING = 2
    STOPPED = 3


class FSM:
    def __init__(self, socket_server: PodSocketServer):
        """Store socket server instance."""
        self.socket = socket_server
        self._register_handlers(
            {
                "start": self.handle_start,
                "stop": self.handle_stop,
                "service": self.handle_service,
            }
        )

        self._state: State = State.INIT
        self._last_state = self._state
        self._running_tick = 0
        # State transitions are run whenever the pod is in the given state
        # These transitions should return the next state
        self._state_transitions = {
            State.RUNNING: self._running_periodic,
        }

        # Enter actions are run once when transitioning to a state from a different one
        self._enter_actions = {
            State.INIT: self._enter_init,
            State.SERVICE: self._enter_service,
            State.RUNNING: self._enter_running,
            State.STOPPED: self._enter_stopped,
        }

        # To avoid race conditions, socket handlers will defer state transitions
        self._interrupt_state: Optional[State] = None

        # components
        # self._hvs = HighVoltageSystem()
        # self._hvs.enable()

        self._brakes = Brakes()
        self._brakes.engage()
        self._wheel_encoder_counter = Value("i", 0)
        self._wheel_encoder_speed = Value("d", 0.0)
        self._wheel_encoder_fault = Value("b", 0)
        self._pt_downstream = PressureTransducer(ADDRESS_PT_DOWNSTREAM)
        self._motors = Motors()
        self._signal_light = SignalLight()

    async def run(self) -> None:
        """Tick the state machine by loop."""
        p = Process(
            target=wheel_encoder_process,
            args=(
                self._wheel_encoder_counter,
                self._wheel_encoder_speed,
                self._wheel_encoder_fault,
            ),
        )
        p.start()

        try:
            while True:
                self.tick()
                await asyncio.sleep(0.001)
        finally:
            p.join()

    def tick(self) -> None:
        """Tick the state machine by running the action for the current state."""
        # If entering a new state, run the enter action
        if self._state != self._last_state and self._state in self._enter_actions:
            self._enter_actions[self._state]()

        self._pod_periodic()
        next_state = self._state
        if self._state in self._state_transitions:
            next_state = self._state_transitions[self._state]()

        self._last_state = self._state
        # This should be the only place where a value is assigned to self._state
        self._state = self._interrupt_state or next_state
        self._interrupt_state = None

    def _pod_periodic(self) -> None:
        """Perform operations on every tick."""
        asyncio.create_task(
            self.socket.emit_stats(
                {
                    "tick": self._running_tick,
                    "pressureDownstream": round(
                        self._pt_downstream.measure_pressure(), 2
                    ),
                }
            )
        )

    def _enter_service(self) -> None:
        """Perform operations once when entering the service state."""
        log.info("Entering service, disabling brakes")
        self._brakes.disable()

    def _enter_running(self) -> None:
        """Perform operations once when starting to run the pod."""
        self._signal_light.enable()
        log.info("Entering running")
        self._brakes.disable()

    def _running_periodic(self) -> State:
        """Perform operations when the pod is running."""
        self._running_tick += 1

        if self._wheel_encoder_fault.value:
            log.error("Wheel encoder faulted")
            return State.STOPPED

        self._motors.drive(20)

        asyncio.create_task(
            self.socket.emit_stats(
                {
                    "wheelCounter": self._wheel_encoder_counter.value,
                    "wheelSpeed": self._wheel_encoder_speed.value,
                }
            )
        )
        log.info(f"wheel encoder speed: {self._wheel_encoder_speed.value}")

        if self._wheel_encoder_counter.value > STOP_THRESHOLD:
            return State.STOPPED

        return State.RUNNING

    def _enter_init(self) -> None:
        self._signal_light.disable()

    def _enter_stopped(self) -> None:
        """Perform operations once when stopping the pod."""
        self._brakes.engage()
        self._motors.stop()
        log.info("Entering stopped")
        self._signal_light.disable()

    async def handle_start(self, sid: str) -> None:
        """Start the FSM and the pod."""
        self._interrupt_state = State.RUNNING
        log.info(f"{sid} sent start")

    async def handle_service(self, sid: str) -> None:
        """Start the FSM and the pod."""
        self._interrupt_state = State.SERVICE

    async def handle_stop(self, sid: str) -> None:
        """Stop the FSM and the pod."""
        self._interrupt_state = State.STOPPED
        log.info(f"{sid} sent stop")
        # TODO: actually stop the pod

    def _register_handlers(self, handlers: Mapping[str, EventHandler]) -> None:
        """Register given handlers as socket event handlers."""
        for event, handler in handlers.items():
            setattr(self.socket, f"on_{event}", handler)

    def stop_heartbeat(self) -> None:
        self._motors.stop_heartbeat()
