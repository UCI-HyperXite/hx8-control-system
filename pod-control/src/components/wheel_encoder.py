import time
from logging import getLogger
from typing import Literal

import RPi.GPIO as GPIO

log = getLogger(__name__)

PIN_ENCODER_A = 14
PIN_ENCODER_B = 15


EncoderState = Literal[0, 1, 2, 3]
EncoderDiff = Literal[-1, 0, 1, 2]


def encode_state(a: bool, b: bool) -> EncoderState:
    """Produce a two-bit gray code."""
    return (a << 1) + (a ^ b)


def state_difference(p: EncoderState, q: EncoderState) -> EncoderDiff:
    """Provide the difference in states in the range -1 to 2."""
    return (p - q + 1) % 4 - 1


class WheelEncoder:
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup((PIN_ENCODER_A, PIN_ENCODER_B), GPIO.IN)

        self.counter = 0
        self._last_time = time.time()
        self._last_state = self._read_state()
        log.debug("Setup complete.")

    def measure(self) -> float:
        current_time = time.time()
        state = self._read_state()

        delta_d = 1 / 16

        speed = 0.0
        inc = state_difference(state, self._last_state)

        if inc == 2:
            log.error(f"Encoder skipped from {state} to {self._last_state}")
            raise ValueError("Illegal encoder transition.")

        if inc != 0:
            log.info(f"counter: {self.counter}")
            delta_t = current_time - self._last_time
            speed = inc * delta_d / delta_t
            log.info(f"Instantaneous Speed: {speed}")
            self._last_time = current_time

        self._last_state = state
        self.counter += inc

        return speed

    def _read_state(self) -> int:
        return encode_state(GPIO.input(PIN_ENCODER_A), GPIO.input(PIN_ENCODER_B))

    def __del__(self) -> None:
        GPIO.cleanup((PIN_ENCODER_A, PIN_ENCODER_B))


def main() -> None:
    wheel_encoder = WheelEncoder()
    try:
        while True:
            wheel_encoder.measure()
            time.sleep(0.001)
    except KeyboardInterrupt:
        print("Program terminated.")


if __name__ == "__main__":
    main()
