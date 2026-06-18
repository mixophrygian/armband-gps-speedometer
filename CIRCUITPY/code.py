"""Armband GPS Speedometer - main firmware.

Copy this file to the Feather's CIRCUITPY drive as `code.py` after the bench
bring-up stages pass (see docs/bench-bringup.md). Requires these libraries in
CIRCUITPY/lib/: adafruit_gps, adafruit_ht16k33, neopixel.

Behavior (see docs/test-plan.md "Intentional State Tests"):
- Boot:               display "8888" + blue sweep across the LED strip.
- No fix (never had): display "----" + amber comet.
- Normal (has fix):   display mph (2 decimals) + rainbow comets.
- Stale/lost fix:     display "----" + yellow pulse.
- Caught error:       display "Err" + red flashing (latches until reset).

This firmware is safe to run with NO NeoPixel strip attached: driving D6 with
nothing connected is harmless, so you can flash it today and see mph on the
display outdoors. The LEDs light up once the lane is wired (Stage 7).
"""

import math
import time

import adafruit_gps
import adafruit_ht16k33.segments
import board
import busio
import neopixel

# --- Configuration ----------------------------------------------------------

KNOTS_TO_MPH = 1.15078

# NeoPixel layout. v2 is a single 10-pixel lane (armband space only fits ~10
# pixels at 60 LED/m). Change PIXELS_PER_LANE to match whatever you physically
# cut and wired. The lane scaffolding (LANE_COUNT / LANE_REVERSED / chain_index)
# is kept parameterized so a future multi-lane build only needs these constants
# changed; with one lane it is effectively a straight strip, no serpentine.
LANE_COUNT = 1
PIXELS_PER_LANE = 10
PIXEL_COUNT = LANE_COUNT * PIXELS_PER_LANE
LANE_REVERSED = (False,)  # single lane: no reversal
LED_PIN = board.D6
BRIGHTNESS = 0.12  # documented cap; lower it if the battery browns out

# A fix that disappears for longer than this is treated as stale/lost.
STALE_AFTER_S = 3.0

# Speeds below this are shown as 0.00. A physically stationary GPS still
# reports a slow random walk (each 1 Hz fix lands a few metres away, typically
# under ~1 mph); without this deadband the display jitters between 0 and a
# couple mph while you stand still.
SPEED_DEADBAND_MPH = 1.0

# How many consecutive below-deadband GPS speed samples are required before the
# display drops from a moving speed to 0.00. This rejects a one-sample bogus zero
# while moving without delaying the first real nonzero speed after you start.
ZERO_CONFIRM_SAMPLES = 2

# How often to refresh things (seconds).
DISPLAY_PERIOD_S = 0.35
LED_PERIOD_S = 0.03   # ~33 fps
GPS_PERIOD_S = 0.1    # poll the 1 Hz RMC stream in small non-jarring slices
# Cap a blocking GPS read so the main loop stays responsive.
GPS_READ_TIMEOUT_S = 0.02

# Comet animation rates. These are expressed as "old 33 fps frame steps" so the
# numbers stay easy to tune, then converted to elapsed-time movement in the loop.
NORMAL_STEP = 0.8     # running rainbow comet
NOFIX_STEP = 0.4      # amber "searching" comet
PULSE_STEP = 0.15     # stale pulse, radians
COMET_TAIL = 4.0      # comet tail length in pixels
# Comet spacing == lane length, so comets flow back to back: as one head exits
# the end, the next enters the start (no dark gap).
WAVE_PERIOD = PIXELS_PER_LANE

# Set True to print GPS status (state/fix/sentence/mph) over the USB serial console
# once per second. Leave False in the field.
DEBUG = False
DEBUG_PERIOD_S = 1.0

# --- Hardware setup ----------------------------------------------------------


def make_i2c():
    try:
        return board.I2C()
    except AttributeError:
        return busio.I2C(board.SCL, board.SDA)


i2c = make_i2c()
display = adafruit_ht16k33.segments.Seg7x4(i2c)
display.brightness = 0.8

pixels = neopixel.NeoPixel(
    LED_PIN,
    PIXEL_COUNT,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB,
)

gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False, timeout=GPS_READ_TIMEOUT_S)
# Output RMC only, update once per second. RMC carries fix status and speed, which
# keeps the main app from building a stale backlog of GPS sentences.
gps.send_command(b"PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

# --- LED helpers -------------------------------------------------------------


def chain_index(lane, physical_position):
    """Map a lane + left-to-right position to its index in the wired chain."""
    if LANE_REVERSED[lane]:
        physical_position = PIXELS_PER_LANE - 1 - physical_position
    return lane * PIXELS_PER_LANE + physical_position


def set_lane_pixel(lane, physical_position, color):
    pixels[chain_index(lane, physical_position)] = color


def scale_color(color, scale):
    return (int(color[0] * scale), int(color[1] * scale), int(color[2] * scale))


def draw_comet_stream(phase, color_for, tail_len=COMET_TAIL):
    """Draw a continuous stream of comets spaced WAVE_PERIOD apart.

    `phase` is the lead comet's head position (pixels). `color_for(n)` returns
    the (r,g,b) for comet index n, so each comet can be a different color.
    Anti-aliased: each pixel's brightness is a smooth function of its distance
    from each fractional head, so motion glides between pixels.
    """
    lead = int(phase // WAVE_PERIOD)
    # Only the lead comet and its neighbors can touch a short lane.
    for lane in range(LANE_COUNT):
        for pos in range(PIXELS_PER_LANE):
            r = g = b = 0.0
            for n in range(lead - 1, lead + 2):
                d = phase - n * WAVE_PERIOD - pos
                if d <= -1.0 or d > tail_len:
                    continue
                bright = 1.0 + d if d < 0.0 else 1.0 - d / tail_len
                cr, cg, cb = color_for(n)
                r += cr * bright
                g += cg * bright
                b += cb * bright
            set_lane_pixel(
                lane,
                pos,
                (
                    int(r) if r < 255.0 else 255,
                    int(g) if g < 255.0 else 255,
                    int(b) if b < 255.0 else 255,
                ),
            )
    pixels.show()


def draw_comet(color, head, tail_len=COMET_TAIL):
    """A single anti-aliased comet at fractional `head` (for the boot sweep)."""
    pixels.fill((0, 0, 0))
    cr, cg, cb = color
    for lane in range(LANE_COUNT):
        for pos in range(PIXELS_PER_LANE):
            d = head - pos
            if d <= -1.0 or d > tail_len:
                continue
            bright = 1.0 + d if d < 0.0 else 1.0 - d / tail_len
            set_lane_pixel(
                lane, pos, (int(cr * bright), int(cg * bright), int(cb * bright))
            )
    pixels.show()


def draw_pulse(color, phase):
    """Whole chain pulsing brightness via a sine on `phase` (radians)."""
    level = 0.15 + 0.85 * (0.5 + 0.5 * math.sin(phase))
    pixels.fill(scale_color(color, level))
    pixels.show()


def boot_sweep():
    """Show 8888 and sweep a blue comet down the chain once."""
    display.fill(0)
    display.print("8888")
    display.show()
    blue = (0, 120, 255)
    head = 0.0
    while head < PIXELS_PER_LANE + COMET_TAIL:
        draw_comet(blue, head)
        head += 0.5
        time.sleep(0.02)
    pixels.fill((0, 0, 0))
    pixels.show()


# --- Display helpers ---------------------------------------------------------


def format_mph(mph):
    """Fit mph into 4 seven-seg digits. 2 decimals below 100 mph; the display
    only has 4 digits, so degrade to 1 decimal at/above 100 to avoid overflow."""
    if mph < 0:
        mph = 0.0
    if mph < 100:
        return "{:.2f}".format(mph)  # e.g. 12.34, max 99.99
    if mph < 1000:
        return "{:.1f}".format(mph)  # e.g. 123.4
    return "999.9"


def nmea_sentence_type(sentence):
    """Return the 3-letter NMEA sentence type, e.g. RMC or GGA."""
    if not sentence:
        return None
    if isinstance(sentence, bytes):
        sentence = sentence.decode("ascii", "ignore")
    comma = sentence.find(",")
    if comma < 4:
        return None
    return sentence[comma - 3 : comma]


def show_text(text):
    display.fill(0)
    display.print(text)
    display.show()


# --- Error state -------------------------------------------------------------


def error_loop():
    """Latch on a caught error: flash red LEDs and show Err until reset."""
    on = False
    while True:
        on = not on
        show_text("Err")
        pixels.fill((60, 0, 0) if on else (0, 0, 0))
        pixels.show()
        time.sleep(0.3)


# --- Main --------------------------------------------------------------------


def main():
    boot_sweep()

    ever_had_fix = False
    last_fix_at = 0.0
    last_mph = 0.0

    last_display_at = 0.0
    last_led_at = 0.0
    last_gps_at = 0.0
    last_debug_at = 0.0
    wave_phase = 0.0
    pulse_phase = 0.0
    state = "nofix"
    mph = 0.0

    zero_sample_count = 0   # consecutive below-deadband speed samples
    last_sample_key = None  # GPS-clock timestamp of the last speed sample

    amber = (255, 70, 0)
    yellow = (255, 150, 0)

    # Rainbow comets for the running state: red, orange, yellow, green, blue,
    # indigo, violet. Violet is pushed pinker so it reads distinct from indigo.
    rainbow = (
        (255, 0, 0),
        (255, 60, 0),
        (255, 160, 0),
        (0, 255, 0),
        (0, 0, 255),
        (75, 0, 130),
        (180, 0, 160),
    )

    def rainbow_for(n):
        return rainbow[n % len(rainbow)]

    def amber_for(n):
        return amber

    # Wrap the phase at a whole number of rainbow cycles so it stays small (keeps
    # float precision) while keeping color order continuous across the wrap.
    wave_wrap = WAVE_PERIOD * len(rainbow)

    while True:
        now = time.monotonic()

        # Service LEDs before GPS/display I2C work so animation frames are not
        # held behind a read timeout. State changes show up on the next frame.
        if now - last_led_at >= LED_PERIOD_S:
            led_elapsed = now - last_led_at if last_led_at else LED_PERIOD_S
            last_led_at = now
            led_frames = led_elapsed / LED_PERIOD_S
            if state == "normal":
                wave_phase = (wave_phase + NORMAL_STEP * led_frames) % wave_wrap
                draw_comet_stream(wave_phase, rainbow_for)
            elif state == "stale":
                pulse_phase += PULSE_STEP * led_frames
                draw_pulse(yellow, pulse_phase)
            else:  # nofix
                wave_phase = (wave_phase + NOFIX_STEP * led_frames) % wave_wrap
                draw_comet_stream(wave_phase, amber_for)

        gps_updated = False
        sentence_type = None

        # Read the 1 Hz GPS a couple times a second. Reading it every loop would
        # overwork the shared I2C bus; each scheduled read is bounded by timeout.
        if now - last_gps_at >= GPS_PERIOD_S:
            last_gps_at = now
            # One sentence per read, on purpose. The GtopI2C driver can't tell
            # when its buffer is empty (in_waiting is hardcoded to 16), so reads
            # can wait for their timeout if no full sentence is ready. The short
            # constructor timeout above keeps a miss from stalling the LEDs.
            gps_updated = gps.update()
            if gps_updated:
                sentence_type = nmea_sentence_type(
                    getattr(gps, "nmea_sentence", None)
                )
            # Use the actual post-read time for freshness and UI scheduling.
            now = time.monotonic()

        # RMC carries its own active/void flag. Use it directly so the main app
        # does not need GGA just to decide whether the current RMC speed is valid.
        rmc_status = getattr(gps, "isactivedata", None)
        rmc_active = (
            sentence_type == "RMC"
            and rmc_status is not None
            and rmc_status.lower() == "a"
        )
        has_fix = gps.has_fix or rmc_active
        if gps_updated and sentence_type in ("RMC", "GGA") and has_fix:
            ever_had_fix = True
            last_fix_at = now

        fresh_fix = ever_had_fix and (now - last_fix_at) < STALE_AFTER_S
        if fresh_fix:
            state = "normal"
        elif ever_had_fix:
            state = "stale"
        else:
            state = "nofix"

        # Take one speed sample per parsed RMC sentence. Sampling only after RMC
        # matters: GGA has a timestamp but no speed, and could otherwise make us
        # latch the previous speed for the new second before the real speed
        # sentence arrives.
        if (
            fresh_fix
            and gps_updated
            and sentence_type == "RMC"
            and gps.speed_knots is not None
            and gps.timestamp_utc is not None
        ):
            sample_key = (
                gps.timestamp_utc.tm_hour,
                gps.timestamp_utc.tm_min,
                gps.timestamp_utc.tm_sec,
            )
            if sample_key != last_sample_key:
                last_sample_key = sample_key
                raw_mph = gps.speed_knots * KNOTS_TO_MPH
                if raw_mph >= SPEED_DEADBAND_MPH:
                    zero_sample_count = 0
                    last_mph = raw_mph
                else:
                    zero_sample_count = min(
                        ZERO_CONFIRM_SAMPLES,
                        zero_sample_count + 1,
                    )
                    if last_mph == 0.0 or zero_sample_count >= ZERO_CONFIRM_SAMPLES:
                        last_mph = 0.0

        # In "normal" state keep showing the last good speed; a brief dropout
        # within the grace period should hold the reading, not blink to 0.00.
        # Once we go stale the display switches to "----" anyway, so reset and
        # drop the stale zero count so it doesn't skew reacquire.
        if state == "stale" or state == "nofix":
            last_mph = 0.0
            zero_sample_count = 0
            last_sample_key = None
        mph = last_mph

        if DEBUG and now - last_debug_at >= DEBUG_PERIOD_S:
            last_debug_at = now
            raw_mph = (
                gps.speed_knots * KNOTS_TO_MPH
                if gps.speed_knots is not None
                else None
            )
            print(
                "state:", state,
                "| fix:", has_fix,
                "| updated:", gps_updated,
                "| sentence:", sentence_type,
                "| raw mph:", round(raw_mph, 2) if raw_mph is not None else None,
                "| shown mph:", round(mph, 2),
                "| fix age:", round(now - last_fix_at, 1) if ever_had_fix else None,
            )

        # Update the display at a calm cadence.
        if now - last_display_at >= DISPLAY_PERIOD_S:
            last_display_at = now
            show_text(format_mph(mph) if state == "normal" else "----")

        time.sleep(0.005)


try:
    main()
except Exception as err:  # noqa: BLE001 - intentionally catch-all for field use
    print("FATAL:", err)
    error_loop()
