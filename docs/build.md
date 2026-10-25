# Build guide

The hardware is a Feather RP2040 with a seven-segment FeatherWing stacked on top,
a PA1010D GPS mounted outside the case, and a 10-pixel LED strip. The
[BOM](bom.md) covers parts, the [wiring guide](wiring.md) covers connections, and
the [enclosure guide](3d-printing-guide.md) covers CAD and print settings.

## Assembly

Disconnect **both USB and LiPo** before soldering or changing connections. Check
battery polarity with a meter against the Feather's `+`/`-` markings before
plugging it in for the first time. A JST-PH plug can fit and still have its wires
reversed.

1. **Build the display stack.** Match the display's decimal points to the
   FeatherWing silkscreen. Fit male headers to the FeatherWing and stacking
   headers to the Feather, with sockets above and tails below. The display
   plugs into the sockets; check that neither row is offset by a pin.
2. **Dry-fit the enclosure.** Trim the half-size perma-proto to the dimensions
   in the enclosure guide. Check the complete stack, trimmed header tails,
   battery clearance, display orientation, and USB opening before fixing
   anything in place. Extra sockets under the Feather make the stack taller.
3. **Test before permanent wiring.** Connect the GPS by STEMMA QT and temporarily
   wire the LED strip and switch following the wiring guide. Install firmware
   and run the [bench checks](#bench-checks) below while everything is accessible.
4. **Attach the armband hardware.** Check the reading direction while worn,
   then attach the baseplate to the armband and the base to the baseplate.
   Bond the strip and add a sewn fabric retainer. Feed the three-conductor LED
   cable through the enclosure opening **before soldering it to the proto
   board**. Once soldered, the pod and strip stay connected; you'll need to
   desolder the cable to separate them.
5. **Wire the proto board.** Use 26 AWG stranded silicone wire and the
   [connection table](wiring.md). Fit the data resistor and ground
   connections before soldering the Feather's tails into the board. Keep the
   data input at the strip's `DIN` end. A 100 µF, 6.3 V or higher capacitor at
   the LED input is recommended but optional; check its polarity. Find the
   DPDT commons and throws with a meter, then check both positions against the
   [switch table](wiring.md#dpdt-power-switch). Insulate the switch lugs and
   exposed LED joints.
6. **Check the wiring with power disconnected.** The data path should measure
   roughly the series resistor value. Check that all grounds connect and neither
   battery nor switched LED power is shorted to ground. Verify the switch
   grounds `EN` and disconnects LED power in OFF. Re-run the bench checks after
   soldering.
7. **Secure the internals.** Protect the LiPo from solder joints, header tails,
   and screws with felt or another protective layer. Support the stack so the
   display and USB port align without compressing the battery or forcing the
   lid closed. Clamp the cable at the enclosure exit and secure it at the strip
   so the wire takes the flex instead of the solder pads. Leave enough slack to
   lift the lid.
8. **Mount the GPS on the lid.** The case has a cable opening for the GPS but
   no internal mount. With the electronics removed, drill mounting holes
   to match the board. Fit the battery and lid, then fasten the GPS at two
   diagonal corners with the ceramic antenna facing outward/skyward. Keep
   enough cable slack to swing the GPS aside after removing one screw.
   Keep screw tips clear of the battery and wiring.

You can charge through USB-C with the case closed, but there's **no charge-LED
window**. Open the pod to check the Feather's charge indicator. If you want to
see it from outside, add a window or light pipe.

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

The firmware expects 10 pixels on `D6`, with `BRIGHTNESS = 0.12`. Adjust the
layout constants if your strip has a different length or orientation. Set
`DEBUG = True` to print GPS status once per second on the serial console; leave
it off for normal use.

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

With the display test loaded, remove USB and switch the board off and on to
check that it boots on battery alone.
Check charging with the battery connected and the switch OFF, then disconnect
USB and verify that OFF disables the display/GPS and cuts LED power. Stop using
a battery that heats abnormally, swells, or smells unusual.

## Status patterns

These are the firmware's display and LED patterns. The animation runs at a fixed
rate; it doesn't change with speed.

| State | Display | LEDs | Check |
| --- | --- | --- | --- |
| Boot | `8888` | Blue sweep | Reset or power on. |
| No fix yet | `----` | Amber comets | Start without a usable sky view. |
| Fresh fix | mph, two decimals below 100 mph | Rainbow comets | Get an outdoor fix and walk. |
| Stale/lost fix | `----` | Yellow pulse | After getting a fix, block reception and wait for updates to stop; the timeout is 3 seconds. |
| Caught runtime error | `Err` | Red flashing until reset | For a deliberate bench test, temporarily raise an exception inside `main()` after `boot_sweep()`, then restore the firmware. |

Errors during imports or hardware setup happen before the main error handler
starts, so check the serial console if you don't see an error pattern. The
pattern also depends on the display and strip still working.

The firmware shows zero for speeds below 1 mph. Once you're moving, it waits for
two consecutive samples below that threshold before returning to zero. The two
decimal places don't mean the GPS is that accurate; see the
[measurement summary](../README.md#what-the-measurements-show).

## Final checks

- [ ] USB boot, battery boot, switch OFF, and charging with the switch OFF work.
- [ ] All pixels animate without flicker or resets at your chosen brightness.
- [ ] You can tell the no-fix, normal, stale, and caught-error patterns apart.
- [ ] USB-C is reachable and the lid can open without pulling on solder joints.
- [ ] No exposed conductors or sharp edges touch skin, fabric, or the LiPo.
- [ ] Battery stays in place without being squeezed, bent, or pressed against
      hardware.
- [ ] Pod stays in place, the cable is strain-relieved at both ends, and the strip
      does not bend sharply at its pads.
- [ ] You can read the display while wearing it. Compare speed with a phone/watch
      to catch obvious problems; neither is a calibration reference.
- [ ] Check comfort after 10 minutes and record runtime at the chosen brightness.
      **90 minutes is a design target, not a measured result.**

## Troubleshooting

| Symptom | Check |
| --- | --- |
| No `CIRCUITPY` drive | USB data cable, switch ON, and correct UF2. `RPI-RP2` is the bootloader drive. |
| Blank serial console | Use a console that asserts DTR. On macOS, `screen /dev/cu.usbmodem… 115200` worked in this build; use your board's port name. Close other programs using the port. Exit screen with `Ctrl-A`, `K`, `y`. |
| Import error | Re-run the circup install command; copying only the three top-level libraries omits dependencies. |
| No `0x70` | Power off; check header alignment, display orientation, and solder joints. |
| No `0x10` | Power off; reseat the STEMMA QT cable and check its routing. |
| GPS responds but has no fix | Take the antenna outdoors with a clear view of the sky. A first fix can take minutes. Seeing the GPS on I²C only tells you the board can talk to it. |
| Display works but strip is dark | Battery/switch power path, shared ground, `DIN` direction, and the D6/resistor path. |
| Flicker or resets | Check battery voltage and connections under load, reduce brightness, and inspect the LED supply wiring. |
| No visible charge indication when closed | The case has no charge-LED window; open the pod to check. |
