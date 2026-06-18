"""Stage 1 bring-up: Feather alone.

Copy this file to CIRCUITPY/code.py. Open the serial console. You should see a
counter print once per second. If the board exposes board.LED, it will blink.
"""

import time

import board
import digitalio


led = None
led_pin = getattr(board, "LED", None)
if led_pin is not None:
    led = digitalio.DigitalInOut(led_pin)
    led.direction = digitalio.Direction.OUTPUT

count = 0
while True:
    print("Feather RP2040 alive:", count)
    if led is not None:
        led.value = not led.value
    count += 1
    time.sleep(1)
