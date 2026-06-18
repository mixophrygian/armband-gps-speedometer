# Test Plan

## Bench Tests

- USB boot: Feather appears as CIRCUITPY, runs `code.py`, and shows boot pattern.
- Battery boot: unplug USB, turn switch on, and confirm display/LED startup.
- Switch off: display, GPS, and LEDs all turn off.
- USB-C charging: with LiPo plugged in, USB-C powers the charger and charge LED is visible.
- I2C display: display shows `8888` at boot and `----` while waiting for GPS.
- GPS: PA1010D gets an outdoor fix with the antenna facing up.
- LED lane: all 10 pixels respond; the comet/wave runs cleanly down the lane.
- Brownout check: at configured brightness, no random resets or flicker.

## Intentional State Tests

- No GPS fix: cover/start indoors and confirm amber wave + `----`.
- Normal running/walking: go outdoors and confirm numeric mph + fixed-rate rainbow wave.
- GPS stale/lost: block GPS sky view after a fix and confirm yellow pulse + `----`.
- Caught code error: temporarily raise an exception after setup and confirm red flashing + `Err`.

## Wear Tests

- Pod does not slide on the armband.
- Hardwired pod-to-lane cable is strain-relieved; a tug on the armband reaches the grommet clamp, not the solder joints.
- The LED lane does not sharply bend at solder pads.
- No exposed copper, solder, pins, or sharp enclosure edges touch skin/clothing.
- LiPo is not compressed, bent, punctured, hot, or rubbing against hardware.
- Charging works in place via USB-C with the pod mounted on the armband (the pod is hardwired to the lane; it does not detach for charging).

## Acceptance Criteria

- Runtime reaches at least 90 minutes with normal LED brightness.
- Display remains readable while walking/running outdoors.
- GPS speed is plausible compared with a phone/watch.
- All status patterns are distinguishable to an adult helper.
- The kid can put on/remove the armband without managing loose wires.
