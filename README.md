# Armband GPS Speedometer

A kid-wearable armband speedometer built from Adafruit modules:

- GPS speed from an Adafruit Mini GPS PA1010D.
- mph (2 decimals) on a 4-digit seven-segment FeatherWing.
- A single 10-pixel NeoPixel lane on the armband (scoped down from the original
  four-lane plan; the armband only has room for ~10 pixels at 60 LED/m).
- Electronics pod hardwired to the lane, charged in place via USB-C through the
  Feather RP2040 (no pod-to-armband connector).

This v1 intentionally avoids a custom PCB. It uses existing Adafruit boards and
a small soldered perma-proto wiring hub inside the pod. Do not use a solderless
breadboard in the wearable.

## Project Structure

- `CIRCUITPY/code.py` - firmware to copy onto the Feather's CIRCUITPY drive.
- `CIRCUITPY/bringup/` - staged test programs to copy as `code.py` during
  bench bring-up.
- `CIRCUITPY/lib/requirements.txt` - CircuitPython libraries to copy into
  `CIRCUITPY/lib/`.
- `docs/bom.md` - purchase list and missing-part traps.
- `docs/bench-bringup.md` - detailed first-power, header, display, GPS,
  battery, and LED bring-up instructions.
- `docs/wiring.md` - electrical wiring, LED lane, and charging switch.
- `docs/assembly-checklist.md` - build phases from bench to final armband.
- `docs/3d-printing-guide.md` - primary enclosure walkthrough for the
  3D-printed pod (OpenSCAD, slicing for Bambu/Prusa, PETG, print order).
- `cad/enclosure.scad` - parametric 3D-printable enclosure (compact, battery
  under the stack for low CoG; ~69 x 61 x 41 mm).
- `cad/verify_fit.py` - optional CAD sanity check that redraws the plan view.
- `docs/test-plan.md` - bench and field acceptance tests.

## Firmware Defaults

- Units: mph.
- Display: speed in mph, 2 decimals (auto-drops to 1 decimal at/above 100 mph to fit 4 digits).
- LED lanes: 1.
- Pixels per lane: 10.
- Total pixels: 10.
- LED pin: Feather `D6`.
- LED brightness cap: `0.12`.
- LED lane wiring: single straight lane, no serpentine. (The firmware keeps the
  lane/`LANE_REVERSED` scaffolding so a future multi-lane build only needs the
  constants in `code.py` changed.)

## Install

Start with `docs/bench-bringup.md`; it walks through Feather setup, header
soldering, display installation, GPS, battery charging, and LED tests in order.

Quick install summary:

1. Install CircuitPython for the Adafruit Feather RP2040.
2. Copy `CIRCUITPY/code.py` to the CIRCUITPY drive as `code.py`.
3. Copy the required libraries from the Adafruit CircuitPython Library Bundle
   into `CIRCUITPY/lib/`: `adafruit_gps`, `adafruit_ht16k33`, and `neopixel`.
   If using `circup`, run `circup install -r CIRCUITPY/lib/requirements.txt`
   from this project folder after the Feather is mounted.
4. Wire the hardware following `docs/wiring.md`.
5. Run the bench tests in `docs/test-plan.md` before enclosing anything.

The firmware is designed to be useful during bring-up: it shows `8888` and a
blue sweep on boot, `----` plus an amber wave while waiting for GPS, speed
(2-decimal mph) plus a fixed-rate rainbow comet once GPS data is available, a
yellow pulse plus `----` if a fix goes stale/lost, and `Err` plus red flashing
for caught application errors after hardware setup.
