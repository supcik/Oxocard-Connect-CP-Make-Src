# https://github.com/supcik/Oxocard-Connect-CP-Make-Src/blob/main/src/load_cell.py
# Simple Scale project with a Scale class

import time
from struct import pack, unpack

import board
import digitalio
from adafruit_hx711.hx711 import HX711
from microcontroller import Pin

DATA_PIN: Pin = board.IO01
CLOCK_PIN: Pin = board.IO02


class Measure:

    def __init__(
        self,
        raw_value: int,
        tare: int = 0,
        calibration_factor: float = 1.0,
    ):
        self._raw_value = raw_value
        self._tare = tare
        self._calibration_factor = calibration_factor

    @property
    def raw_value(self):
        v = self._raw_value
        # Handle negative values
        return unpack("l", pack("L", v))[0]

    @property
    def value(self):
        return self.raw_value - self._tare

    @property
    def weight(self):
        return self.value * self._calibration_factor


class Scale:

    CHANNEL = HX711.CHAN_A_GAIN_128

    def __init__(self, data_pin: Pin, clock_pin: Pin, channel=CHANNEL):
        # Configure the pins for the HX711
        data = digitalio.DigitalInOut(data_pin)
        data.direction = digitalio.Direction.INPUT
        clock = digitalio.DigitalInOut(clock_pin)
        clock.direction = digitalio.Direction.OUTPUT

        self._channel = channel
        self._hx711 = HX711(data, clock)
        self._tare = 0
        self._calibration_factor = 1.0

    def read_blocking(self):
        """
        Read the HX711 blocking until a value is available.
        """
        return self._hx711.read_channel_blocking(self._channel)

    def measure(self):
        """
        Measure the weight and return a Measure object.
        """
        v = self.read_blocking()
        while v >= 0xFFFFFFFF:  # Read until a valid value is obtained
            v = self.read_blocking()
        return Measure(v, self._tare, self._calibration_factor)

    def tare(self, value=None):
        """
        Set the tare (zero) value for the scale.
        """
        if value is not None:
            self._tare = value
        else:
            self._tare = self.measure().value

    def calibrate(self, actual_weight: float, value=None):
        """
        Calibrate the scale with a known weight.
        """
        if value is None:
            value = self.measure().value
        self._calibration_factor = actual_weight / value


def main():
    scale = Scale(DATA_PIN, CLOCK_PIN)
    scale.tare()  # Set tare to current raw value
    # For example, with 1Kg, the value of the sensor on my scale is 418480
    scale.calibrate(1000, 418480)
    while True:
        m = scale.measure()
        print(
            f"raw: {m.raw_value}, value: {m.value}, Weight: {m.weight:.0f} g"
        )
        time.sleep(1)


main()
