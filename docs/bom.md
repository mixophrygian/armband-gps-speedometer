# Bill of materials

Parts for one armband. The linked boards and battery define the enclosure fit;
measure substitutes before printing. See [wiring](wiring.md) and
[assembly](build.md#assembly) for connections and placement.

## Electronics

| Qty | Part | Constraint / part used |
| --- | --- | --- |
| 1 | [Adafruit Feather RP2040, PID 4884](https://www.adafruit.com/product/4884) | USB-C, LiPo charger, STEMMA QT |
| 1 | [Adafruit Mini GPS PA1010D, PID 4415](https://www.adafruit.com/product/4415) | I²C receiver; mounts outside the lid, antenna skyward |
| 1 | [0.56-inch four-digit seven-segment FeatherWing](https://www.adafruit.com/product/3108) | PID 3108 red or 3110 yellow; HT16K33 driver |
| 1 | [Protected 3.7 V, 2000 mAh LiPo, PID 2011](https://www.adafruit.com/product/2011) | Nominal 60 × 36 × 7 mm; verify actual size and connector polarity |
| 1 | [STEMMA QT / Qwiic cable](https://www.adafruit.com/product/4399) | Allow slack to move the GPS for service |
| 10 pixels | WS2812B strip, 60 LEDs/m | About 167 mm; prototype used BTF-LIGHTING IP65, black PCB, “Pure Gold Wire” strip |
| 1 set | Feather stacking headers | Sockets above the Feather, tails below for the proto hub |
| 1 set | Male headers for the FeatherWing | Display plugs into the Feather |
| 1 | 470 Ω resistor | Series LED data resistor; 330 Ω is an alternative |
| 1 | DPDT toggle, 6 mm threaded bushing | Body approximately 13 × 12 × 10 mm; CAD hole is 6.7 mm |
| 1 | [Half-size perma-proto, PID 1609](https://www.adafruit.com/product/1609) | Trim the 81 mm length to about 65 mm; retain the 51 mm width |

## Mechanical parts and consumables

| Item | Constraint / purpose |
| --- | --- |
| Kid-sized wrist splint or suitable armband | Must accommodate the pod and roughly 167 mm LED strip |
| Printed base, lid, and baseplate | [CAD and print settings](3d-printing-guide.md) |
| Small mounting screws | Match the printed pilots and GPS board; check length against internal clearance |
| 26 AWG silicone stranded wire | Three-conductor LED cable plus short switch connections |
| Heat shrink, strain-relief tie points or grommet | Insulate joints and anchor both ends of the LED cable |
| Felt / insulating sheet and foam | Separate LiPo from solder/header tails; support the stack without compressing the cell |
| Adhesive, hook-and-loop, heavy thread, stretchy fabric | Secure the baseplate and retain the LED strip mechanically |
| USB-C data cable | Firmware upload and charging |

Tools: soldering equipment, multimeter, cutters, calipers, and access to a PETG
printer. Slice the supplied meshes for the actual printer and filament.

## Optional additions

- **100 µF electrolytic capacitor, rated 6.3 V or higher:** recommended provision
  across the LED input supply. The prototype notes record operation without it;
  no transient measurement establishes a minimum capacitance. See
  [LED power](wiring.md#led-power-and-cable).
- **CR1220 backup cell:** fits the GPS board's backup holder and can preserve
  receiver state between uses. It is not needed for normal operation.

The strip is driven directly from the LiPo with 3.3 V data in this prototype.
Check replacement strips across the battery's operating range; matching the
WS2812B name alone does not establish identical electrical behavior. Runtime
and outdoor readability are [verification targets](build.md#final-checks),
not guaranteed specifications.
