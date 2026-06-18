# Enclosure Design (Hand-Built Box)

> **STATUS: DRAFT / not committed.** This is a working proposal, not a locked
> design. The lid-as-chassis approach, charge-in-place, exposed GPS, box size,
> and connector placement are all still up for change. Dry-fit and revise before
> committing to any cuts or purchases.

A v1 electronics pod built from an off-the-shelf ABS project box, not
3D printed. Goal: hold every board with the GPS antenna and display facing
skyward, USB-C and the charge LED reachable without opening the pod, the switch
reachable but guarded. The pod is **hardwired to the armband lane and charged in
place via USB-C** — it stays mounted on the armband and only opens for service.

This v1 will be **chunky** — it's a lot of through-hole hardware on an arm.
Prioritize fit, access, and safe wiring over compactness.

## Core Architecture: Everything Mounts To The Lid

The whole electronics module attaches to the **underside of the lid**. The
**base is just a cover/shell** that drops over it.

Why: lift the lid and the whole electronics assembly comes up with it. The only
thing crossing the lid/base boundary is the **hardwired armband cable**, which
enters the base grommet and runs to the lid-mounted perma-proto — leave it
**coiled with service slack** so the lid lifts a few cm without tugging it. You
also build the module lid-face-down on the bench, which is far easier than
working inside a deep box.

Consequences of this choice (all designed around below):

- The **display, Feather stack, GPS, battery, and perma-proto all hang from the
  lid** into the base.
- All **port openings (USB-C, charge LED, switch) go in the base walls**,
  positioned to line up with the hanging boards **when the lid is closed**. You
  lose port access while open — fine, since you only open it to work on it.
- The armband cable is **hardwired** (3 conductors: `+`, `GND`, data) — no
  pod-to-armband connector. It enters through a **grommet in the base bottom**
  (strain-relieved to the base) and runs up to the perma-proto on the lid. Leave
  **coiled service slack** so the lid lifts a few cm for bench work without
  tugging solder joints. Because the cable is captive, the lid no longer fully
  detaches from the base — full separation means desoldering at the perma-proto.
  This was a deliberate trade for fewer parts and no pop-apart connector.
  **Charging is via the USB-C port in place**, so the pod does not need to come
  apart for daily use.

## Component Inventory And Dimensions

| Component | Footprint (mm) | Height (mm) | Mounting |
| --- | --- | --- | --- |
| Feather RP2040 + 7-seg FeatherWing stack | 50.8 x 22.8 | ~27 envelope (tallest) | Long standoffs lid -> Feather; display flush to lid window |
| Mini GPS PA1010D (PID 4415) | 25.5 x 25.4 | 8.2 | Antenna flush through a lid cutout (exposed) |
| LiPo battery (PID 2011) | 60 x 36 | 7 | Foam tape + strap to the lid (it hangs, so grip it well) |
| Perma-proto **half-size** (PID 1609), trimmed | ~65 x 51 (from 51 x 81 stock) | ~12 with parts | Seats the whole Feather + spare wiring rows; cut the length only. Quarter-size was too small. |
| DPDT **toggle** switch (6mm bushing) | body ~13 x 12 x 10 | ~33 with lever | Bushing through a 6.5mm round hole + printed guard ribs (see cad/enclosure.scad) |

> Confirm every number against your actual parts with calipers before cutting.
> Heights especially grow with headers, soldered components, and wire bends.

### Feather + display stack height breakdown

The tallest thing in the pod is the Feather/display sandwich. The stacking
headers add height in **two** places — the board-to-board gap *and* the tails
that hang below the Feather:

| Layer (top -> bottom) | Height (mm) |
| --- | --- |
| 7-seg display body above the FeatherWing PCB | ~8 |
| FeatherWing PCB | ~1.6 |
| Stacking-header board-to-board gap (plastic spacer) | ~8.5 |
| Feather PCB | ~1.6 |
| Stacking-header male tails below the Feather | ~7.5 |
| **Total envelope: display top -> tail tips** | **~27** |
| Board stack only: display top -> Feather PCB bottom | ~20 |

With the lid as chassis, the display is at the lid; the Feather and its tails
hang ~20-27 mm down into the base. The perma-proto nests in the space below the
Feather where the tails come down to wire into it. Measure your own stack: tail
length and display body height vary by part and how you trimmed the legs.

## Recommended Box Size

Target **internal** dimensions (with margin for wiring, padding, and dry-fit
slop):

- Length: **~90 mm**
- Width: **~55 mm**
- Height: **~35 mm** (clears the ~27 mm hanging stack + window/seating/lid clearance)

That's roughly a **100 x 60 x 45 mm external ABS project box**. Search terms:
"ABS project box 100x60x45" (or 100x68x50). Favor a **taller** box if unsure —
the ~27 mm hanging stack is the binding constraint, and you can always pad empty
space. Pick a box with a **screw-down lid** so you can reopen it during bring-up.

## Layout (looking at the lid's underside, before you lower the base on)

```text
        <--------------- ~90 mm length --------------->
       +-----------------------------------------------+
   ^   | [GPS antenna   |  [ Feather + display STACK ]  |
   |   |  flush in lid  |  display flush to lid window  |
 ~55mm |  cutout]       |  (50.8 x 22.8, hangs ~27)     |
   |   |  [ battery,    |  [perma-proto NESTED below    |
   v   |   foam+strap ] |   the Feather, wired to tails]|
       +-----------------------------------------------+
         hardwired cable exits this end (grommet) -> armband
         USB-C / charge-LED / switch -> base side walls (align when closed)
```

Everything in that diagram is **fixed to the lid**. The base carries only the
cable grommet, which the hardwired armband cable passes through on its way to
the lid-mounted perma-proto.

## Hardwired Cable (No Connector)

The pod connects to the armband lane through a **single hardwired 3-conductor
cable** (`+`, `GND`, data) — no pod-to-armband connector. The connector earlier
plans used existed so the pod could be unplugged for charging; with charge-in-
place via USB-C that reason is gone, so it was dropped for fewer parts and no
pop-apart failure mode.

- The cable runs from the **perma-proto on the lid**, out the **base grommet**,
  to the armband lane.
- Leave **coiled service slack** at the perma-proto end so the lid can lift a
  few cm for bench work without tugging joints.
- **Strain-relieve at the grommet** (cable tie to an internal boss or a glued
  stop) so a tug on the armband can't reach the solder joints.

Consequence: pod and armband are **one captive unit**. The lid no longer fully
separates from the base+cable — to take them apart you desolder at the perma-
proto. That's the accepted trade for a simpler, more robust wearable.

Charging: via the **USB-C port in place** through the base cutout. The pod does
not detach from the armband for daily use.

## Cut List

Mark from your dry-fit, then cut. Sizes are starting points — measure your parts.

### In the LID (the chassis / skyward face)

| # | Opening | Size (mm) | Notes |
| --- | --- | --- | --- |
| 1 | 7-seg display window | Cut **~1-2 mm smaller** than the display module all around | Leaves a lip the display seats against (see flush-mount below) |
| 2 | GPS antenna cutout | ~ the ceramic antenna footprint | Antenna sits flush in it, exposed to the sky; PCB stays inside |

### In the BASE walls (align when the lid is closed)

| # | Opening | Size (mm) | Notes |
| --- | --- | --- | --- |
| 3 | USB-C port | ~10 x 5, cut a little oversize | Aligns to the Feather's USB-C jack when closed |
| 4 | Charge LED window | ~2-3 dia hole or light pipe | Next to the USB-C cutout, over the CHG LED |
| 5 | DPDT switch slot | ~13 x 7 (fit your switch) | Recessed/guarded so it can't be bumped off |
| 6 | Cable grommet (armband cable) | ~6-8 dia hole + rubber grommet | In the **base bottom**; the hardwired 3-conductor cable passes through and is strain-relieved here. Leave coiled service slack inside so the lid can lift |

## Flush-Mounting The Display

The trick: the display rests against a **lip**, and **standoffs from the lid**
carry the load.

1. Cut the window **slightly smaller** than the display module so a ~1-2 mm lip
   of lid plastic overlaps the display edge. The display face presses against
   that lip from inside -> flush with the lid's outer surface, and the lip stops
   it pushing out.
2. Run **long standoffs (~20 mm) from the lid down to the Feather's mounting
   holes** (Feather is the bottom of the stack). These hold the assembly and
   press the display gently against the lip.
3. **Do not let the lip carry weight** — it only sets the flush position. The
   standoffs carry the load so the display's solder joints aren't stressed.
4. Add a **clear cover** behind the window (see below) for protection.

## Display Window Cover

The bare LED module will get scratched and knocked on a kid's wearable. Add a
hard cover behind the window:

- Use **polycarbonate (Lexan), not acrylic** — polycarbonate is impact
  resistant; acrylic is brittle and cracks.
- **Best: RED-tinted transparent polycarbonate.** Your display is the red
  version (PID 3108); a red filter over red LEDs sharply boosts contrast and
  daylight readability by darkening the "off" segments. Directly helps the
  "readable while running" requirement.
- ~1.5 mm thick, cut a few mm larger than the window, glued behind the opening
  from inside the lid.

## Tools And Cutting Technique

ABS is soft and forgiving — it cuts/drills cleanly and does not shatter like
acrylic.

| Opening type | Best tool |
| --- | --- |
| Round holes (charge LED, screw holes) | Drill + **step ("Unibit") bit** |
| Rectangular cutouts (display, USB-C, switch) | **Drill the corners**, then connect with a **hand nibbler** (easiest), coping/jeweler's saw, or rotary tool with a cutting wheel |
| Edge cleanup | Needle files or sandpaper |

- A **hand nibbler (~$10)** is the easiest, safest way to make clean rectangular
  cutouts in a thin ABS wall — no power tools, no melting.
- With a rotary tool, go **slow / low speed** — too fast melts and gums ABS.
- Always cut **slightly undersize, then file to fit.**
- Mark with a fine Sharpie after dry-fitting the boards.

## Assembly And Safety Notes

- **Battery hangs from the lid** — foam tape **plus** a strap/zip-tie or a
  foam-lined pocket so it can't drop. Never compress, bend, or rest it on solder
  points or screw heads.
- **Standoffs / foam tape** secure boards; favor nylon standoffs for the stack
  (it takes force) and foam/glue for light parts. Keep metal screws away from
  the battery.
- **Strain relief:** clamp the hardwired armband cable at the base grommet
  (cable tie to an internal boss, or a glued knot/zip-tie stop) so a tug on the
  armband can't reach the solder joints. Leave coiled service slack between the
  grommet and the perma-proto so the lid lifts without tensioning the wires.
- **Switch guard:** recess the DPDT switch or add a raised rib so arm motion
  can't flip it off mid-run.
- **GPS sweat protection:** the exposed antenna's PCB should get a thin
  conformal coat or a bead of clear silicone around the cutout edge, since a
  kid's arm sweat will reach it. (If you'd rather keep it sealed, mount it under
  thin plastic instead — GPS works fine through a few mm of ABS.)
- **Edges:** round/sand sharp box corners; cover internal sharp solder tails so
  nothing pokes toward the arm.
- **Wire length:** leave the armband cable long enough that the lid lifts a few
  cm without tugging joints.

## Pre-Cut Confirm Checklist

- [ ] Base internal depth clears the ~27 mm hanging stack envelope (incl. tails) + clearance.
- [ ] All footprints fit on the lid with the perma-proto nested below the Feather.
- [ ] Display window lip lines up with the LED face when the stack is mounted.
- [ ] GPS antenna sits flush in its lid cutout, no metal/battery beside or above it.
- [ ] USB-C and charge-LED base cutouts align with the Feather when the lid is closed.
- [ ] Switch reachable but guarded.
- [ ] Battery is strapped (not just taped) so it can't drop when inverted.
- [ ] Hardwired armband cable enters a base grommet (strain-relieved) with coiled service slack so the lid can lift a few cm.
- [ ] Lid closes without pinching wires or crushing the battery.
