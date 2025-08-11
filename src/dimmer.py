# LED control with PWM / J. Supcik, August 2025


import board
import digitalio
import pwmio
from adafruit_debouncer import Button

LED_PIN = board.IO01
DUTY_CYCLES = [0xFFFF, 0xF000, 0x0000, 0xF000]
BUTTON_PIN = board.BTN5


def main():
    index: int = 0
    led = led = pwmio.PWMOut(
        LED_PIN, frequency=50000, duty_cycle=DUTY_CYCLES[index]
    )
    btn = digitalio.DigitalInOut(BUTTON_PIN)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = None  # The Oxocard already provides a pulldown
    switch = Button(btn, value_when_pressed=True)

    while True:
        switch.update()
        if switch.pressed:
            index = (index + 1) % len(DUTY_CYCLES)
            led.duty_cycle = DUTY_CYCLES[index]


main()
