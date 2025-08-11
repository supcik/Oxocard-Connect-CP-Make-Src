# https://github.com/supcik/Oxocard-Connect-CP-Make-Src/blob/main/src/dimmer.py
# LED control with PWM

import board
import digitalio
import pwmio
from adafruit_debouncer import Button

LED_PIN = board.IO01
BUTTON_PIN = board.BTN5

# Duty cycles sequence for the LED
DUTY_CYCLES = [0xFFFF, 0xF000, 0x0000, 0xF000]


def main():
    index: int = 0
    # Configure the LED with PWM
    led = led = pwmio.PWMOut(
        LED_PIN, frequency=50000, duty_cycle=DUTY_CYCLES[index]
    )

    # Configure the button
    btn = digitalio.DigitalInOut(BUTTON_PIN)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = None  # The Oxocard already provides a pulldown
    switch = Button(btn, value_when_pressed=True)

    while True:
        switch.update()
        if switch.pressed:
            # configure the duty cycle of the PWM with the next value
            index = (index + 1) % len(DUTY_CYCLES)
            led.duty_cycle = DUTY_CYCLES[index]


main()
