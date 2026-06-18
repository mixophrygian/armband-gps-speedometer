# 3D Printing the Enclosure — From Zero

You've never printed anything, so this starts at the beginning and stays applied:
every step is tied to producing *this* box. The CAD file is `cad/enclosure.scad`.

## The one mental model to start with

A 3D print goes through **three** programs, not one. People new to it usually
think "CAD file → printer" and get stuck when the printer won't open their file.

1. **Design (CAD)** — you make the shape. That's `enclosure.scad`, opened in
   OpenSCAD. Output: an **STL** file (a watertight mesh of the shape).
2. **Slice** — separate software (Bambu Studio / Orca for the Bambu, PrusaSlicer
   for the Prusa) chops the STL into layers and writes machine instructions
   (**G-code / .3mf**) for *your specific printer and filament*.
3. **Print** — the printer runs the sliced file.

CAD knows nothing about your printer; the slicer is where printer- and
material-specific reality enters. Keep these three buckets separate in your head
and nothing about this will be confusing.

---

## Part 1 — OpenSCAD: see the box, then bend it to your parts

### Install and first render (Mac)

1. Download OpenSCAD from `openscad.org/downloads.html`, drag to Applications.
   (Free, ~40 MB. Windows/Linux builds are on the same page.)
2. Open `cad/enclosure.scad` in it. You'll see code on the left, a 3D view on
   the right.
3. Press **F5** (Preview — fast). The box appears. Drag to orbit, scroll to zoom.
4. At the top of the file, change `part = "assembled"` to `"base"`, press **F5**
   again. Now you see just the shell. Try `"lid"`. This is how you'll look at
   each piece.

That's the whole interaction loop: **edit a number → F5 → look**. OpenSCAD is
"CAD by typing," which sounds backwards but is exactly why it's the right tool
here — every dimension is a labeled variable, so making the box fit your parts is
editing numbers, not nudging geometry with a mouse.

### Design at a glance (the compact layout)

The box is **~69 × 61 × 41 mm** (plus two small screw ears on the ends). It's
**layered**: the display (centred) and GPS live at the lid; below them the column
is **battery → perma-proto → Feather → display**, with the battery flat on the
floor. That keeps the heaviest part lowest (low centre of gravity on your arm).
Reaching ~41 mm tall assumes you **trim the stacking-header tails** after wiring
and **trim the half-size perma-proto** to a small hub.

Two things to know:

- **GPS over the battery — mostly a non-issue here.** The battery overlaps the
  GPS in plan, but it sits ~28 mm *below* the lid-mounted antenna — about a patch
  antenna's near-field edge (λ/2π ≈ 30 mm at L1), with the GPS's own ground plane
  in between. That vertical gap does the real work, so expect at most a minor
  effect, not a meaningful sensitivity loss (and the battery is passive metal,
  not an RF noise source). On an arm-worn device the body under the antenna is a
  bigger lower-side RF load than the battery anyway. If you ever want more GPS
  margin, the real lever is a larger ground plane under the patch (copper tape to
  GND) — the PA1010D's weak point — not relocating the battery.
- **Want it even smaller?** Three levers: a shorter battery (the 60 mm cell sets
  the box length), trimming the stacking-header tails after wiring (shaves
  height), and cutting the perma-proto hub down to a small perfboard scrap so it
  tucks into dead space instead of needing its own room.

### How the file is built (so you can change it)

Open the file and read top to bottom — it's commented for exactly this. The
structure:

- **`MEASURED PARTS`** — real-world sizes (Feather, display, GPS antenna,
  battery). These came from the documented parts in `docs/bom.md`. Several
  are marked **`(VERIFY)`** — those are the ones I'm least sure of and you must
  confirm with calipers.
- **`ENCLOSURE SHELL`** — cavity size and wall thicknesses. The cavity
  (`inner_l/w/h`) is the empty space your parts live in; the outer size follows
  automatically.
- **`LAYOUT`** — an X/Y coordinate for each part (where it sits when you look
  down at the lid). These are the numbers you'll nudge after a dry-fit.
- **`GEOMETRY`** — the actual modeling. You rarely touch this.

The load-bearing idea: **you do not redraw anything to refit a part.** Measure
your real battery, type its true length into `batt_l`, press F5. If it now pokes
out of the cavity, bump `inner_w`. That feedback loop is the entire skill.

### Check the fit without printing

`cad/verify_fit.py` is an optional sanity check that mirrors the same numbers
and redraws the top-view plan (`cad/enclosure_plan.png`). Run it after you
change dimensions if you want a quick text/plan check before printing:

```
python3 cad/verify_fit.py
```

It already caught two layout bugs while I was setting this up (the GPS was
clipping the wall and overlapping the display stack). The printed parts and
actual dry-fit are still the real gate. If you change a number in the `.scad`,
update the matching value at the top of `verify_fit.py` before relying on its
output.

### Export the STL

For each part you want to print: set `part` (e.g. `"base"`), press **F6** (full
render — slower, makes it watertight), then **File → Export → Export as STL**.
For the lid, use **`part = "lid_print"`** — that's the lid pre-flipped so its
flat face is down, ready to slice. Export `base.stl` and `lid.stl`.

---

## Part 2 — The order that saves you a wasted print

Do **not** print the fully-featured version first. The internal mounts (printed
Feather posts, battery cradle, GPS retainer) depend on exact part positions you
haven't dry-fit yet. Sequence:

1. **Leave `mount_features = false`** (it already is). Export and print the
   **base only** first — it's the cheapest way to learn your printer and confirm
   the cavity swallows your boards.
2. **Dry-fit.** Drop your actual Feather stack, GPS, and battery into the printed
   base. Confirm they fit with room for wiring. Measure anything that's off with
   calipers and update the `.scad`.
3. **Print the lid** (`part = "lid_print"`), still plain. Check the display
   window lines up with the display face and the GPS antenna pokes through its
   hole. Adjust `stack_x/stack_y` and `gps_x/gps_y` if not.
4. **Now set `mount_features = true`**, tune the mount positions to your dry-fit,
   optionally re-run `verify_fit.py`, and reprint the lid. The base rarely needs
   a reprint.

This is the difference between "print once, glue everything, done in an evening"
(totally fine — you said so) and "print, dry-fit, refine." Start with #1
regardless; it's your real first print and a throwaway is cheap insurance.

A zero-cost version of the dry-fit: print the plan (`cad/enclosure_plan.png`) at
100% scale on paper, lay your parts on it, and check before you print anything.

---

## Part 3 — Slicing (Bambu and Prusa)

You have both a Bambu Lab and a Prusa — both are excellent and both run PETG out
of the box. Pick whichever's free; the steps are the same shape.

**Bambu Lab** → Bambu Studio (or Orca Slicer). **Prusa** → PrusaSlicer.

1. **Open the slicer, pick your exact printer model and nozzle** (almost always
   0.4 mm) from its dropdown. This is the step that makes the file printer-correct.
2. **Import** `base.stl` (and later `lid.stl`). It drops onto the virtual plate.
3. **Orientation** — this matters more than any setting:
   - **Base:** floor flat on the plate, opening up. Import orientation is already
     correct. The walls print upward; the USB/switch cutouts are holes in
     vertical walls and bridge fine with no support.
   - **Lid:** flat outer face **down** on the plate, mount features pointing up.
     If you exported with `part = "lid_print"` it's already oriented; otherwise
     rotate 180° about X. Printed this way the lid needs **no supports**.
4. **Filament:** select a **PETG** profile (e.g. "Generic PETG" or the Bambu/Prusa
   PETG preset). Don't use the default PLA profile.
5. **Key settings** (the presets are mostly right; sanity-check these):
   - Layer height **0.2 mm** (0.28 for the fit-test base if you want it faster).
   - Walls/perimeters **3+** — it's a wearable that gets dropped.
   - Infill **15–20%**, grid or gyroid.
   - Supports **off** (with the orientations above you don't need them).
   - **Brim 3–5 mm** — PETG can lift at the corners; a brim prevents it and peels
     off after. Cheap insurance on a ~70 mm-long flat part.
6. **Slice**, eyeball the layer preview, then **send to the printer** (Bambu: over
   network/SD; Prusa: export G-code to SD/USB).

---

## Part 4 — PETG and the actual print

**Why PETG, briefly:** the default everyone starts with is PLA, which goes soft
around 55–60 °C. A car in summer sun hits that and your box deforms. PETG stays
solid to ~80 °C and shrugs off sweat, UV, and impact — the right call for an
outdoor kid's wearable. It's the second most common filament after PLA: every
spool vendor stocks it, it's cheap, and both your printers handle it natively.
(ABS/ASA is even tougher but warps and smells while printing — not worth it here.)

**PETG quirks vs PLA, so they don't surprise you:**
- Hotter: nozzle ~235–245 °C, bed ~70–85 °C (let the preset set it).
- Likes a **dry** spool — if it's been open in humid air for months, dry it first
  (printer's built-in dry cycle, or a food dehydrator) or you'll get stringing.
- Sticks to smooth PEI build plates *really* well — a thin swipe of glue stick
  acts as a **release** agent so you don't chip the plate prying parts off.
- A little **stringing** (fine hairs) is normal; they brush off.

**Running it:**
1. Make sure the build plate is clean (IPA wipe) and loaded with PETG.
2. Start the print. **Watch the first layer** — that's where 90% of failures
   happen. It should look like flat, slightly-squished lines fully stuck down,
   no gaps and not see-through. If it's not sticking, stop and re-level / re-set
   Z-offset (your printer's wizard does this).
3. The base is ~1–2 hours; the lid similar. Let the bed cool before removing —
   PETG often pops off on its own as the plate cools.
4. **Post-processing:** the holes may have a thin "bridge" skin or whiskers — open
   them with a hobby knife or a quick twist of a drill bit by hand. Self-tapping
   M3 screws cut their own threads into the bosses; drive slowly so you don't
   strip them.

---

## Print day — taking files to a shared / unknown machine

You don't control the machine, so make the files universal and carry a cheat-sheet.

### Before you leave the house

1. **Plug in your measured numbers and optionally re-run the check.** Open `enclosure.scad`,
   set the `MEASURE`/`VERIFY` values to your real calipered numbers — at minimum
   `stack_hang`, `stack_envelope` (the assembled display→Feather→tail-tips drop),
   `gps_ant_l/w`, and the switch body height. `python3 cad/verify_fit.py` can
   catch obvious layout mistakes, but dry-fitting the real boards is the gate.
2. **Export three STLs.** In OpenSCAD set `part` to each of `base`, `lid_print`,
   and `baseplate`; press **F6**, then **File → Export → Export as STL**.
   - Leave `mount_features = false` for this first round (plain box).
   - For the baseplate's first print, set **`mount_radius = 1000`** so it prints
     **flat** — far easier than a curved plate, and a 3 mm PETG plate pulled down
     by 12 sew/rivet points will conform to a "somewhat curved" stiff brace. Only
     model the real curve if the flat one visibly rocks on the brace.
3. **STL is universal** — it loads in any slicer (Bambu Studio, PrusaSlicer, Cura,
   Orca). You don't need to know the machine in advance.

### What to physically bring

- USB stick with the **3 STLs**, plus a cloud/email copy as backup.
- The **actual electronics** — assembled Feather/display stack, battery, switch —
  to **dry-fit into the base on the spot**. This is the whole point of going: find
  out it fits (or doesn't) before you leave.
- **Calipers.**
- A **PETG spool** if the shop lets you load your own filament; otherwise ask what
  they have. PLA is fine for the *throwaway test base* only — get PETG for the
  real build (see Part 4 for why).
- This guide.

### At the machine (any slicer)

1. Import the STL.
2. Select **the machine's own printer profile** (ask staff which model) and a
   **0.4 mm nozzle**.
3. Filament: **PETG** if available.
4. **Orientation** (this is the part people get wrong):

   | Part | Sits on the bed as | Support |
   | --- | --- | --- |
   | `base` | floor down, opening up (as exported) | none |
   | `lid` (use `lid_print`) | flat outer face down, features up | none |
   | `baseplate` (flat) | flat bottom down, rails up | none |

5. Settings: **0.2 mm** layer, **3** perimeters, **15–20 %** infill, **supports
   OFF**, **brim 5 mm**.
6. Slice, eyeball the preview, and **print the `base` first**.

### Order on the day

Print the **base first** → **dry-fit your boards into it right there** → if it's
good, print the **lid** and **baseplate** in the same session. If something's off,
note exactly what, and it's a one-variable fix back home rather than a bad full
set of prints. Bringing the electronics is what turns one trip into a finished
fit instead of a guess.

---

## When you're back at it

The realistic path: install OpenSCAD, render the box, **print the plain base
first** as your learning print, dry-fit your boards, then refine. Everything
above is reference you can come back to. When you hit the dry-fit step and the
numbers need changing, that's the moment to come back and we'll tune the layout
together.
