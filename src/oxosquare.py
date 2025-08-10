# Fills the display with random squares and blends them with the OXOCARD logo colors.

import random

import board
import displayio
from adafruit_display_shapes.rect import Rect

splash = displayio.Group()
board.DISPLAY.auto_refresh = False
board.DISPLAY.root_group = splash

SQUARE_SIZE = const(20)
CONVERGENCE_STEPS = const(2000)
CONVERGENCE_OVERFLOW = 1.2

OXOCARD_LOGO = [
    [0x80197F, 0x000000, 0x7AB41D],
    [0x000000, 0xE2006A, 0x000000],
    [0xEA690B, 0x000000, 0x00A6E2],
]


def unpack_color(c):
    """
    Extract RGB components from a packed color integer.
    """
    r = (c >> 16) & 0xFF
    g = (c >> 8) & 0xFF
    b = (c >> 0) & 0xFF
    return (r, g, b)


def pack_color(r, g, b):
    """
    Pack RGB components into a single integer.
    """
    return (r << 16) + (g << 8) + b


def blend(c1, c2, f):
    """
    Blend two colors based on a factor f (0.0 to 1.0).
    Returns a new packed color of c1 * f + c2 * (1.0 - f).
    """
    r1, g1, b1 = unpack_color(c1)
    r2, g2, b2 = unpack_color(c2)
    r = int(r1 * f + r2 * (1.0 - f)) & 0xFF
    g = int(g1 * f + g2 * (1.0 - f)) & 0xFF
    b = int(b1 * f + b2 * (1.0 - f)) & 0xFF
    return pack_color(r, g, b)


def main():
    # Calculate the number of rows and columns based on the display size
    ROWS = board.DISPLAY.height // SQUARE_SIZE
    COLUMNS = board.DISPLAY.width // SQUARE_SIZE

    # Calculate logo square size based on the number of rows and columns
    LOGO_SQ_ROWS = ROWS // len(OXOCARD_LOGO)
    LOGO_SQ_COLS = COLUMNS // len(OXOCARD_LOGO[0])

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
    for random_row in range(ROWS):
        for random_column in range(COLUMNS):
            splash.append(grid[random_row][random_column])

    # Randomly fill squares with colors
    index = 0
    direction = 1
    while True:
        random_column = random.randrange(ROWS)
        random_row = random.randrange(COLUMNS)
        random_color = random.getrandbits(24)
        logo_color = OXOCARD_LOGO[random_row // LOGO_SQ_ROWS][
            random_column // LOGO_SQ_COLS
        ]
        color = blend(logo_color, random_color, min(index / CONVERGENCE_STEPS, 1.0))
        grid[random_row][random_column].fill = color
        board.DISPLAY.refresh()
        index += direction
        if index > CONVERGENCE_STEPS * CONVERGENCE_OVERFLOW:
            direction = -1
        if index == 0:
            direction = 1


main()
