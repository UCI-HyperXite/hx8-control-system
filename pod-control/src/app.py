import socketio

from fsm import FSM
from services.pod_socket_server import PodSocketServer

sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="http://localhost:3000"
)

pod_socket = PodSocketServer("/pod")
sio.register_namespace(pod_socket)

app = socketio.ASGIApp(sio)
fsm = FSM(pod_socket)
