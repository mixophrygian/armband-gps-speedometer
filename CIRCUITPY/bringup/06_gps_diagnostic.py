"""GPS diagnostic: prove the module is talking, then watch satellites climb.

Copy to CIRCUITPY/code.py and open the serial console. Take it outdoors with the
ceramic antenna (the square metal patch) facing straight up at open sky.

How to read the output:
- "0x10 on bus: True"            -> GPS is wired and responding on I2C.
- "0x10 on bus: False"          -> GPS not connected (check STEMMA QT / SDA-SCL).
- raw NMEA lines printing        -> the module IS sending data.
- "sats in view: N" climbing    -> antenna sees sky; a fix is coming.
- sats stuck at 0 for minutes    -> antenna blocked, indoors, or antenna fault.
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


i2c = make_i2c()

# 1) Is the GPS even on the bus?
while not i2c.try_lock():
    pass
found = i2c.scan()
i2c.unlock()
print("I2C devices:", [hex(a) for a in found])
print("0x10 on bus:", 0x10 in found, " (GPS)")
print("0x70 on bus:", 0x70 in found, " (display)")

gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)
# Output GGA (fix + sats) and RMC (speed), once per second.
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

last_print = 0
saw_any_sentence = False

while True:
    gps.update()
    now = time.monotonic()

    # nmea_sentence holds the most recent raw sentence the parser accepted.
    sentence = getattr(gps, "nmea_sentence", None)
    if sentence and not saw_any_sentence:
        saw_any_sentence = True
        print("FIRST RAW NMEA SEEN:", sentence)

    if now - last_print >= 1.0:
        last_print = now
        print(
            "talking:", saw_any_sentence,
            "| fix:", gps.has_fix,
            "| sats in view:", gps.satellites,
        )
        if sentence:
            print("   raw:", sentence)
        if gps.has_fix:
            print("   lat/lon:", gps.latitude, gps.longitude,
                  "| speed_knots:", gps.speed_knots)

    time.sleep(0.1)
