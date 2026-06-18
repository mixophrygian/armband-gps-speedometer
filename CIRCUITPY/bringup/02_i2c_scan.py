"""Stage 2 bring-up: scan the I2C bus.

Copy this file to CIRCUITPY/code.py. Expected addresses:
* 0x70 when the 7-segment FeatherWing is installed
* 0x10 when the PA1010D GPS is connected over STEMMA QT

If no I2C boards are attached yet, the Feather may report that no pull-ups were
found. That is normal at the bare-Feather stage.
"""

import time

import board
import busio


def make_i2c():
    try:
        return board.I2C()
    except AttributeError:
        return busio.I2C(board.SCL, board.SDA)


while True:
    try:
        i2c = make_i2c()
    except RuntimeError as error:
        if "pull up" in str(error).lower():
            print("I2C bus not ready: no pull-ups found yet.")
            print("Attach the display FeatherWing or GPS, then reset the Feather.")
        else:
            print("I2C setup error:", error)
        time.sleep(2)
        continue

    try:
        while not i2c.try_lock():
            pass

        addresses = i2c.scan()
        i2c.unlock()

        if addresses:
            print("I2C devices:", [hex(address) for address in addresses])
        else:
            print("I2C devices: none found")
    except RuntimeError as error:
        print("I2C scan error:", error)
    finally:
        if hasattr(i2c, "deinit"):
            i2c.deinit()

    time.sleep(2)
