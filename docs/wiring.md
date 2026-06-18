# Wiring Guide

## System Layout

```text
Pod, charged in place via USB-C
+----------------------------------------------------+
| GPS antenna up        7-segment display readable   |
| Feather RP2040 + LiPo + perma-proto + DPDT switch  |
| USB-C cutout + charge LED window                   |
+--- hardwired 3-conductor cable (+, GND, data) -----+
                     |  (continuous, no connector)
Armband, semi-permanent LED
+----------------------------------------------------+
| lane 1: 10 pixels  ->                              |
+----------------------------------------------------+
```

> Note: this v2 **hardwires** the pod to the armband lane — three continuous
> conductors (`+`, `GND`, data), no pod-to-armband connector. The pod is charged
> **in place via USB-C** and never separates from the armband for daily use, so
> the connector that earlier plans used (to unplug the pod for charging) was
> dropped: fewer parts, fewer joints, and no non-locking connector to pop apart
> on a kid's arm. The trade-off is that pod and armband are now one captive unit
> — separating them later means desoldering. See `3d-printing-guide.md` for the
> documented 3D-printed pod.

This v2 is a **single 10-pixel lane** — the armband only has room for about 10
pixels at 60 LED/m. That removes the serpentine wiring and the lane-to-lane data
joints the original four-lane plan needed. The firmware still keeps the lane
scaffolding so it is one constant change away from multi-lane:

```python
LANE_COUNT = 1
PIXELS_PER_LANE = 10
LANE_REVERSED = (False,)   # single lane: no reversal
```

## I2C Devices

Use the Feather RP2040's default I2C/STEMMA QT bus:

| Device | Connection |
| --- | --- |
| 7-segment FeatherWing | Plugged into Feather headers; uses I2C address `0x70`. |
| Mini GPS PA1010D | STEMMA QT cable to the same I2C bus. |

Mount the GPS with its ceramic patch antenna facing skyward. Do not place the
display, LiPo, switch, or copper wiring over the GPS antenna.

## Header Stack And Remaining Connections

The display FeatherWing should not be soldered directly to the Feather. The
intended stack is:

```text
7-segment FeatherWing with male headers
        plugs into
Feather stacking-header sockets
        soldered to
Feather RP2040 through-holes
        with male tails available underneath
```

Those stacking-header tails are how the pod wiring gets access to Feather pins
after the display is installed. The through-holes are occupied, but not lost;
they now continue through the header pins.

Use these connection sources:

| Need | Connection source |
| --- | --- |
| LiPo battery | Feather JST-PH battery connector, not through-holes |
| Charging | Feather USB-C connector |
| GPS | Feather STEMMA QT connector, or `SDA`/`SCL` tails if the connector is blocked |
| LED data | `D6` stacking-header tail to perma-proto resistor |
| LED power | `BAT` stacking-header tail to DPDT switch/perma-proto |
| LED ground | `GND` stacking-header tail to perma-proto |
| Power switch | `EN` stacking-header tail to switch, then `GND` when off |

For v1, the cleanest layout is usually a small perma-proto next to or under the
Feather stack, with short wires from the accessible bottom tails. If you can make
a tidy underside proto mount without blocking USB-C, the tails can also be
soldered into that proto board.

## Pod-To-Armband Cable (Hardwired, No Connector)

The pod and the armband lane are joined by a **single hardwired 3-conductor
cable** — no connector. Earlier plans used a JST-PH 6-pin pair so the pod could
be unplugged for charging; charging now happens **in place via USB-C**, so that
reason is gone and the connector was dropped. The result is fewer parts, half
the solder joints, and no non-locking connector that can pop apart on a kid's
arm.

The three conductors:

| Conductor | From (pod) | To (armband) |
| --- | --- | --- |
| LED `+` | Feather `BAT` via the DPDT switch | lane `+` pad |
| LED data | Feather `D6` via the 470 ohm resistor | lane `DIN` pad |
| LED `GND` | Feather `GND` | lane `GND` pad |

Use 26-30 AWG silicone stranded wire with a consistent color convention (red
`+`, black `GND`, a third color for data). Run all three as one bundled cable
out of the pod to the lane.

> Trade-off you've accepted: with no connector, pod and armband are one captive
> unit. To separate them for service you desolder at the perma-proto. Leave a
> little extra cable length (service slack) so the pod can open and the lid lift
> without tugging the lane's solder joints — see `3d-printing-guide.md`.

Strain relief still matters, just at different points: clamp the cable where it
exits the pod (grommet) and immobilize it at the lane end so arm motion flexes
the cable, never the solder pads.

## NeoPixel Lane

Use one 10-pixel cut from the BTF-LIGHTING WS2812B strip (Pure Gold Wire,
60 LED/m, IP65). Only 10 pixels go into the build; the rest of the strip is
practice scraps and spares.

Data path:

```text
Feather D6
  -> 470 ohm resistor (330 ohm works; 300-500 ohm acceptable)
  -> hardwired data conductor
  -> lane DIN -> lane DOUT (unused)
```

Power:

```text
Feather BAT -> DPDT switch -> hardwired + conductor -> LED lane +
Feather GND ------------------------------------------> LED lane GND
```

A single lane needs no lane-to-lane chaining: `+`, `GND`, and data land on the
one lane's DIN end and that's it. Keep the LED ground tied to Feather ground.

Place the 100 uF capacitor **on the armband side**, across LED `+` and `GND`
at or near the lane's DIN end. Observe capacitor polarity. (Earlier
versions of this doc put the cap pod-side; armband-side is better practice
because the cap's job is to absorb switching transients at the LED input, and
a pod-side cap sees those transients only after the connector and cable have
already dropped some of them. If you'd rather not put a cap on the armband
for mechanical reasons, the pod-side placement still helps and is acceptable.)

The NeoPixel guides recommend ~1000 uF, but this build uses **100 uF**
intentionally: the strip is powered directly from a LiPo (no switching-supply
turn-on spike to absorb) at a 0.12 brightness cap across only 10 pixels, so the
transient current is tiny. 100 uF is more than ample here; parallel a second
100 uF for ~200 uF if you ever raise the brightness or pixel count. Do not
bother sourcing a 1000 uF part for this design.

## DPDT Power Switch

Use one DPDT switch so OFF disables both the Feather regulator and LED battery
power while leaving the LiPo plugged into the Feather for USB-C charging.

| Switch pole | Common lug | ON throw | OFF throw |
| --- | --- | --- | --- |
| Feather enable | Feather `EN` | Not connected | Feather `GND` |
| LED power | LED `+` (hardwired conductor) | Feather `BAT` | Not connected |

The Feather `EN` pin is pulled up internally. Grounding `EN` turns off the 3.3V
regulator. The second pole prevents the LED strip from staying connected to the
LiPo when the wearable is off.

The LiPo stays plugged into the Feather JST-PH battery connector at all times.
Charging happens through Feather USB-C. The enclosure needs a USB-C opening and
a small window or light pipe for the charge status LED.

## Practical Wearable Notes

- Never let the LiPo bend, crush, rub against solder joints, or sit under screw
  heads.
- Cover exposed LED strip pads with heat shrink or flexible sealant.
- Strain-relieve the hardwired cable where it exits the pod (clamp at the
  grommet) and where it meets the lane, so arm motion flexes the cable, never
  the solder pads. Leave a little service slack so the pod can open without
  tugging joints.
- Do not sharply bend the LED strip at solder pads. Let fabric/foam flex around
  the strip segments.
- Keep a common ground between Feather, GPS/display I2C, and LEDs.
