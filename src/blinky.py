# Blinky with Oxocard Connect and CircuitPython / J. Supcik, august 2025

import time

import board
import digitalio

HALF_PERIOD_S = 0.2  # Half period in seconds
LED_PIN = board.IO01


def main():
    led = digitalio.DigitalInOut(LED_PIN)
    led.switch_to_output(True)
    while True:
        led.value = not led.value  # Toggle the LED
        time.sleep(HALF_PERIOD_S)


main()  # Run the main function
