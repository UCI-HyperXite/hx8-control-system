import time
from logging import getLogger

from signal_light import SignalLight

import limmy

log = getLogger(__name__)

serial_port_1 = "/dev/ttyACM0"
serial_port_2 = "/dev/ttyACM1"


class Motors:
    def __init__(self) -> None:
        self.motor_1 = limmy.VESC(serial_port=serial_port_1)
        self.motor_2 = limmy.VESC(serial_port=serial_port_2)

    def drive(self, speed: float) -> None:
        log.info(f"Driving motors at {speed} mph")
        self.motor_1.set_speed_mph(speed)
        self.motor_2.set_speed_mph(speed)

    def stop(self) -> None:
        log.info("Halting motors")
        self.motor_1.halt()
        self.motor_2.halt()

    def stop_heartbeat(self) -> None:
        log.info("stopping heartbeat")
        self.motor_1.stop_heartbeat()
        self.motor_2.stop_heartbeat()

    def __del__(self) -> None:
        self.stop()
        print("Motors: stopping heartbeat of both, do not kill program")
        self.motor_1.stop_heartbeat()
        self.motor_2.stop_heartbeat()
        # del self.motor_1
        # del self.motor_2


if __name__ == "__main__":
    light = SignalLight()

    SPEED = 2
    T_DRIVE = 2

    motors = Motors()

    while True:
        c = input("continue: ")
        if c == "stop":
            break

        speed = int(input("speed: "))
        run_time = int(input("time: "))

        light.enable()
        motors.drive(speed)
        print(f"told motors to drive at {speed} for {time} seconds")
        time.sleep(run_time)
        print("told motors to stop")
        motors.stop()
        light.disable()

    print("stopping heartbeat")
    motors.stop_heartbeat()
