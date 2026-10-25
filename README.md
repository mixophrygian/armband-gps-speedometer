# Armband GPS Speedometer

A GPS speedometer strapped to a kid-sized wrist splint. A Feather RP2040 reads
a PA1010D GPS receiver and shows speed on a four-digit display, while ten
NeoPixels run a rainbow comet along the band. The Feather, display, and battery
sit in a printed pod.

![Completed armband speedometer](https://github.com/user-attachments/assets/bc3b3a26-924e-4150-a297-303ea21b6c35)

The display shows GPS ground speed in mph. The LEDs tell you when it's starting
up, waiting for a fix, running normally, losing reception, or hitting an error.
The comet always moves at the same rate. The display's two decimal places are
just formatting; they don't tell you how accurate the GPS is.

## Build it

- [Parts](docs/bom.md): the boards, battery, strip, and mounting hardware.
- [Wiring](docs/wiring.md): pin connections and the two-pole power switch.
- [Build guide](docs/build.md): assembly, firmware installation, and testing.
- [Enclosure](docs/3d-printing-guide.md): what to print and where the fit is tight.

A trimmed piece of perma-proto handles the wiring, so there's no custom PCB.
The display plugs into stacking headers on the Feather. The GPS sits on top of
the lid, and the LiPo goes underneath the boards, insulated from the solder
joints. The case body measures **75.8 × 61.8 × 41 mm**, excluding the screw ears,
baseplate, and GPS.

A three-wire cable permanently connects the pod to the LED strip. You can charge
through the Feather's USB-C port without taking anything off the band. The DPDT
switch turns off the Feather's regulator and cuts power to the LEDs, while
leaving the charger connected.

## Firmware

The main program is [CIRCUITPY/code.py](CIRCUITPY/code.py). Follow the
[build guide](docs/build.md#install-firmware) to install CircuitPython and the
libraries. The settings live at the top of the file:

| Setting | Default |
| --- | --- |
| LED strip | 10 pixels, `D6`, brightness `0.12` |
| GPS output | RMC only, requested at 2 Hz |
| Display refresh | Every 0.35 s |
| Stale fix timeout | 3 s |
| Stationary-speed cutoff | Below 1.0 mph; takes two low readings in a row to return to zero |

## What the measurements show

Asking the GPS for fewer sentence types helped the code keep up. In one
60-second test at 1 Hz, it read 60 valid RMC reports with RMC-only output,
compared with 31 when all sentences were enabled. That result applies to the
polling setup used in the test; it doesn't tell us the I²C bus's speed limit.

The GPS also reported some motion while sitting still, which is why the code
has a low-speed cutoff. The recordings don't tell us the module's default
static-navigation threshold or whether its filter starts after a fixed delay.
Startup times were measured from opening the computer's serial port; the moment
power was applied wasn't recorded.

The battery-life goal is at least 90 minutes, but there's no timed runtime result
yet. Try it on and check that you can read the display while moving. Make sure
the cables won't pull on solder joints and the battery has room without being
squeezed.
