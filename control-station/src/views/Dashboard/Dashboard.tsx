import { sendPing } from "services/socketHandler";

function Dashboard() {
	return (
		<div>
			<h1>Dashboard</h1>
			<button onClick={sendPing}>Send Ping</button>
		</div>
	);
}

export default Dashboard;
