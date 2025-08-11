# https://github.com/supcik/Oxocard-Connect-CP-Make-Src/blob/main/src/button.py
# LED control with button press using CircuitPython

import board
import digitalio
from adafruit_debouncer import Button

LED_PIN = board.IO01
BUTTON_PIN = board.BTN5  # The middle button


def main():
    led = digitalio.DigitalInOut(LED_PIN)
    led.switch_to_output(True)

    btn = digitalio.DigitalInOut(BUTTON_PIN)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = None  # The Oxocard already provides a pulldown
    switch = Button(btn, value_when_pressed=True)

    while True:
        switch.update()
        if switch.pressed:
            led.value = not led.value  # Toggle the LED


main()
