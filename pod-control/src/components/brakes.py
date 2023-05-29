from logging import getLogger
from typing import Final

try:
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi.RPi import GPIO as GPIO

log = getLogger(__name__)

PIN_PNEUMATICS_RELAY: Final[int] = 26


class Brakes:
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_PNEUMATICS_RELAY, GPIO.OUT)

    def engage(self) -> None:
        """Enable the brakes by closing the pneumatics."""
        log.info("Engaging brakes")
        GPIO.output(PIN_PNEUMATICS_RELAY, GPIO.LOW)

    def disable(self) -> None:
        """Disable the brakes by opening the pneumatics."""
        log.info("Disabling brakes")
        GPIO.output(PIN_PNEUMATICS_RELAY, GPIO.HIGH)

    def __del__(self) -> None:
        """Clean up the GPIO pin used for braking."""
        GPIO.cleanup(PIN_PNEUMATICS_RELAY)
