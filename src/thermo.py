# https://github.com/supcik/Oxocard-Connect-CP-Make-Src/blob/main/src/thermo.py
# Get the temperature from a thermistor and send it to Adafruit IO

import math
import time
from os import getenv

import adafruit_connection_manager
import adafruit_requests
import board
import wifi
from adafruit_io.adafruit_io import IO_HTTP
from analogio import AnalogIn
from microcontroller import Pin

DELAY_S = const(5)


class Thermometer:

    RESISTOR_1 = 2200
    VCC = 3.3
    KELVIN_OFFSET = 273.15

    def __init__(self, pin: Pin, beta=4050.0, t0=298.15, r0=10000.0):
        self._beta = beta
        self._t0 = t0
        self._r0 = r0
        self._analog_in = AnalogIn(pin)

    def _voltage(self, samples) -> float:
        """
        Read the voltage from the analog pin `samples` times and return
        the average value.
        """
        sum = 0
        for _ in range(samples):
            sum += (self._analog_in.value * self.VCC) / 65536
        return sum / samples

    def temperature(self, samples=10) -> float:
        vr = self._voltage(samples)
        vntc = self.VCC - vr
        rntc = vntc * self.RESISTOR_1 / vr
        tk = 1.0 / (
            1.0 / self._t0
            + (1 / self._beta) * math.log(rntc / self._r0)
        )
        return tk - self.KELVIN_OFFSET


def main():
    # Initialize the thermometer
    thermo = Thermometer(board.IN06)
    # Set up Adafruit IO
    aio_username = getenv("AIO_USERNAME")
    aio_key = getenv("AIO_KEY")
    aio_feed_name = getenv("AIO_FEED_NAME")

    if not aio_feed_name:
        raise ValueError(
            "AIO_FEED_NAME environment variable is not set"
        )

    # Set up the Wi-Fi connection
    pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
    ssl_context = adafruit_connection_manager.get_radio_ssl_context(
        wifi.radio
    )
    requests = adafruit_requests.Session(pool, ssl_context)

    # Initialize Adafruit IO HTTP client
    io = IO_HTTP(aio_username, aio_key, requests=requests)

    while True:
        temp = thermo.temperature()
        print(f"Temperature : {temp:.1f} °C")
        # Send the temperature to Adafruit IO
        io.send_data(aio_feed_name, str(temp))
        time.sleep(DELAY_S)


main()
