# Simple example using Serial Controlled Servo / J. Supcik, August 2025

import time

import board
from sc_servo import SerialControlledServo

POSITIONS = [0, 307, 614, 307]
SPEED = 1000


def main() -> None:
    # Replace boards.IO02 and board.IO01 with the appropriate pins for your board
    servo = SerialControlledServo(tx_pin=board.IO02, rx_pin=board.IO01)
    index: int = 0
    while True:
        servo.set_position(
            servo_id=1, pos=POSITIONS[index], speed=SPEED
        )
        index = (index + 1) % len(POSITIONS)
        while servo.is_moving(servo_id=1):
            time.sleep(0.1)
        time.sleep(0.5)  # Wait 1/2 second


main()
