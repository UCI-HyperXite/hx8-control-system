import { useEffect, useMemo, useState } from "react";
import PodSocketClient, { PodData } from "services/PodSocketClient";

function usePodData() {
	const [podData, setPodData] = useState<PodData>({ status: "" });
	const podSocketClient = useMemo(() => new PodSocketClient(setPodData), []);

	useEffect(() => {
		// disable socket instance on cleanup
		return () => {
			podSocketClient.off();
		};
	}, [podSocketClient]);

	return { podData, podSocketClient };
}

export default usePodData;
