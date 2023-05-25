import time

import RPi.GPIO as GPIO

PIN_ENCODER_A = 14
PIN_ENCODER_B = 15


class WheelEncoder:
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_ENCODER_A, GPIO.IN)
        GPIO.setup(PIN_ENCODER_B, GPIO.IN)

        self.counter = 0
        self._last_time = time.time()
        self._last_A = self._read_A()
        self._last_B = self._read_B()
        print("Setup complete.")

    def measure(self) -> float:
        encoder_A = self._read_A()
        encoder_B = self._read_B()

        delta_d = 1 / 8

        calc = 0.0
        if encoder_A != self._last_A or encoder_B != self._last_B:
            current_time = time.time()

            if encoder_B != encoder_A:
                self.counter -= 1
            else:
                self.counter += 1
                print("counter: ", self.counter)
                delta_t = current_time - self._last_time
                calc = delta_d / delta_t
                print("Instantaneous Speed:", calc)
                self._last_time = current_time

        self._last_A = encoder_A
        self._last_B = encoder_B
        return calc

    def _read_A(self) -> bool:
        return GPIO.input(PIN_ENCODER_A)

    def _read_B(self) -> bool:
        return GPIO.input(PIN_ENCODER_B)

    def __del__(self) -> None:
        GPIO.cleanup()


def main() -> None:
    wheel_encoder = WheelEncoder()
    try:
        while True:
            wheel_encoder.measure()
    except KeyboardInterrupt:
        print("Program terminated.")


if __name__ == "__main__":
    main()
