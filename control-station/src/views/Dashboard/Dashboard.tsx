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
		</div>
	);
}

export default Dashboard;
