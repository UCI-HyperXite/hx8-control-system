import { io } from "socket.io-client";
const SERVER_URL = "http://169.234.17.168:8000";
//const SERVER_URL = "http://localhost:8000";
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

export function load() {
    sio.emit("load",);
    console.log("Load sent");
}

export function stop() {
    sio.emit("stop", 4);
    console.log("Stop sent");
}

export function fstop() {
    sio.emit("stop", 4);
    console.log("Force Stop sent");
}

export function start() {
    sio.emit("start", 2);
    console.log("Start sent");
}

export default sio;
export { pt300, pt5000, odometer, speed, vminus, vplus, shuntcurr, bms };

