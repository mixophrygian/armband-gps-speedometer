"""Stage 3 bring-up: seven-segment FeatherWing.

Copy this file to CIRCUITPY/code.py after installing the display and the
adafruit_ht16k33 library. You should see 8888, then a changing counter.
"""

import time

import adafruit_ht16k33.segments
import board
import busio


def make_i2c():
    try:
        return board.I2C()
    except AttributeError:
        return busio.I2C(board.SCL, board.SDA)


display = adafruit_ht16k33.segments.Seg7x4(make_i2c())
display.brightness = 0.8
display.fill(0)
display.print("8888")
display.show()
time.sleep(2)

count = 0
while True:
    display.fill(0)
    display.print(str(count % 10000))
    display.show()
    print("display count", count)
    count += 1
    time.sleep(0.5)
