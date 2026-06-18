"""Stage 4 bring-up: PA1010D GPS over STEMMA QT/I2C.

Copy this file to CIRCUITPY/code.py after installing the adafruit_gps library.
Take the GPS outdoors, ceramic antenna facing skyward. A first fix may take a
few minutes.
"""

import time

import adafruit_gps
import board
import busio


def make_i2c():
    try:
        return board.I2C()
    except AttributeError:
        return busio.I2C(board.SCL, board.SDA)


gps = adafruit_gps.GPS_GtopI2C(make_i2c(), debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

last_print = 0
while True:
    gps.update()
    now = time.monotonic()

    if now - last_print >= 1.0:
        last_print = now
        print("fix:", gps.has_fix, "satellites:", gps.satellites)
        if gps.has_fix:
            print(
                "lat/lon:",
                gps.latitude,
                gps.longitude,
                "speed_knots:",
                gps.speed_knots,
            )

    time.sleep(0.1)
