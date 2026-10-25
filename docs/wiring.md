# Wiring

The display plugs into the Feather, whose header tails solder into the proto
board below it. The GPS connects by STEMMA QT, and the ten-pixel strip uses a
three-wire cable soldered at both ends. Unplug USB and the LiPo before soldering
or changing connections.

## Connections

```text
LiPo <----> Feather battery connector / USB-C charger
                  |
                  +-- BAT -- DPDT pole B (ON) -------- LED +
                  +-- GND --------------------------- LED GND
                  +-- D6 --- 470 Ω ------------------- LED DIN
                  +-- EN --- DPDT pole A (OFF) ------- GND
                  |
                  +-- 3V / GND / SDA / SCL --+-- display (0x70)
                                           +-- GPS     (0x10)

Optional 100 µF: LED + -- capacitor (+ to +, − to GND) -- LED GND
```

Pole A closes when the switch is OFF; pole B closes when it's ON. The battery
stays connected to the charger either way. The table below shows the lug wiring.

| Connection | Route |
| --- | --- |
| Display | FeatherWing male headers into Feather stacking-header sockets; default I²C bus, `0x70` |
| GPS | Feather STEMMA QT connector; same I²C bus, `0x10` |
| LED data | Feather `D6` → 470 Ω resistor on proto → strip `DIN`; `DOUT` unused |
| LED power | Feather `BAT` → switch pole B → strip `+` |
| LED ground | Feather `GND` → strip `GND` |
| LiPo | Feather JST-PH battery connector; check polarity with a meter against the board markings |
| Charging | Feather USB-C; no battery disconnection needed |

Keep the display removable. On the proto board, `BAT`, switched LED `+`, `GND`,
`EN`, and each side of the data resistor need separate connections. Check which
holes share a copper strip before placing the resistor or joining power rails.

## DPDT power switch

| DPDT pole | Common lug | ON throw | OFF throw |
| --- | --- | --- | --- |
| A: regulator enable | Feather `EN` | Unconnected | Feather `GND` |
| B: LED supply | LED `+` | Feather `BAT` | Unconnected |

Use a continuity meter to find each common lug and its throws; the lever direction
can be misleading. Check that both poles switch as shown in the table.
Grounding `EN` turns off the Feather's 3.3 V regulator, while the other pole cuts
battery power to the LEDs. OFF still leaves the battery connected to the charger,
so unplug the battery as well as USB before working on the wiring.

## LED power and cable

Use 26 AWG silicone stranded wire, with red for switched `+`, black for `GND`,
and a third color for data. The strip runs directly from the LiPo, with 3.3 V
data from the Feather. The firmware starts with brightness set to `0.12`.

If you add the optional 100 µF capacitor, use one rated for at least 6.3 V and
connect it across switched LED `+` and `GND`, near the strip's `DIN` end. Check
its polarity and insulate the leads. The prototype ran without one; 100 µF is
a suggestion, and supply spikes haven't been measured. Test again if you change
the strip, cable, brightness, or pixel count.

Feed the cable through the case before soldering its proto-board end. Anchor it
at the pod exit and at the strip, with enough slack to lift the lid. A tug on the
cable should reach the anchor before it reaches a solder pad. Insulate exposed
pads and keep sharp bends away from the joints. Follow the assembly order in the
[build guide](build.md#assembly).

Mount the GPS on top of the lid with its ceramic antenna facing up and clear
of the display, wiring, and other hardware. Keep the battery insulated from
header tails and solder joints. There's a USB opening, but **no window for the
charge LED**. Open the lid to check it, or add a window or light pipe if you want
to see it with the case closed.
