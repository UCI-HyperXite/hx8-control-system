import usePodData from "./usePodData";

function Dashboard() {
	const { podData, podSocketClient } = usePodData();

	return (
		<div>
			<h1>Dashboard</h1>
			<button onClick={() => podSocketClient.sendPing()}>Send Ping</button>
			<div>
				{Object.entries(podData).map(([key, value]) => (
					<p key={key}>
						{key} - {value}
					</p>
				))}
			</div>
			<button onClick={() => podSocketClient.sendService()}>service</button>
			<button onClick={() => podSocketClient.sendStart()}>start</button>
			<button onClick={() => podSocketClient.sendStop()}>stop</button>
		</div>
	);
}

export default Dashboard;
