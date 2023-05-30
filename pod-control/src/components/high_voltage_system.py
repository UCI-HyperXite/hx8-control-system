from typing import Final

try:
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi.RPi import GPIO as GPIO

PIN_CONTACTOR_RELAY: Final[int] = 20


class HighVoltageSystem:
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_CONTACTOR_RELAY, GPIO.OUT)

    def disable(self) -> None:
        """Disable the contactors by opening the relay."""
        GPIO.output(PIN_CONTACTOR_RELAY, GPIO.LOW)

    def enable(self) -> None:
        """Enable the contactors by closing the relay."""
        GPIO.output(PIN_CONTACTOR_RELAY, GPIO.HIGH)

    def __del__(self) -> None:
        """Clean up the GPIO pin used for the contactors."""
        GPIO.cleanup(PIN_CONTACTOR_RELAY)


if __name__ == "__main__":
    hvs = HighVoltageSystem()
    hvs.enable()
    input("press enter to disable")
    hvs.disable()
