import { CustomConsole } from 'customconsole';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { fstop, getBms, getOdometer, getPt300, getPt5000, getShuntcurr, getSpeed, getVminus, getVplus, load, start, stop } from "services/piserver";

import "./panel1.css";

function Panel1() {

    return (
        <div>
            <Container fluid>
                <Row>
                    <div className='row1'><b>HyperXite 8 Control
                        Panel</b></div>
                    <hr></hr>
                </Row>
                <Row>
                    <div className="prop"><h1 style={{ fontSize: '20px', textAlign: 'center' }}>Pneumatics</h1><table>
                        <tr>
                            <th style={{ fontSize: '25px' }}>PT 300</th>
                            <th style={{ fontSize: '25px' }}>PT 5000</th>
                        </tr>
                        <tr>
                            <td style={{ fontSize: '50px', color: 'white' }}>{getPt300()}</td>
                            <td style={{ fontSize: '50px', color: 'white' }}>{getPt5000()}</td>
                        </tr>
                    </table></div>
                    <div className="pnuem" > <table>
                        <tr>
                            <th style={{ fontSize: '30px' }}>Speed</th>
                            <th style={{ fontSize: '30px' }}>Odometer</th>
                        </tr>
                        <tr>
                            <td style={{ fontSize: '80px', color: 'white' }}>{getSpeed()}</td>
                            <td style={{ fontSize: '80px', color: 'white' }}>{getOdometer()}</td>
                        </tr></table></div>
                    <div className="console"><CustomConsole /></div>
                    <div className="consolebar">Error Console</div>

                </Row>
                <Row>

                    <Row>
                        <div className='sensors'> <table>
                            <tr>
                                <th style={{ fontSize: '20px' }}>BMS HSV</th>
                                <th style={{ fontSize: '20px' }}>VPlus</th>
                                <th style={{ fontSize: '20px' }}>VMinus</th>
                                <th style={{ fontSize: '20px' }}>Shunt Current</th>
                            </tr>
                            <tr>
                                <td style={{ fontSize: '50px', color: 'white' }}>{getBms()}</td>
                                <td style={{ fontSize: '50px', color: 'white' }}>{getVplus()}</td>
                                <td style={{ fontSize: '50px', color: 'white' }}>{getVminus()}</td>
                                <td style={{ fontSize: '50px', color: 'white' }}>{getShuntcurr()}</td>
                            </tr></table></div>
                    </Row>


                </Row>
                <Row>

                    <button className="buttonstart" onClick={start}>START</button>
                    <button className="buttonstop" onClick={stop}>STOP</button>
                    <button className="buttonforcequit" onClick={fstop}>FORCE STOP</button>
                    <button className="buttonload" onClick={load}>LOADING</button>
                </Row>
            </Container>
        </div>
    );

    // If you want to start measuring performance in your app, pass a function
    // to log results (for example: reportWebVitals(console.log))
    // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals

}
export default Panel1