import socketio


class PodSocket(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        print(sid, environ)
        pass

    def on_disconnect(self, sid):
        print(sid)
        pass

    async def on_ping(self, sid, data):
        print(sid)
        await self.emit("pong", "pong")
