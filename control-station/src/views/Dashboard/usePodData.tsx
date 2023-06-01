import { useEffect, useMemo, useState } from "react";
import PodSocketClient, { PodData } from "services/PodSocketClient";

function usePodData() {
	const [podData, setPodData] = useState<PodData>({
		tick: 0,
		wheel: 0,
		pressureDownstream: 0.0,
	});

	const podSocketClient = useMemo(() => new PodSocketClient(setPodData), []);

	useEffect(() => {
		podSocketClient.enable();
		// disable socket instance on cleanup
		return podSocketClient.disable.bind(podSocketClient);
	}, [podSocketClient]);

	return { podData, podSocketClient };
}

export default usePodData;
