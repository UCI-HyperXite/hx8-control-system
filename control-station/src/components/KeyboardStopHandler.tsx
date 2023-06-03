import { useEffect } from "react";
import PodSocketClient from "services/PodSocketClient";

interface KeyboardStopHandlerProps {
	podSocketClient: PodSocketClient;
}

function KeyboardStopHandler({ podSocketClient }: KeyboardStopHandlerProps) {
	useEffect(() => {
		const downHandler = (event: KeyboardEvent) => {
			if (event.code === "Space") {
				console.log("emit stop");
				podSocketClient.sendStop();
			}
		};
		window.addEventListener("keydown", downHandler);

		return () => {
			window.removeEventListener("keydown", downHandler);
		};
	}, [podSocketClient]);

	return <></>;
}

export default KeyboardStopHandler;
