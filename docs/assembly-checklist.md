# Assembly Checklist

## 1. Pre-Purchase Check

- [ ] All core boards are in the cart: Feather RP2040, PA1010D GPS, 7-segment FeatherWing.
- [ ] NeoPixel strip quantity is 2 m, even though only ~10 pixels (~167 mm) are used in v2.
- [ ] LiPo is Adafruit-compatible JST-PH polarity.
- [ ] STEMMA QT cable is present for the GPS.
- [ ] 26-30 AWG silicone wire (red/black/data color) for the hardwired pod-to-lane cable is present. (v2 uses no pod-to-armband connector; the JST-PH 6-pin pairs are spares.)
- [ ] DPDT slide switch is present.
- [ ] Resistor, capacitor, silicone wire, heat shrink, Velcro, foam, and USB-C cable are present.

## 2. Bench Bring-Up

- [ ] Follow `docs/bench-bringup.md` before mounting anything to the armband.
- [ ] Feather alone boots over USB and prints from `01_feather_serial.py`.
- [ ] CircuitPython libraries are installed in `CIRCUITPY/lib/`.
- [ ] 7-segment LED module is soldered to the display FeatherWing in the correct orientation.
- [ ] Display FeatherWing male headers are soldered straight.
- [ ] Feather stacking headers are soldered straight.
- [ ] I2C scan sees display address `0x70`.
- [ ] Display test shows `8888` and a counter.
- [ ] GPS is connected by STEMMA QT; I2C scan sees GPS address `0x10`.
- [ ] GPS test reports fix/satellites outdoors.
- [ ] LiPo charges over Feather USB-C and boots the Feather on battery.
- [ ] The 10-pixel NeoPixel lane works on the bench before bonding to fabric.

## 3. LED Lane Prototype (single 10-pixel lane)

- [ ] Cut one 10-pixel lane.
- [ ] Note the data direction arrow before sewing or bonding; wire into `DIN`.
- [ ] Solder `+`, `GND`, and data (through the 470 ohm resistor) to the `DIN` end.
- [ ] Heat-shrink every exposed LED lane joint.
- [ ] Verify all 10 pixels animate.

## 4. Switch And Charging Test

- [ ] Wire DPDT switch on the bench before final pod assembly.
- [ ] OFF position grounds Feather `EN`.
- [ ] OFF position disconnects LED `+` from Feather `BAT`.
- [ ] ON position leaves Feather `EN` floating and connects LED `+` to Feather `BAT`.
- [ ] LiPo charges from USB-C while the battery remains plugged into the Feather.
- [ ] Charge status LED is visible enough for the final pod design.

## 5. Pod And Armband Dry Fit

- [ ] GPS antenna is skyward and unobstructed.
- [ ] Display is readable while worn.
- [ ] Switch is reachable but not easy to bump accidentally.
- [ ] USB-C is reachable without opening the pod.
- [ ] LiPo is padded and isolated from solder joints.
- [ ] Hardwired pod-to-lane cable is strain-relieved at the pod grommet, with coiled service slack so the lid can lift.
- [ ] Pod Velcros on and off the armband cleanly.
  - Charging method is **finalized: charge-in-place via USB-C** — the whole unit
    stays on the armband while charging, so the pod does not need to come off for
    power. The USB-C port just needs to be reachable through a box opening.

## 6. Final Assembly

- [ ] Permanent wiring is soldered on the proto board. See `proto-soldering.md`
      for the step-by-step solder order (can be done before choosing an enclosure).
- [ ] All exposed joints are heat-shrunk or insulated.
- [ ] Boards are secured with standoffs, screws, or foam tape.
- [ ] Pod corners are rounded or padded.
- [ ] Armband has no scratchy solder, sharp plastic, or loose wire ends.
- [ ] Final firmware settings match the actual pixel count and lane orientation.

## 7. Field Test

- [ ] Outdoor GPS lock succeeds before running.
- [ ] Speed display is readable during movement.
- [ ] LEDs show no-fix, normal, stale/lost, and error patterns.
- [ ] Compare speed against a phone/watch.
- [ ] Check comfort after 10 minutes.
- [ ] Check battery warmth and runtime.
