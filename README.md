# Armband GPS Speedometer

A wearable speedometer built around a Feather RP2040, a PA1010D GPS receiver,
a four-digit display, and ten NeoPixels. The electronics sit in a printed pod
on a kid-sized wrist splint, with a rainbow comet running along the band.

![Completed armband speedometer](https://github.com/user-attachments/assets/bc3b3a26-924e-4150-a297-303ea21b6c35)

The firmware displays GPS ground speed in mph. LED patterns distinguish startup,
waiting for a fix, normal operation, a stale fix, and an application error.
The animation runs at a fixed rate; it does not encode speed. Two decimal places
are display resolution, not a claim of GPS accuracy.

## Build it

| Reference | Contents |
| --- | --- |
| [Parts](docs/bom.md) | Exact modules, mechanical constraints, and substitutions |
| [Wiring](docs/wiring.md) | Connections, I²C addresses, and the two-pole power switch |
| [Build and verification](docs/build.md) | Firmware installation, bench checks, and assembly order |
| [Enclosure](docs/3d-printing-guide.md) | CAD parameters, printable parts, orientation, and fit |

The build uses soldered perma-proto as a wiring hub; no custom PCB is needed.
The display plugs into stacking headers on the Feather. The GPS mounts on top
of the lid, and the LiPo sits below the board stack with insulation between it
and the solder joints. The current CAD shell is **75.8 × 61.8 × 41 mm**, excluding
the screw ears, baseplate, and external GPS.

A three-wire cable permanently joins the pod to the LED strip. The battery
charges through the Feather's USB-C port with the assembly still on the band.
A DPDT switch disables the Feather regulator and disconnects LED power while
leaving the charger connected.

## Firmware

[CIRCUITPY/code.py](CIRCUITPY/code.py) is the application; the
[build guide](docs/build.md#install-firmware) covers installing CircuitPython
and its libraries. Configuration constants are at the top of the file:

| Setting | Default |
| --- | --- |
| LED strip | 10 pixels, `D6`, brightness `0.12` |
| GPS output | RMC only, requested at 2 Hz |
| Display refresh | Every 0.35 s |
| Stale fix timeout | 3 s |
| Stationary-speed cutoff | Below 1.0 mph; two consecutive low samples before clearing a moving reading |

## What the measurements show

Reducing the GPS output to RMC sentences improved recovery of speed updates in
the polling tests: at a 1 Hz GPS setting, one 60-second run recovered 60 valid
RMC reports with RMC-only output, versus 31 with all sentences enabled. These
are results for the tested polling configuration, not an I²C bandwidth limit.

Stationary captures also contained nonzero speed readings, motivating the
software cutoff. They do not establish the GPS module's factory static-navigation
threshold or a fixed delay before its filter activates. Startup measurements
are timed from opening the host serial port; electrical power-on was not timestamped.

Runtime of at least 90 minutes is a build acceptance target; no measured battery
runtime is documented here. Final checks include readability while moving,
strain relief, and battery clearance, as well as the electronics.
