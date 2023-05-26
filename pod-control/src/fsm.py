import asyncio
from enum import Enum
from typing import Callable, Coroutine, Mapping, Optional

from services.pod_socket_server import PodSocketServer

EventHandler = Callable[..., None | Coroutine[None, None, None]]


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
            }
        )

        self._state = State.INIT
        self._running_tick = 0
        self._state_transitions = {
            State.RUNNING: self._running_periodic,
        }

        # To avoid race conditions, socket handlers will defer state transitions
        self._interrupt_state: Optional[State] = None

    async def run(self) -> None:
        """Tick the state machine by loop."""
        while True:
            self.tick()
            await asyncio.sleep(0.001)

    def tick(self) -> None:
        """Tick the state machine by running the action for the current state."""
        self._pod_periodic()
        next_state = self._state
        if self._state in self._state_transitions:
            next_state = self._state_transitions[self._state]()
        # This should be the only place where a value is assigned to self._state
        self._state = self._interrupt_state or next_state
        self._interrupt_state = None

    def _pod_periodic(self) -> None:
        """Perform operations on every tick."""
        pass

    def _running_periodic(self) -> State:
        """Perform operations when the pod is running."""
        self._running_tick += 1
        return State.RUNNING

    async def handle_start(self, sid: str) -> None:
        """Start the FSM and the pod."""
        self._interrupt_state = State.RUNNING

    async def handle_stop(self, sid: str) -> None:
        """Stop the FSM and the pod."""
        self._interrupt_state = State.STOPPED
        # TODO: actually stop the pod

    def _register_handlers(self, handlers: Mapping[str, EventHandler]) -> None:
        """Register given handlers as socket event handlers."""
        for event, handler in handlers.items():
            setattr(self.socket, f"on_{event}", handler)