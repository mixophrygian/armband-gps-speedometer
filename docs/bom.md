# Bill of materials

These are the parts for one armband. The case is sized for the boards and battery
linked here, so measure any substitutes before printing. The [wiring](wiring.md)
and [build](build.md#assembly) guides show how they go together.

## Electronics

| Qty | Part | Notes |
| --- | --- | --- |
| 1 | [Adafruit Feather RP2040, PID 4884](https://www.adafruit.com/product/4884) | USB-C, LiPo charger, STEMMA QT |
| 1 | [Adafruit Mini GPS PA1010D, PID 4415](https://www.adafruit.com/product/4415) | I²C receiver; mounts on top of the lid, antenna facing up |
| 1 | [0.56-inch four-digit seven-segment FeatherWing](https://www.adafruit.com/product/3108) | PID 3108 red or 3110 yellow; HT16K33 driver |
| 1 | [Protected 3.7 V, 2000 mAh LiPo, PID 2011](https://www.adafruit.com/product/2011) | About 60 × 36 × 7 mm; check the actual size and connector polarity |
| 1 | [STEMMA QT / Qwiic cable](https://www.adafruit.com/product/4399) | Leave enough slack to move the GPS aside when opening the case |
| 10 pixels | WS2812B strip, 60 LEDs/m | About 167 mm; prototype used BTF-LIGHTING IP65, black PCB, “Pure Gold Wire” strip |
| 1 set | Feather stacking headers | Sockets above the Feather, tails below for the proto board |
| 1 set | Male headers for the FeatherWing | Display plugs into the Feather |
| 1 | 470 Ω resistor | Series LED data resistor; 330 Ω is an alternative |
| 1 | DPDT toggle, 6 mm threaded bushing | Body approximately 13 × 12 × 10 mm; CAD hole is 6.7 mm |
| 1 | [Half-size perma-proto, PID 1609](https://www.adafruit.com/product/1609) | Cut the 81 mm length down to about 65 mm; leave the 51 mm width alone |

## Mechanical parts and consumables

| Item | Notes |
| --- | --- |
| Kid-sized wrist splint or suitable armband | Needs room for the pod and roughly 167 mm of LED strip |
| Printed base, lid, and baseplate | [CAD and print settings](3d-printing-guide.md) |
| Small mounting screws | Match the printed pilot holes and GPS board; keep the tips clear of the battery and wiring |
| 26 AWG silicone stranded wire | Three-conductor LED cable plus short switch connections |
| Heat shrink, strain-relief tie points or grommet | Insulate joints and anchor both ends of the LED cable |
| Felt / insulating sheet and foam | Keep the LiPo away from solder joints and header tails; support the boards without squeezing the cell |
| Adhesive, hook-and-loop, heavy thread, stretchy fabric | Attach the baseplate and sew a retainer over the LED strip |
| USB-C data cable | Firmware upload and charging |

You'll need soldering equipment, a multimeter, cutters, calipers, and a printer
that can handle PETG. Slice the supplied STLs for your printer and filament.

## Optional additions

- **100 µF electrolytic capacitor, rated 6.3 V or higher:** a suggested addition
  across the LED supply. The prototype ran without one; voltage spikes weren't
  measured, so this isn't a tested minimum value. See
  [LED power](wiring.md#led-power-and-cable).
- **CR1220 backup cell:** fits the GPS board's backup holder and can preserve
  receiver state between uses. The GPS works without it.

This build powers the strip directly from the LiPo and drives it with 3.3 V data.
If you use a different WS2812B strip, test it with both a full battery and a low
one: strips sold under the same name can behave differently. Check
[runtime and outdoor readability](build.md#final-checks) on your finished build.
