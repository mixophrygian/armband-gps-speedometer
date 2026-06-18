# Bench Bring-Up Guide

This guide gets the electronics working in stages before anything is mounted to
the armband. The goal is to find mistakes while the hardware is still easy to
hold, inspect, and rework.

Do not plug in the LiPo while soldering. Do not power the Feather from USB while
adding/removing boards. Unplug power first, change hardware, inspect, then power
again.

## What You Need On The Bench

- Feather RP2040
- 7-segment FeatherWing
- Feather stacking headers
- Male header strips for the 7-segment FeatherWing
- PA1010D GPS
- STEMMA QT cable
- USB-C data cable
- Computer with a serial console editor such as Mu, Thonny, or the CircuitPython serial console
  - On macOS, the reliable console is `screen /dev/cu.usbmodem101 115200` (baud 115200).
    The board only streams once DTR is asserted; `screen` does this, but the VS Code
    Serial Monitor extension does not, so it shows nothing. Quit screen with
    `Ctrl-A` then `K` then `y`. If a port is stuck/busy, run `pkill screen`.
    The exact device name may differ; list ports with `ls /dev/cu.usbmodem*`.
- Soldering iron, solder, flush cutters, and something to hold headers straight
- Later stages: NeoPixel strip (BTF-LIGHTING WS2812B Pure Gold Wire, 60 LED/m, IP65 — 1 m is plenty), 470 ohm resistor, 100uF capacitor (see wiring.md for why 100uF instead of the usual 1000uF), 26-30 AWG silicone wire for the hardwired pod-to-lane cable (v2 has no pod-to-armband connector), LiPo (Adafruit 2000 mAh PID 2011, standard polarity), and a 6mm-bushing DPDT toggle switch
- Multimeter — required at Stage 6 for battery polarity verification; also useful throughout for continuity and short checks

## Stage 1: Feather Alone

1. Leave the display, GPS, LEDs, switch, and LiPo disconnected.
2. Plug the Feather into the computer with a USB-C data cable.
3. If a drive named `CIRCUITPY` appears, CircuitPython is already installed.
4. If no `CIRCUITPY` drive appears, install CircuitPython:
   - Unplug USB.
   - Hold the Feather `BOOTSEL` button while plugging USB back in.
   - A drive named `RPI-RP2` should appear.
   - Download the Feather RP2040 CircuitPython UF2 from CircuitPython.org.
   - Drag the UF2 file onto `RPI-RP2`.
   - The board should reboot and appear as `CIRCUITPY`.
5. Copy `CIRCUITPY/bringup/01_feather_serial.py` from this repo to the mounted board as `code.py`.
6. Open the serial console.

Success: the console prints `Feather RP2040 alive:` once per second. If your
board exposes `board.LED`, that LED also blinks.

If it fails:
- Try another USB-C cable; many cables are charge-only.
- Confirm the drive is named `CIRCUITPY`, not `RPI-RP2`.
- Reinstall CircuitPython if the drive contents look strange.

## Stage 2: Install Libraries

Install these libraries into the board's `CIRCUITPY/lib/` folder:

- `adafruit_gps`
- `adafruit_ht16k33`
- `neopixel`

Manual method:
1. Download the Adafruit CircuitPython Library Bundle that matches your major
   CircuitPython version.
2. Open the bundle's `lib/` folder.
3. Copy `adafruit_gps.mpy`, the `adafruit_ht16k33/` folder, and `neopixel.mpy`
   into `CIRCUITPY/lib/`.

`circup` method:

```sh
circup install -r CIRCUITPY/lib/requirements.txt
```

Run that command from this project folder while the Feather is mounted.

## Stage 3: Assemble The 7-Segment FeatherWing Itself

Do this before soldering anything onto the Feather. The 7-segment FeatherWing
often comes as a FeatherWing PCB/backpack plus the LED display module. The LED
module must be soldered onto the FeatherWing PCB before the Feather can drive
it. Adafruit's assembly guide is here:
`https://learn.adafruit.com/adafruit-7-segment-led-featherwings/assembly`.

1. Unplug USB. Leave the LiPo disconnected.
2. Keep the Feather set aside. You are only working on the display FeatherWing.
3. If the LED display module is already soldered to the FeatherWing PCB, inspect
   the joints and skip to Stage 4.
4. Prepare the 12-pin and 16-pin male header strips for the FeatherWing:
   - Cut them to length if needed.
   - Put the long pins down into a breadboard so the short pins point up.
   - Place the FeatherWing PCB over the short pins.
   - Solder one corner pin on each row, confirm the PCB sits flat, then solder
     all remaining header pins.
5. Align the LED display module on the FeatherWing PCB:
   - Match the decimal point dots to the silkscreen; they should be on the
     bottom side indicated by the board.
   - Do not install the display upside down.
6. Solder the LED display module to the FeatherWing PCB:
   - Go slowly, one pin at a time.
   - Clip each display leg short after soldering if it is in the way.
7. Inspect the FeatherWing:
   - No solder bridges between adjacent display pins.
   - No solder bridges between adjacent header pins.
   - Display module is flat and correctly oriented.

## Stage 4: Solder Feather Stacking Headers And Install The Display

This step makes the display plug cleanly into the Feather while leaving the
stacking-header tails accessible underneath for later pod wiring.

Do not solder the display FeatherWing directly to the Feather. The Feather gets
the stacking headers; the assembled display FeatherWing plugs into the sockets
on top. The male tails underneath the Feather remain usable connection points
for `D6`, `BAT`, `GND`, `EN`, and any other signals needed later.

1. Unplug USB. Leave the LiPo disconnected.
2. Solder the stacking headers onto the Feather:
   - Put the female sockets on the component/top side of the Feather.
   - The male tails pass down through the Feather holes.
   - Solder from the underside of the Feather.
   - Start with one corner pin on each row, check that both headers are straight,
     then solder the remaining pins.
3. Plug the assembled 7-segment FeatherWing into the Feather's top sockets.
   Align both rows; do not offset by one pin. The display should sit above the
   Feather, LED side up.
4. Plug USB back in.
5. Copy `CIRCUITPY/bringup/02_i2c_scan.py` to the Feather as `code.py`.

Success: the serial console reports an I2C address `0x70`.

Then copy `CIRCUITPY/bringup/03_display_test.py` to the Feather as `code.py`.

Success: the display shows `8888`, then a counting number.

If it fails:
- Power off and check the display is not shifted by one pin.
- Power off and confirm the LED display module is not upside down.
- Reflow any dull or cracked header joints.
- Run the I2C scanner again. No `0x70` means the display is not electrically connected.

## Stage 5: Connect And Test The GPS

1. Unplug USB.
2. Plug one end of the STEMMA QT cable into the Feather's STEMMA QT port.
3. Plug the other end into the PA1010D GPS.
4. Place the GPS with the ceramic antenna facing upward.
5. Plug USB back in.
6. Copy `CIRCUITPY/bringup/02_i2c_scan.py` to the Feather as `code.py`.

Success: the scanner should show `0x70` for the display and `0x10` for the GPS.

Then copy `CIRCUITPY/bringup/04_gps_test.py` to the Feather as `code.py`.

Success: the serial console prints fix status and satellite count once per
second. Take the GPS outdoors for the first real fix; the first fix can take a
few minutes. Once fixed, it prints latitude/longitude and speed in knots.

If it fails:
- Reseat both ends of the STEMMA QT cable.
- Confirm the GPS antenna side is facing up.
- Move outdoors, away from buildings and metal surfaces.
- Add the CR1220 coin cell later to improve warm-start behavior.

## Stage 6: Confirm Battery Charging

Do this before the LEDs, while the current draw is still small.

The battery for this build is the Adafruit 3.7V 2000mAh LiPo, PID 2011. It uses
Adafruit-standard JST-PH polarity and should plug straight into the Feather, but
do the polarity check anyway before first power. Plugging in a reversed-polarity
battery will damage the Feather's charger IC, the battery, or both. This is the
most common way people kill Feathers. Do not skip the check.

1. Unplug USB.
2. Verify the battery polarity before plugging it into the Feather:
   - Look at the Feather RP2040 silkscreen next to the JST-PH battery socket.
     It marks `+` and `-` for the two contacts. On the Feather RP2040, `+` is
     the contact closer to the USB-C port; `-` is the outboard contact.
   - With the battery still unplugged, take a photo or note which colored wire
     of the battery enters which side of the JST housing. Do not trust the
     wire color alone — confirm electrically in the next step.
   - Set a multimeter to DC volts (20 V range). Carefully probe the bare metal
     of each contact through the slots in the battery's JST-PH connector:
     red probe on the contact you think is `+`, black on the contact you think
     is `-`.
       - A positive reading (~3.7-4.2 V) means the wire on your red-probe side
         is `+`. Confirm that wire lines up with the Feather's `+` silkscreen
         mark when the connector is oriented to plug in.
       - A negative reading means the battery's `+` and `-` are swapped
         relative to where the Feather expects them.
   - If swapped:
       - Depress the tiny barb on each metal contact with a pin or fine
         tweezers and slide the contact out the back of the JST housing.
       - Swap the two contacts so they sit in the opposite positions.
       - Push them back in until they click and gently tug each wire to
         confirm it's seated.
       - Re-check with the multimeter before plugging into the Feather.
   - Only proceed once the multimeter confirms `+` on the battery aligns with
     `+` on the Feather silkscreen.
3. Put the Feather on a non-conductive surface.
4. Plug the LiPo into the Feather JST-PH battery connector.
5. Plug USB back in.
6. Confirm the Feather charge LED turns on or indicates charging.
7. Let it charge for a few minutes and confirm the LiPo does not get hot, puff,
   or smell odd.
8. Leave `03_display_test.py` on the board, or copy it back to the board as
   `code.py`, so the display gives you a visible battery-power indicator.
9. Unplug USB and confirm the Feather can boot from battery by watching the
   display counter.

Success: the board runs from USB, charges the LiPo, and also runs from battery.

Stop immediately if the battery heats up, swells, smokes, smells odd, or the
connector polarity does not match the Feather silkscreen after the multimeter
check.

## Stage 7: Test The LED Lane

This v2 uses a single 10-pixel lane, so this one stage is the whole LED bring-up
— there is no separate four-lane stage anymore. Do this on the bench before
bonding the lane to the armband.

1. Unplug USB and LiPo.
2. Cut one 10-pixel lane from the BTF-LIGHTING WS2812B NeoPixel strip.
3. Find the `DIN`, `+`, and `GND` pads. Follow the strip's data arrows; wire
   into the `DIN` end (the `DOUT` end stays unused).
4. Wire Feather `D6` through the 470 ohm resistor (a single 330 ohm is fine —
   300-500 ohm acceptable) to strip `DIN`. The resistor sits in series on the
   data line: `D6` -> resistor leg 1, resistor leg 2 -> `DIN`.
5. Wire strip `GND` to Feather `GND`.
6. For this test, wire strip `+` to Feather `BAT` or to the planned switched LED
   power line.
7. Add the 100uF capacitor across strip `+` and `GND`, observing polarity.
8. Plug in the LiPo, then USB.
9. Copy `CIRCUITPY/bringup/05_one_lane_neopixel_test.py` to the Feather as `code.py`.

Success: the 10-pixel lane shows a low-brightness chasing pattern.

If it fails:
- Check that data goes into `DIN`, not `DOUT`.
- Check that LED ground and Feather ground are connected.
- Check capacitor polarity.
- Keep brightness low during testing.

> Single lane means no serpentine and no lane-to-lane data joints — the part
> that was the hardest soldering in the four-lane plan is simply gone. If you
> later want more lanes, the firmware only needs `LANE_COUNT`, `PIXELS_PER_LANE`,
> and `LANE_REVERSED` changed in `code.py`.

## Stage 8: Switch Test

Only add the DPDT switch after the Feather, display, GPS, battery, and the LED
lane have all worked independently.

1. Unplug USB and LiPo.
2. Wire switch pole 1:
   - Common lug to Feather `EN`.
   - OFF throw to Feather `GND`.
   - ON throw left unconnected.
3. Wire switch pole 2:
   - Common lug to LED `+` (the hardwired conductor to the lane).
   - ON throw to Feather `BAT`.
   - OFF throw left unconnected.
4. Plug in LiPo.
5. Turn switch ON: Feather and LEDs should power.
6. Turn switch OFF: Feather and LEDs should turn off.
7. Plug in USB with LiPo still connected and confirm charging still works.

Success: the switch turns the wearable off, but USB-C charging still works
because the LiPo remains connected to the Feather charger.

## Stage 9: Full Firmware

After every staged test passes:

1. Copy this repo's `CIRCUITPY/code.py` to the Feather as `code.py`.
2. Power on.
3. Confirm boot behavior:
   - Display shows `8888`.
   - LEDs show a blue sweep.
   - Display shows `----` while waiting for GPS.
   - LEDs show an amber no-fix wave.
4. Take the setup outdoors.
5. Confirm GPS fix and mph display.

Do not put the boards in the pod until this stage works on the bench.
