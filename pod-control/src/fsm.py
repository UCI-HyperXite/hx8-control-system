import asyncio
from enum import Enum
from typing import Callable, Coroutine, Mapping

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

    async def run(self) -> None:
        """Tick the state machine by loop."""
        while True:
            self.tick()
            await asyncio.sleep(0.001)

    def tick(self) -> None:
        """Tick the state machine by running the action for the current state."""
        self._pod_periodic()
        if self._state in self._state_transitions:
            self._state_transitions[self._state]()

    def _pod_periodic(self) -> None:
        """Perform operations on every tick."""
        pass

    def _running_periodic(self) -> None:
        """Perform operations when the pod is running."""
        self._running_tick += 1

    async def handle_start(self, sid: str) -> None:
        """Start the FSM and the pod."""
        self._state = State.RUNNING

    async def handle_stop(self, sid: str) -> None:
        """Stop the FSM and the pod."""
        self._state = State.STOPPED
        # TODO: actually stop the pod

    def _register_handlers(self, handlers: Mapping[str, EventHandler]) -> None:
        """Register given handlers as socket event handlers."""
        for event, handler in handlers.items():
            setattr(self.socket, f"on_{event}", handler)
