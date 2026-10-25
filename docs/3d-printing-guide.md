# Enclosure

The CAD source is [`cad/enclosure.scad`](../cad/enclosure.scad). With the lid
closed, the shell measures **75.8 × 61.8 × 41 mm**, excluding the screw ears,
baseplate, switch lever, and external GPS. Inside, there's 71 × 57 × 36 mm of
space; the baseplate footprint is 87.8 × 68.8 mm.

The LiPo sits below the trimmed perma-proto and Feather/display stack. USB-C exits
the **−X (left) wall**; the three LED wires exit the **+X (right) wall**. The lid
has a display window, a 6.7 mm toggle-switch hole, and a 6 mm GPS cable hole. The
GPS mounts **outside**, antenna up, using two diagonal screws. Choose its position
and drill the holes during assembly; neither is set in the CAD. The current model
has no internal GPS retainer, antenna opening, switch guard, or charge-LED window.

![Enclosure layout](../cad/enclosure_plan.png)

The diagram shows the layout, with approximate GPS placement and component
heights. **Don't use it as a full-size drilling or fit template**—check the CAD
and your actual parts. There's also a [larger diagram](../cad/enclosure_plan_slide.png).

## Export and print

Render each `part` in OpenSCAD with F6 and export under the names below. Start with
`mount_features = false` to print a plain shell for checking fit. Setting it to
true adds a battery cradle to the base and Feather posts to the lid; check their
positions before reprinting.

| `part` selector | STL | Orientation | Suggested settings |
| --- | --- | --- | --- |
| `base` | [`base.stl`](../cad/base.stl) | Floor down, opening up | PETG, 0.2 mm layers, 3+ perimeters, 15–20% infill |
| `lid_print` | [`lid_print.stl`](../cad/lid_print.stl) | Outer face down; exported in this orientation | Same; features point up |
| `baseplate` | [`base_plate.stl`](../cad/base_plate.stl) | Underside down, locating rails up | Same; default `mount_radius = 10000` is nearly flat |

Start with supports off and add a 3–5 mm brim if needed. Check the slice preview,
especially the USB opening and the baseplate underside. Re-export after changing
parameters; the checked-in STLs won't update automatically. The `assembled`
preview lifts the lid by 4 mm to show its mating lip, so it appears taller than
the closed case.

## Fit parameters and checks

Print the plain base first and dry-fit the boards, battery, and wiring before
printing the lid and baseplate.

| Parameter | Current value | What to check |
| --- | --- | --- |
| `proto_l`, `proto_w` | 65 × 51 mm | Trimmed half-size perma-proto; this sets the required cavity footprint |
| `stack_x`, `stack_y` | −7, −4 mm | Display window and Feather alignment; USB is on the left |
| `stack_hang` | 22 mm | Display face to Feather PCB bottom; determines USB cutout height |
| `stack_envelope` | 27 mm | Display face to lowest header-tail tips; measure after soldering/trimming |
| `batt_l`, `batt_w`, `batt_h` | 62 × 37 × 7 mm | Actual cell, including wrapping and cable exit |
| `inner_l`, `inner_w`, `inner_h` | 71 × 57 × 36 mm | Room for the complete assembly, insulation, and wire bends |
| `disp_pkg_l`, `disp_pkg_w`, `disp_lip` | 50, 20, −2 mm | Produces a 54 × 24 mm display window |
| `usb_w`, `usb_h` | 15 × 10 mm | Connector and cable-plug clearance through the wall |
| `switch_x`, `switch_y`, `switch_hole_d` | −22, 18, 6.7 mm | Bushing/nut fit and internal body/terminal clearance |
| `gps_cable_x`, `gps_cable_y`, `gps_cable_d` | 25, −16, 6 mm | Cable route to the external GPS; check the connector passes through |
| `lip_clear` | 0.35 mm | Lid fit after printing; adjust for printer/material tolerances |

These dimensions leave just `inner_h − stack_envelope − batt_h = 2 mm` between
the battery and header tails. That's **before** any hub, solder, felt, or wiring
extending below those tips. Measure the complete stack and raise `inner_h` if
needed; don't use the lid to squeeze everything against the LiPo. Recheck USB and
display alignment after adding foam or changing the stack height.

This script reads the dimensions from the SCAD source and redraws the enclosure
layout. It needs Python and Matplotlib:

```sh
python3 cad/verify_fit.py
```

The script treats parts as rectangular boxes. You'll still need to check corners,
the mating lip, wires, fasteners, and the fit of the finished assembly. Keep
insulation between the battery and every solder joint or header tail. Thread the
LED cable through the base before soldering it to the hub. For the assembly steps
and GPS service loop, see [build guide: assembly](build.md#assembly).
