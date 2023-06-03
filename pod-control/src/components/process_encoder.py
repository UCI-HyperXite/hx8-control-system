import time
from logging import getLogger
from multiprocessing import Value
from multiprocessing.sharedctypes import Synchronized
from typing import Literal, cast

try:
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi.RPi import GPIO as GPIO

log = getLogger(__name__)

PIN_ENCODER_A = 14
PIN_ENCODER_B = 15


EncoderState = Literal[0, 1, 2, 3]
EncoderDiff = Literal[-1, 0, 1, 2]


def encode(a: bool, b: bool) -> EncoderState:
    """Produce a two-bit gray code."""
    return cast(EncoderState, (a << 1) + (a ^ b))


def difference(p: EncoderState, q: EncoderState) -> EncoderDiff:
    """Provide the difference in states in the range -1 to 2."""
    return cast(EncoderDiff, (p - q + 1) % 4 - 1)


class WheelEncoder:
    """
    Process based wheel encoder.
    Note: the type system for multiprocessing is currently incomplete.
    """

    def __init__(
        self,
        counter_value: Synchronized[int],
        speed_value: Synchronized[float],
        fault_value: Synchronized[bool],
    ) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup((PIN_ENCODER_A, PIN_ENCODER_B), GPIO.IN)

        self._start_time = time.time()

        self._counter = counter_value
        self._speed = speed_value
        self._fault = fault_value
        self.reset()
        log.info("Process encoder setup complete.")

    def reset(self) -> None:
        self._counter.value = 0
        self._last_time = time.time()
        self._last_state = self._read_state()

    def measure(self) -> None:
        current_time = time.time()
        state = self._read_state()

        delta_d = 1 / 16

        calc = 0.0
        inc = difference(state, self._last_state)

        if inc == 2:
            log.error("WHEEL ENCODER FAULT", state, self._last_state)
            self._fault.value = True

        if inc != 0:
            log.debug("counter: ", self._counter.value, current_time - self._start_time)
            delta_t = current_time - self._last_time
            calc = inc * delta_d / delta_t
            log.debug("Instantaneous Speed:", calc)
            self._last_time = current_time

            self._last_state = state
            self._speed.value = calc
            self._counter.value += inc

    def _read_state(self) -> EncoderState:
        return encode(GPIO.input(PIN_ENCODER_A), GPIO.input(PIN_ENCODER_B))

    def __del__(self) -> None:
        GPIO.cleanup((PIN_ENCODER_A, PIN_ENCODER_B))


def wheel_encoder_process(
    counter_value: Synchronized[int],
    speed_value: Synchronized[float],
    fault_value: Synchronized[bool],
) -> None:
    wheel_encoder = WheelEncoder(counter_value, speed_value, fault_value)
    while True:
        wheel_encoder.measure()
        time.sleep(0)


if __name__ == "__main__":
    from multiprocessing import Process

    counter_value = Value("i", 0)
    speed_value = Value("d", 0.0)
    fault_value = Value("b", False)
    p = Process(
        target=wheel_encoder_process, args=(counter_value, speed_value, fault_value)
    )
    p.start()
    p.join()
