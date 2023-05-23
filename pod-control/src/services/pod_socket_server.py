from logging import getLogger
from typing import Any, NoReturn

import socketio

log = getLogger(__name__)

Sid = str


class PodSocketServer(socketio.AsyncNamespace):
    def on_connect(self, sid: Sid, environ: dict[str, Any]) -> None:
        """When a client connects to the socket server."""
        log.info(sid, "connected", environ)

    def on_disconnect(self, sid: Sid) -> None:
        """When a client disconnects from the socket server."""
        log.info(sid, "disconnected")

    async def on_ping(self, sid: Sid, data: str) -> None:
        """Ping, pong!"""
        await self.emit_pong(sid, "pog")

    async def emit(self, *args: Any) -> NoReturn:
        """Do not use this generic emit."""
        raise TypeError("Should use named emit.")

    async def emit_pong(self, to: Sid, data: str) -> None:
        """Emit a pong message."""
        await socketio.AsyncNamespace.emit(self, "pong", data, to=to)
