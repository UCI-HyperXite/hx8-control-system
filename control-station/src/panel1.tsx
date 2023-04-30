import Propulsion from 'propulsion';
import { Link, Route, Routes, useNavigate } from 'react-router-dom';
import { Dashboard } from "views";
import "./panel1.css";

function Panel1() {
    const navigate = useNavigate();
    const routeChange1 = () => {
        const path = `.propulsion`;
        navigate(path);
    }
    return (
        <div>
            <div className="row1">
                <b>HyperXite 8 Control
                    Panel</b>
                <hr></hr>
            </div>
            <div className="row2">
                <div className="camera"><Dashboard /> </div>
                <div className="camerabar">RASPBERRY PI CAMERA</div>
                <div className="console"></div>
                <div className="consolebar">ERROR CONSOLE</div>
            </div>
            <div className="row3">
                <div className="sensors"></div>
                <span className="ptname">PT:</span>
                <span className="eprname">EPR:</span><span className="sensorname"> Sensor Data:</span><span className="bmsname">BMS Fault
                    Value:</span>
                <button className="pnbutton" onClick={routeChange1}>Pneumatics</button>
                <Link to="/propulsion"><button className="props" >Propulsion</button> </Link>
                <Routes>
                    <Route path="propulsion" element={<Propulsion />} />
                </Routes>

            </div>
            <div className="row4">
                <span className="distancename">Distance Traveled: </span>
                <span className="invertername">Inverter Frequency:</span>
                <button className="buttonstart">START</button>
                <button className="buttonstop">STOP</button>
                <button className="buttonforcequit">FORCE STOP</button>
            </div>
            <div className="row5">
            </div>
        </div>
    );

    // If you want to start measuring performance in your app, pass a function
    // to log results (for example: reportWebVitals(console.log))
    // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals

}
export default Panel1