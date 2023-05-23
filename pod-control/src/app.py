import socketio

from services.pod_socket_server import PodSocketServer

sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="http://localhost:3000"
)

sio.register_namespace(PodSocketServer("/pod"))

app = socketio.ASGIApp(sio)
