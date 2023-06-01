import { Dispatch, SetStateAction } from "react";
import { Socket } from "socket.io-client";
import { ioNamespace } from "./socketHandler";

interface ServerToClientEvents {
	connect: () => void;
	pong: (data: string) => void;
	stats: (data: Partial<PodData>) => void;
}

interface ClientToServerEvents {
	ping: (data: string) => void;
	service: () => void;
	start: () => void;
	stop: () => void;
}

export interface PodData {
	tick: number;
	wheel: number;
	pressureDownstream: number;
}

type SetPodData = Dispatch<SetStateAction<PodData>>;

class PodSocketClient {
	socket: Socket<ServerToClientEvents, ClientToServerEvents>;
	serverEvents: ServerToClientEvents;
	setPodData: SetPodData;

	constructor(setPodData: SetPodData) {
		this.socket = ioNamespace("pod");
		this.serverEvents = {
			connect: this.onConnect,
			pong: this.onPong,
			stats: this.onStats,
		};
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

	onDisconnect() {
		console.log("Disconnected from server.");
	}

	onPong(data: string) {
		console.log("server says", data);
		// this.setPodData({ status: data });
	}

	onStats(data: Partial<PodData>) {
		this.setPodData((d) => ({ ...d, ...data }));
	}

	sendPing() {
		this.socket.emit("ping", "ping");
	}

	sendService() {
		this.socket.emit("service");
	}

	sendStart() {
		this.socket.emit("start");
	}

	sendStop() {
		this.socket.emit("stop");
	}
}

export default PodSocketClient;
