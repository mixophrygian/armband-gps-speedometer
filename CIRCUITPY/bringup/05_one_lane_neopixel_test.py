"""Stage 7 bring-up: the single 10-pixel NeoPixel lane.

Copy this file to CIRCUITPY/code.py after wiring the LED lane to D6 with the
series resistor and shared ground. Keep brightness low during bench tests.
"""

import time

import board
import neopixel


PIXEL_COUNT = 10
BRIGHTNESS = 0.08
pixels = neopixel.NeoPixel(
    board.D6,
    PIXEL_COUNT,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB,
)

# Rainbow order: red, orange, yellow, green, blue, indigo, violet.
colors = (
    (255, 0, 0),
    (255, 60, 0),
    (255, 160, 0),
    (0, 255, 0),
    (0, 0, 255),
    (75, 0, 130),
    (180, 0, 160),
)

while True:
    for color in colors:
        for head in range(PIXEL_COUNT + 3):
            pixels.fill((0, 0, 0))
            for tail in range(4):
                pos = head - tail
                if 0 <= pos < PIXEL_COUNT:
                    scale = 1.0 - tail * 0.25
                    pixels[pos] = (
                        int(color[0] * scale),
                        int(color[1] * scale),
                        int(color[2] * scale),
                    )
            pixels.show()
            time.sleep(0.05)
