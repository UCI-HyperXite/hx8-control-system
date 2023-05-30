import logging

import socketio

from fsm import FSM
from services.pod_socket_server import PodSocketServer

logging.basicConfig(level=logging.INFO)


sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="http://localhost:3000"
)

pod_socket = PodSocketServer("/pod")
sio.register_namespace(pod_socket)


def on_startup() -> None:
    """Run the FSM when starting the socket app"""
    # This should be equivalent to asyncio.create_task(fsm.run())
    sio.start_background_task(fsm.run)


app = socketio.ASGIApp(sio, on_startup=on_startup)
fsm = FSM(pod_socket)
