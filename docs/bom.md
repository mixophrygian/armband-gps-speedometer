# Bill of Materials

This is the complete shopping list to build one armband speedometer from
scratch. Adafruit PIDs are given where a specific part matters; equivalents from
other vendors work unless a note says otherwise.

## Core Electronics

| Qty | Item | Notes |
| --- | --- | --- |
| 1 | [Adafruit Feather RP2040, PID 4884](https://www.adafruit.com/product/4884) | Main controller, USB-C, built-in LiPo charger, STEMMA QT. |
| 1 | [Adafruit Mini GPS PA1010D STEMMA QT, PID 4415](https://www.adafruit.com/product/4415) | Mount antenna facing skyward, not under the display/battery. |
| 1 | [Adafruit 0.56" 4-Digit 7-Segment FeatherWing, PID 3108 (red) or 3110 (yellow)](https://www.adafruit.com/product/3108) | Yellow (3110) is a bit more readable in bright daylight; red (3108) is fine indoors/dusk. Either works. |
| 1 | [Adafruit Lithium Ion Battery 3.7V 2000mAh, PID 2011](https://www.adafruit.com/product/2011) | Adafruit-standard JST-PH polarity — plugs straight into the Feather, no re-pinning. Built-in protection circuit. 60 x 36 x 7 mm. The smaller 1200mAh PID 258 also works if you want a lighter pack. **Verify connector polarity against the Feather silkscreen before plugging in — some third-party packs ship reverse-wired (see bench-bringup.md Stage 6).** |
| 1 | [STEMMA QT / Qwiic JST-SH 4-pin I2C cable](https://www.adafruit.com/product/4399) | Connects the GPS to the Feather. |

## LED Lane

| Qty | Item | Notes |
| --- | --- | --- |
| 1m | BTF-LIGHTING WS2812B Pure Gold Wire LED Strip, 60 LED/m, IP65, black PCB (Amazon) | The build uses 10 pixels (1 lane); 1m (60 px) is plenty and leaves practice/splice scraps. Buy 2m if you want generous practice material. WS2812B = standard NeoPixel chip; Pure Gold Wire = premium bond-wire variant (more reliable than the ECO line) for a wearable that takes abuse. See [LED Strip Details](#led-strip-details) below. |

## Headers & Power Conditioning

| Qty | Item | Notes |
| --- | --- | --- |
| 1 | Feather stacking headers | Must be stacking-style: female sockets on top, male tails extending below the Feather. Plain male strips won't give the under-side access the wiring needs. |
| 1+ | Male header strip | For the 7-segment FeatherWing legs. |
| 1 | 470 ohm resistor | NeoPixel data line. Anything 300-500 ohm is fine; a single 330 ohm works too. |
| 1 | 100uF electrolytic capacitor, 6.3V+ | Place near the first LED on the armband side, not the pod-side connector. 100uF (vs the usual ~1000uF) is deliberate here: LiPo source, brightness capped at 0.12, only 10 px = tiny transients. See wiring.md. |
| 1 | Miniature DPDT switch — 6mm-bushing **toggle** | One pole disables Feather `EN`; one pole cuts LED `BAT+`. The 3D enclosure cuts a 6.5mm round hole + guard ribs for the toggle. |

## Wiring & Assembly

| Qty | Item | Notes |
| --- | --- | --- |
| 1 | **Half-size** perma-proto (51 x 81 mm), or generic perfboard | Pod wiring hub. A quarter-size board doesn't have enough holes to seat the Feather — use half-size [PID 1609](https://www.adafruit.com/product/1609). Trim to ~65 x 51 to fit the enclosure (cut the length only; this board sizes the box). |
| Several | 26-30AWG silicone stranded wire | Red, black, and a third color for data. |
| Several | Heat-shrink tubing | Cover every soldered LED-strip joint. |
| Several | Standoffs/screws or foam tape | Secure boards inside the pod. |
| 1 | USB-C data cable | Must transfer data, not just charge. |

## Mechanical / Enclosure

| Qty | Item | Notes |
| --- | --- | --- |
| 1 | Armband | Any wearable band; the LED lane is semi-permanently attached to it. |
| 1 | Pod/enclosure | Print the parametric enclosure in `cad/` (see `3d-printing-guide.md`), or use a hand-built ABS project box ~100 x 60 x 45 mm with a screw-down lid (search "ABS project box 100x60x45"). |
| Several | Velcro/hook-and-loop patches | Attach the pod to the armband. |
| Several | Flexible fabric/foam backing strips | Prevent sharp bends at LED solder joints. |
| Several | Cable tie points, thread, or adhesive | Strain relief at the pod-to-lane cable and LED lane ends. |

## Optional

| Qty | Item | Notes |
| --- | --- | --- |
| 1 | CR1220 coin cell | Improves GPS warm-start time. Not required. |

## Tools

| Item | Notes |
| --- | --- |
| Soldering iron + solder | Headers, LED-strip joints, and perma-proto wiring. |
| Multimeter | Required for the battery polarity check (bench-bringup.md Stage 6); also useful for continuity / short checks throughout. |
| Wire cutters / strippers | For the silicone wire and LED-strip leads. |

## LED Strip Details

**BTF-LIGHTING WS2812B Pure Gold Wire LED Strip Light**, 60 LED/m, IP65, black
PCB.

Build allocation:

- 10 pixels in service (1 lane x 10 pixels, lane ~167 mm / 6.6 in) — the armband
  only fits ~10 pixels at 60 LED/m
- The rest of a 1m strip (50 px) is practice scraps and splice spares

Why these specifics:

- **WS2812B chip** is the Adafruit `neopixel` library's reference part. No
  protocol surprises.
- **Pure Gold Wire** is BTF-LIGHTING's premium line. Pure-gold bond wires
  inside each LED package (vs aluminum or alloy on the ECO line) mean better
  corrosion resistance and longer-term reliability — relevant for a wearable
  that takes abuse.
- **IP65** silicone front coating adds sweat and scuff resistance. Sewing
  impact is negligible when sewing between LEDs.
- 60 LED/m at 10 px = ~167 mm lane length, fits the usable armband space and
  still gives room for a clean 5-7 px comet tail (8 px is the floor for a
  recognizable comet, so 10 has margin).
- 2000 mAh LiPo (PID 2011) runs the system many hours at brightness 0.12, far
  past the 90-minute runtime target, with only one lane driven.
- WS2812B is nominally 4-7 V; at 3.7 V LiPo it works but you may see slight
  color drift below ~3.4 V battery voltage. Acceptable at brightness 0.12.

Headroom: leftover strip gives you material to scale up later if you find more
armband real estate. To add pixels or lanes, change `PIXELS_PER_LANE` (and
`LANE_COUNT` / `LANE_REVERSED` for multiple lanes) in `CIRCUITPY/code.py`, and
update `PIXEL_COUNT` in `CIRCUITPY/bringup/05_one_lane_neopixel_test.py` to match
what you cut.

## Pre-Buy / Pre-Power Trap Check

- Battery polarity verified against the Feather silkscreen before plugging in,
  with a multimeter? (See `bench-bringup.md` Stage 6.)
- Stacking headers confirmed, not just plain male strips?
- 7-segment LED module is planned to plug into the Feather via stacking
  headers, not soldered directly to the Feather?
- USB-C cable is data-capable, not charge-only?
- Strain relief plan exists for the hardwired pod-to-lane cable (grommet clamp + service slack)?
- 470 ohm resistor and 100 uF cap for NeoPixel data and power?
- Enough heat shrink for all LED-lane solder joints plus connector joints?
- Way to see the Feather charge LED after the pod is assembled?
