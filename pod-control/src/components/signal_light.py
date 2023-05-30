import time

import RPi.GPIO as GPIO

PIN_SIGNAL_LIGHT = 21


class SignalLight:
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_SIGNAL_LIGHT, GPIO.OUT)

    def disable(self) -> None:
        GPIO.output(PIN_SIGNAL_LIGHT, GPIO.LOW)

    def enable(self) -> None:
        GPIO.output(PIN_SIGNAL_LIGHT, GPIO.HIGH)

    def __del__(self) -> None:
        GPIO.cleanup(PIN_SIGNAL_LIGHT)


if __name__ == "__main__":
    light = SignalLight()
    light.enable()
    time.sleep(5)
    input("press enter to disable")
    light.disable()
