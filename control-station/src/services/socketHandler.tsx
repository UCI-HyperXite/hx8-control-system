import { io } from "socket.io-client";

const SERVER_URL = "http://localhost:5000";

export const ioNamespace = (namespace: string) => {
	return io(`${SERVER_URL}/${namespace}`);
};
