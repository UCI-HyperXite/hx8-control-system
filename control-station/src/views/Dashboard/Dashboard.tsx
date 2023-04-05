import { sendPing } from "services/socketHandler";


function Dashboard() {
	return (
		<div>
			<button onClick={sendPing}>Send Ping</button>

		</div>
	);
}

export default Dashboard;
