import { io } from "socket.io-client";

//Last Rockets:
//const SERVER_URL = "http://192.168.0.11:8000";

//Last Wifi:
//const SERVER_URL = "http://169.234.33.130:8000";

//Local:
const SERVER_URL = "http://localhost:8000";

const sio = io(SERVER_URL);
let pt300 = 0.0;
let pt5000 = 0.0;
let speed = 0.0;
let odometer = 0.0;
let bms = 0.0;
let vplus = 0.0;
let vminus = 0.0;
let shuntcurr = 0.0;

sio.on('connect', () => {
    console.log('connected');
    sio.emit('sum', { numbers: [1, 2] });
});

sio.on('disconnect', () => {
    console.log('disconnected');
});
sio.on('sum_result', (data) => {
    console.log(data);
});
sio.on('velocity', (data) => {
    console.log(data);
    speed = data;
});

sio.on('starting pod', (data) => {
    console.log(data);
});

sio.on('stopping pod', (data) => {
    console.log(data);
});

sio.on('force stopping pod', (data) => {
    console.log(data);
});
sio.on('state1', (data) => {
    console.log(data);
});

sio.on('calc', (data) => {
    console.log(data);
    odometer = data;
});

sio.on('speed', (data) => {
    console.log("Speed: ", data);
});
sio.on('vplus', (data) => {
    console.log("Vplus: ", data);
    vplus = data;
});

sio.on('vminus', (data) => {
    console.log("Vminus: ", data);
    vminus = data;
});

sio.on('shunt', (data) => {
    console.log("Shunt: ", data);
    shuntcurr = data;
});

sio.on('bmsHigh', (data) => {
    console.log("BMS High: ", data);
    bms = data;
});

sio.on('pressure300', (data) => {
    console.log("pressure 300: ", data);
    pt300 = data;
});

sio.on('pressure5000', (data) => {
    console.log("pressure 5000: ", data);
    pt5000 = data;
});

sio.on('BMSCells', (data) => {
    console.log("BMS Cells: ", data);
});
sio.on('Distance', (data) => {
    console.log("BMS Cells: ", data);
});
sio.on('Motor data', (data) => {
    console.log("BMS Cells: ", data);
});

export function load() {
    sio.emit("load", 5);
    console.log("Load sent");
}

export function stop() {
    sio.emit("stop", 4);
    console.log("Stop sent");
}

export function fstop() {
    sio.emit("stop", 5);
    console.log("Force Stop sent");
}

export function start() {
    sio.emit("start", 2);
    console.log("Start sent");
}


export function getPt300() {
    return pt300;
}

export function getPt5000() {
    return pt5000;
}

export function getSpeed() {
    return speed;
}

export function getOdometer() {
    return odometer;
}

export function getBms() {
    return bms;
}

export function getVplus() {
    return vplus;
}

export function getVminus() {
    return vminus;
}

export function getShuntcurr() {
    return shuntcurr;
}
export default sio;
//export { pt300, pt5000, odometer, speed, vminus, vplus, shuntcurr, bms };

