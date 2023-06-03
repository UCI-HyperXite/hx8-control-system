import KeyboardStopHandler from "components/KeyboardStopHandler";
import usePodData from "./usePodData";

function Dashboard() {
	const { podData, podSocketClient } = usePodData();

	return (
		<div>
			<h1>Dashboard</h1>
			<button onClick={() => podSocketClient.sendPing()}>Send Ping</button>
			<div>
				<p>downstream pressure - {podData.pressureDownstream}</p>
				<p>wheel counter - {podData.wheelCounter}</p>
				<p>wheel speed - {podData.wheelSpeed.toFixed(2)}</p>
			</div>
			<KeyboardStopHandler podSocketClient={podSocketClient} />
			<button onClick={() => podSocketClient.sendService()}>service</button>
			<button onClick={() => podSocketClient.sendStart()}>start</button>
			<button onClick={() => podSocketClient.sendStop()}>stop</button>
		</div>
	);
}

export default Dashboard;
