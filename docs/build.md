# Build guide

The build uses a Feather RP2040, a stacked seven-segment FeatherWing, an
external PA1010D GPS, and one 10-pixel LED strip. Use the [BOM](bom.md) for parts,
the [wiring guide](wiring.md) for pin assignments and switch connections, and the
[enclosure guide](3d-printing-guide.md) for CAD and print settings.

## Assembly

Disconnect **both USB and LiPo** before soldering or changing connections. Check
battery polarity with a meter against the Feather's `+`/`-` markings before
first connection; a matching JST-PH housing does not guarantee matching polarity.

1. **Build the display stack.** Match the display's decimal points to the
   FeatherWing silkscreen. Fit male headers to the FeatherWing and stacking
   headers to the Feather, with sockets above and tails below. The display
   plugs into the sockets; check that neither row is offset by a pin.
2. **Dry-fit the enclosure.** Trim the half-size perma-proto to the dimensions
   in the enclosure guide. Check the complete stack, trimmed header tails,
   battery clearance, display orientation, and USB opening before committing
   its position. Additional sockets under the Feather increase stack height.
3. **Test before permanent wiring.** Connect the GPS by STEMMA QT and temporarily
   wire the LED strip and switch following the wiring guide. Install firmware
   and run the [bench checks](#bench-checks) below while everything is accessible.
4. **Attach the armband hardware.** Check the reading direction while worn,
   then attach the baseplate to the armband and the base to the baseplate.
   Bond the strip and add a sewn fabric retainer. Feed the three-conductor LED
   cable through the enclosure opening **before soldering it to the proto
   board**. The completed pod and strip are captive; separation requires
   desoldering.
5. **Wire the proto board.** Use 26 AWG stranded silicone wire and the
   [canonical connection table](wiring.md). Fit the data resistor and ground
   connections before soldering the Feather's tails into the board. Keep the
   data input at the strip's `DIN` end. A 100 µF, 6.3 V or higher capacitor at
   the LED input is recommended but optional; observe polarity. Identify the
   DPDT commons and throws with a meter, then verify both positions against the
   [switch table](wiring.md#dpdt-power-switch). Insulate the switch lugs and
   exposed LED joints.
6. **Check the completed wiring unpowered.** Confirm the data path measures
   approximately the series resistor value, all grounds connect, and neither
   battery nor switched LED power is shorted to ground. Verify the switch
   grounds `EN` and disconnects LED power in OFF. Re-run the bench checks after
   soldering.
7. **Secure the internals.** Isolate the LiPo from solder joints, header tails,
   and screws with felt or another protective layer. Support the stack so the
   display and USB port align without compressing the battery or forcing the
   lid closed. Clamp the cable at the enclosure exit and secure it at the strip
   so flex reaches wire, not solder pads. Leave enough service slack to lift
   the lid.
8. **Mount the GPS on the lid.** The current CAD has a cable opening, not an
   internal GPS retainer. With the electronics removed, drill mounting holes
   to match the board. Fit the battery and lid, then fasten the GPS at two
   diagonal corners with the ceramic antenna facing outward/skyward. Keep
   cable slack so removing one screw lets the GPS hinge aside for service.
   Keep screw tips clear of the battery and wiring.

USB-C remains accessible for charging in place. The current enclosure has
**no charge-LED window**; inspect the Feather's charge indicator with the pod
open during the charging check. Add a window or light pipe only if external
charge indication is needed.

## Install firmware

Install the [Feather RP2040 CircuitPython UF2](https://circuitpython.org/board/adafruit_feather_rp2040/)
if needed: hold BOOTSEL during reset or USB connection, then copy the UF2 to
`RPI-RP2`. The board restarts as `CIRCUITPY`.

With [circup installed](https://docs.circuitpython.org/projects/circup/en/latest/#installation)
and the board mounted, run from the repository root:

```sh
circup install -r CIRCUITPY/lib/requirements.txt
```

This installs the GPS, display, and NeoPixel libraries with their dependencies.
For each bench test, copy the linked script to the **mounted board** as
`code.py`. After testing, replace it with [CIRCUITPY/code.py](../CIRCUITPY/code.py).
The repository's `CIRCUITPY/` directory is the source, not the mounted drive.

The supplied firmware is configured for 10 pixels on `D6`, `BRIGHTNESS = 0.12`,
and the documented strip direction. Adjust the layout constants if the strip
differs. `DEBUG = True` enables once-per-second GPS status on the serial console;
leave it off for normal use.

## Bench checks

Connect each device with power disconnected. Test the display and GPS first,
then check battery operation, the LED strip, and both switch positions before
closing the enclosure.

| Hardware connected | Script copied as `code.py` | Expected result |
| --- | --- | --- |
| Feather only | [01_feather_serial.py](../CIRCUITPY/bringup/01_feather_serial.py) | `Feather RP2040 alive:` once per second; onboard LED blinks if available. |
| Display; then add GPS | [02_i2c_scan.py](../CIRCUITPY/bringup/02_i2c_scan.py) | Display at `0x70`; GPS at `0x10`. A bare Feather may report no I²C pull-ups. |
| Display | [03_display_test.py](../CIRCUITPY/bringup/03_display_test.py) | `8888`, then a counter. |
| GPS, antenna facing open sky | [04_gps_test.py](../CIRCUITPY/bringup/04_gps_test.py) | Fix and satellite count; latitude/longitude and speed in knots after a fix. |
| LED strip with battery power, shared ground, and data resistor | [05_one_lane_neopixel_test.py](../CIRCUITPY/bringup/05_one_lane_neopixel_test.py) | All 10 pixels show a low-brightness rainbow chase. |
| GPS, if further diagnosis is needed | [06_gps_diagnostic.py](../CIRCUITPY/bringup/06_gps_diagnostic.py) | `0x10 on bus: True` and raw NMEA confirm communication. The script's `sats in view` label reports the GGA satellite count used in the fix. |
| Complete assembly | [Main firmware](../CIRCUITPY/code.py) | Boot pattern, then the states below; numeric mph after an outdoor fix. |

With the display test running, confirm battery-only boot after removing USB.
Check charging with the battery connected and the switch OFF, then disconnect
USB and verify that OFF disables the display/GPS and cuts LED power. Stop using
a battery that heats abnormally, swells, or smells unusual.

## Status patterns

These describe the supplied firmware. The animation rate is fixed; it does not
represent speed.

| State | Display | LEDs | Check |
| --- | --- | --- | --- |
| Boot | `8888` | Blue sweep | Reset or power on. |
| No fix yet | `----` | Amber comets | Start without a usable sky view. |
| Fresh fix | mph, two decimals below 100 mph | Rainbow comets | Obtain an outdoor fix and walk. |
| Stale/lost fix | `----` | Yellow pulse | After a fix, obstruct reception and wait for fresh fixes to stop; the timeout is 3 seconds. |
| Caught runtime error | `Err` | Red flashing until reset | For a deliberate bench test, temporarily raise an exception inside `main()` after `boot_sweep()`, then restore the firmware. |

Errors during imports or hardware setup occur before the main error handler and
may only appear on the serial console. A failed display or strip can also prevent
the error indication from working.

The application suppresses speeds below 1 mph and requires two consecutive
below-threshold samples to drop a moving reading to zero. Display precision is
not a claim of GPS accuracy; see the [measurement summary](../README.md#what-the-measurements-show).

## Final checks

- [ ] USB boot, battery boot, switch OFF, and charging with the switch OFF work.
- [ ] All pixels animate without flicker or resets at the configured brightness.
- [ ] No-fix, normal, stale, and caught-error patterns are distinguishable.
- [ ] USB-C is reachable and the lid can open without pulling on solder joints.
- [ ] No exposed conductors or sharp edges touch skin, fabric, or the LiPo.
- [ ] Battery is retained without compression, bending, or contact with hardware.
- [ ] Pod stays in place, the cable is strain-relieved at both ends, and the strip
      does not bend sharply at its pads.
- [ ] Display is readable while worn; compare moving speed with a phone/watch as
      a plausibility check, not a calibration reference.
- [ ] Check comfort after 10 minutes and record runtime at the chosen brightness.
      **90 minutes is a design target, not a measured result.**

## Troubleshooting

| Symptom | Check |
| --- | --- |
| No `CIRCUITPY` drive | USB data cable, switch ON, and correct UF2. `RPI-RP2` is the bootloader drive. |
| Blank serial console | Use a console that asserts DTR. On macOS, `screen /dev/cu.usbmodem… 115200` worked in this build; substitute the actual port. Close other programs holding the port. Exit screen with `Ctrl-A`, `K`, `y`. |
| Import error | Re-run the circup install command; copying only the three top-level libraries omits dependencies. |
| No `0x70` | Power off; check header alignment, display orientation, and solder joints. |
| No `0x10` | Power off; reseat the STEMMA QT cable and check its routing. |
| GPS responds but has no fix | Take the antenna outdoors with an open sky view. A first fix can take minutes; an I²C response proves communication, not reception. |
| Display works but strip is dark | Battery/switch power path, shared ground, `DIN` direction, and the D6/resistor path. |
| Flicker or resets | Check battery voltage and connections under load, reduce brightness, and inspect the LED supply wiring. |
| No visible charge indication when closed | The current CAD has no charge-LED window; inspect with the pod open. |
