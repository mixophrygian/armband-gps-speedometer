# Wiring

The Feather and display share a soldered proto hub. The GPS connects by STEMMA QT;
the ten-pixel strip connects through a captive three-conductor cable. Disconnect
USB and the LiPo before soldering or changing connections.

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

The switch paths above close in opposite positions; see the pole table below.
The battery stays connected to the charger in both positions.

| Connection | Route |
| --- | --- |
| Display | FeatherWing male headers into Feather stacking-header sockets; default I²C bus, `0x70` |
| GPS | Feather STEMMA QT connector; same I²C bus, `0x10` |
| LED data | Feather `D6` → 470 Ω resistor on proto → strip `DIN`; `DOUT` unused |
| LED power | Feather `BAT` → switch pole B → strip `+` |
| LED ground | Feather `GND` → strip `GND` |
| LiPo | Feather JST-PH battery connector; verify polarity electrically against board markings |
| Charging | Feather USB-C; no battery disconnection needed |

Feather stacking-header tails solder into the proto hub below it. Keep the
display removable above it. Maintain separate nets for `BAT`, switched LED `+`,
`GND`, `EN`, and the two sides of the data resistor. Check the proto's connected
rows before placing the resistor or making rail connections.

## DPDT power switch

| DPDT pole | Common lug | ON throw | OFF throw |
| --- | --- | --- | --- |
| A: regulator enable | Feather `EN` | Unconnected | Feather `GND` |
| B: LED supply | LED `+` | Feather `BAT` | Unconnected |

Identify each common and its throws with a continuity meter; do not infer them
from lever direction. Both poles must produce the table's ON/OFF states together.
Grounding `EN` disables the Feather's 3.3 V regulator. The second pole removes
LED battery power. OFF leaves the battery/charger circuit connected, so unplug
the battery as well as USB for hardware work.

## LED power and cable

Use 26 AWG silicone stranded wire, with red for switched `+`, black for `GND`,
and a third color for data. The strip uses direct LiPo power and Feather 3.3 V
data; initial firmware brightness is capped at `0.12`.

An optional 100 µF, 6.3 V-or-higher capacitor goes across switched LED `+` and
`GND` near the strip's `DIN` end, with correct polarity and insulated leads.
The prototype was operated without it. This value is a suggested addition,
not a measured guarantee of supply stability; recheck operation if the strip,
cable, brightness, or pixel count changes.

Feed the cable through the enclosure before soldering its proto end. Anchor it
at the pod exit and at the strip, leaving enough slack to lift the lid. The
anchors must take a tug before the solder pads do. Insulate exposed pads and
avoid sharp bends at joints. Final mechanical order and checks are in the
[build guide](build.md#assembly).

Mount the GPS outside the lid with its ceramic antenna facing skyward and clear
of the display, wiring, and other hardware. Keep the battery insulated from
header tails and solder joints. The current CAD has a USB opening but **no
dedicated charge-indicator window**; check the Feather's charge LED with the
lid open or provide a separate viewing opening/light pipe.
