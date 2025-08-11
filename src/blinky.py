# https://github.com/supcik/Oxocard-Connect-CP-Make-Src/blob/main/src/blinky.py
# Blinky with Oxocard Connect and CircuitPython

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
