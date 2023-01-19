import socketio

from services.pod_socket import PodSocket

sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="http://localhost:3000"
)

sio.register_namespace(PodSocket("/pod"))

app = socketio.ASGIApp(sio)
