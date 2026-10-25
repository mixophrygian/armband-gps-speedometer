# Assembly Checklist

## 1. Pre-Purchase Check

- [ ] All core boards are in the cart: Feather RP2040, PA1010D GPS, 7-segment FeatherWing.
- [ ] NeoPixel strip quantity is 1 m; the build only uses ~10 pixels (~167 mm).
- [ ] LiPo is Adafruit-compatible JST-PH polarity.
- [ ] STEMMA QT cable is present for the GPS.
- [ ] 26-30 AWG silicone wire (red/black/data color) for the hardwired pod-to-lane cable is present. (This build uses no pod-to-armband connector.)
- [ ] 6mm-bushing DPDT toggle switch is present.
- [ ] Resistor, capacitor, silicone wire, heat shrink, Velcro, felt/foam, stretchy fabric, heavy thread, adhesive, and USB-C cable are present.

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

- [ ] Baseplate orientation is correct before attachment; the display will read the right direction when worn.
- [ ] GPS antenna is skyward and unobstructed.
- [ ] Display is readable while worn.
- [ ] Switch is reachable but not easy to bump accidentally.
- [ ] USB-C is reachable without opening the pod.
- [ ] A small foam pad under the stack lifts/supports the display alignment without forcing the lid closed.
- [ ] A felt square isolates the battery from the Feather/perma-proto solder joints.
- [ ] LiPo is padded and isolated from solder joints.
- [ ] Hardwired pod-to-lane cable is strain-relieved at the pod grommet, with coiled service slack so the lid can lift.
- [ ] Pod Velcros on and off the armband cleanly.
  - Charging method is **finalized: charge-in-place via USB-C** — the whole unit
    stays on the armband while charging, so the pod does not need to come off for
    power. The USB-C port just needs to be reachable through a box opening.

## 6. Final Assembly

- [ ] Baseplate is attached to the armband with thread/Velcro; orientation has been checked.
- [ ] LED strip is glued down and also held with sewn stretchy fabric.
- [ ] Base is attached to the baseplate with adhesive; printed screw holes were used only as needed for alignment/backup.
- [ ] LED wires are fed through the base hole before they are soldered to the proto board.
- [ ] Permanent wiring is soldered on the proto board. See `proto-soldering.md`
      for the step-by-step solder order.
- [ ] USB-C port still aligns with the base window before the lid is closed.
- [ ] Wires fit inside the pod without crossing over the display/window.
- [ ] GPS board is screwed to the lid after battery installation; diagonal screws leave it able to hinge aside for battery service.
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
