import { io } from "socket.io-client";

const SERVER_URL = "http://localhost:5000/pod";

const socket = io(SERVER_URL);

socket.on("connect", () => {
	console.log(socket.id);
});

socket.on("disconnect", () => {
	console.log(socket.id);
});

socket.on("pong", (data) => {
	console.log("server says", data);
});

export function sendPing() {
	socket.emit("ping", "ping");
}

export default socket;
