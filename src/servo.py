# https://github.com/supcik/Oxocard-Connect-CP-Make-Src/blob/main/src/servo.py
# Simple example using Serial Controlled Servo

import time

import board
from sc_servo import SerialControlledServo

SERVO_ID = const(1)
# Define the sequence of positions for the servo
POSITIONS = [0, 307, 614, 307]
SPEED = const(1000)
DELAY = 0.5  # Delay between movements in seconds
DELAY_WHILE_MOVING = 0.1  # Delay while the servo is moving in seconds


def main() -> None:
    # Replace boards.IO02 and board.IO01 with the appropriate pins for your board
    servo = SerialControlledServo(tx_pin=board.IO02, rx_pin=board.IO01)
    index: int = 0
    while True:
        servo.set_position(
            servo_id=SERVO_ID, pos=POSITIONS[index], speed=SPEED
        )
        while servo.is_moving(servo_id=SERVO_ID):
            time.sleep(DELAY_WHILE_MOVING)
        # Move to the next position in the sequence
        index = (index + 1) % len(POSITIONS)
        time.sleep(DELAY)  # Wait 1/2 second


main()
