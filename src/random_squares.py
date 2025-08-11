# Fills the display with random squares. Blends them with OxoCard logo colors.
# J. Supcik, August 2025

import random

import board
import displayio
from adafruit_display_shapes.rect import Rect

splash = displayio.Group()
board.DISPLAY.auto_refresh = False
board.DISPLAY.root_group = splash

SQUARE_SIZE = const(40)


def main():
    ROWS = board.DISPLAY.height // SQUARE_SIZE
    COLUMNS = board.DISPLAY.width // SQUARE_SIZE

    # Build a grid of squares
    grid = [
        [
            Rect(
                1 + r * SQUARE_SIZE,
                1 + c * SQUARE_SIZE,
                SQUARE_SIZE - 2,
                SQUARE_SIZE - 2,
                fill=0x00,
            )
            for c in range(COLUMNS)
        ]
        for r in range(ROWS)
    ]

    # Add the squares to the display
    for r in range(ROWS):
        for c in range(COLUMNS):
            splash.append(grid[r][c])

    # Randomly fill squares with colors
    while True:
        c = random.randrange(ROWS)
        r = random.randrange(COLUMNS)
        fill = random.getrandbits(24)
        grid[r][c].fill = fill
        board.DISPLAY.refresh()


main()
