import { Dispatch, SetStateAction } from "react";
import { Socket } from "socket.io-client";
import { ioNamespace } from "./socketHandler";

interface ServerToClientEvents {
	connect: () => void;
	pong: (data: string) => void;
}

interface ClientToServerEvents {
	ping: (data: string) => void;
}

export interface PodData {
	status: string;
}

type SetPodData = Dispatch<SetStateAction<PodData>>;

class PodSocketClient {
	socket: Socket<ServerToClientEvents, ClientToServerEvents>;
	serverEvents: ServerToClientEvents;
	setPodData: SetPodData;

	constructor(setPodData: SetPodData) {
		this.socket = ioNamespace("pod");
		this.serverEvents = { connect: this.onConnect, pong: this.onPong };
		this.setPodData = setPodData;
	}

	enable(): void {
		this.socket.connect();
		console.debug("Enabling socket event handlers");
		Object.entries(this.serverEvents).forEach(([event, handler]) => {
			this.socket.on(event as keyof ServerToClientEvents, handler.bind(this));
		});
	}

	disable(): void {
		console.debug("Disabling socket event handlers");
		Object.keys(this.serverEvents).forEach((event) => {
			this.socket.off(event as keyof ServerToClientEvents);
		});
		this.socket.disconnect();
	}

	onConnect() {
		console.log("Connected to server as", this.socket.id);
	}

	onPong(data: string) {
		console.log("server says", data);
		this.setPodData({ status: data });
	}

	sendPing() {
		this.socket.emit("ping", "ping");
	}
}

export default PodSocketClient;
