import asyncio
from typing import Callable, Coroutine, Mapping

from services.pod_socket_server import PodSocketServer

EventHandler = Callable[..., None | Coroutine[None, None, None]]


class FSM:
    def __init__(self, socket_server: PodSocketServer):
        """Store socket server instance."""
        self.socket = socket_server
        self._register_handlers(
            {
                "stop": self.handle_stop,
            }
        )

        self.running = True

    async def run_periodic(self) -> None:
        while self.running:
            print("tick")
            await asyncio.sleep(1)

    async def handle_stop(self, sid: str) -> None:
        """Stop the FSM and the pod."""
        self.running = False
        # TODO: actually stop the pod

    def _register_handlers(self, handlers: Mapping[str, EventHandler]) -> None:
        """Register given handlers as socket event handlers."""
        for event, handler in handlers.items():
            setattr(self.socket, f"on_{event}", handler)
