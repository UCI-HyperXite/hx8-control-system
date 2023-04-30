import { start } from "services/piserver";



function Dashboard() {
	return (
		<div>
			<button onClick={start}>Start</button>
		</div>
	);
}

export default Dashboard;
