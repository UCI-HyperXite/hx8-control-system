import time

import board
from adafruit_ina219 import INA219, ADCResolution, BusVoltageRange, Gain

REF_CURRENT_LOW = 4
REF_CURRENT_HIGH = 20
REF_PRESSURE_LOW = 0
REF_PRESSURE_HIGH = 300

REF_CURRENT_SPAN = REF_CURRENT_HIGH - REF_CURRENT_LOW
REF_PRESSURE_SPAN = REF_PRESSURE_HIGH - REF_PRESSURE_LOW


class PressureTransducer:
    """Based off of sample code for adafruit_ina219"""

    def __init__(self, address: int) -> None:
        i2c_bus = board.I2C()  # uses board.SCL and board.SDA

        self.ina219 = INA219(i2c_bus, address)
        self.ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_128S
        self.ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_128S
        self.ina219.bus_voltage_range = BusVoltageRange.RANGE_16V
        self.ina219.gain = Gain.DIV_1_40MV

    # measure and display loop
    def read_current(self) -> float:
        current: float = self.ina219.current
        if self.ina219.overflow:
            raise ValueError("Internal Math Overflow Detected!")
        return current

    def measure_pressure(self) -> float:
        current = self.read_current()

        return (
            REF_PRESSURE_LOW
            + REF_PRESSURE_SPAN * (current - REF_CURRENT_LOW) / REF_CURRENT_SPAN
        )


if __name__ == "__main__":
    pt = PressureTransducer(0x40)
    while True:
        print(pt.read_current())
        time.sleep(2)
