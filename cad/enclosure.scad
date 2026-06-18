// ============================================================================
//  Armband GPS Speedometer  —  Enclosure  (parametric)  —  v2: COMPACT
//  Battery sits on the floor UNDER the Feather (lowest centre of gravity).
//  All units are MILLIMETRES.
// ----------------------------------------------------------------------------
//  HOW TO USE (OpenSCAD):
//    F5 = preview | F6 = render | export STL via File > Export
//    Choose what to show with `part` below. Watch the console: it ECHOes the
//    battery clearance and the computed USB cutout height every render.
//
//  Vertical stack-up, floor -> sky (per your assembly):
//    floor -> [LiPo 7mm, flat on the floor] -> small gap -> PERMA-PROTO
//    (the Feather's header tails plug DOWN into it) -> Feather (sits close above
//    the proto) -> stacking-header gap -> FeatherWing backpack -> 7-seg display
//    (face seats against the lid window). display+Feather+proto hang from the lid
//    as ONE plugged-together unit; the battery sits on the floor beneath them.
//    The half-size perma-proto (51 x 81) is far too LONG for this box (81 > 64),
//    so it's TRIMMED to a small hub (proto_l/proto_w) that fits under the Feather.
//    Still MEASURE the assembled drop (display face -> proto bottom) to confirm
//    the height - that's the one number specs can't give you.
//
//  Companion guide: docs/3d-printing-guide.md
// ============================================================================


// ============================================================================
//  WHAT TO RENDER / EXPORT  (one part at a time; export each as its own STL)
// ============================================================================
part = "base";   // "base" | "lid" | "lid_print" | "baseplate" | "assembled"
mount_features = false;   // false = plain box (print this FIRST); true = add posts/cradle
$fn = 56;


// ============================================================================
//  MEASURED PARTS  —  values are your Adafruit spec sheets. (VERIFY) = confirm.
// ============================================================================

// --- Feather RP2040 + 7-seg FeatherWing stack (tallest assembly) ------------
feather_l        = 51.0;   // Feather 51.0 x 23.0 x 7.5
feather_w        = 23.0;
stack_hang       = 22.0;   // display face (at lid) -> Feather PCB bottom   << MEASURE
stack_envelope   = 27.0;   // display face -> tail tips, TRIMMED tails      << MEASURE
                           //   (was ~29 untrimmed; trimming flush after wiring is
                           //    what gets the box to ~41mm. Don't trim -> set back
                           //    to ~29 and bump inner_h ~4mm.)
feather_hole_dl  = 45.72;  // Feather mount-hole spacing, lengthwise  (VERIFY)
feather_hole_dw  = 17.78;  // Feather mount-hole spacing, widthwise   (VERIFY)
//  stack_hang and stack_envelope set the box HEIGHT and the USB cutout height,
//  and they depend on your stacking headers + how far the display stands off
//  the backpack + how you trim the tails -- none of which is on a spec sheet.
//  So MEASURE the assembled stack: face->Feather-PCB, and face->tail-tips.
//  Defaults here are a conservative estimate (display standoff ~10, header gap
//  ~8.5, tails ~7.5). Trimming the tails drops stack_envelope ~4mm; shave inner_h.

// --- 0.56" 4-digit 7-seg display --------------------------------------------
disp_pkg_l       = 50.0;   // display face length   (MEASURE your part)
disp_pkg_w       = 20.0;   // display face height    (you measured ~20, spec said 19)
disp_lip         = -2.0;   // NEGATIVE = clearance. -2 => window is 4mm bigger than the
                           //   display (2mm slop all round), so a recessed display
                           //   shows through with a small border and needs no precise
                           //   alignment. (Use 0 for a tight flush fit, +1 for a lip.)

// --- Mini GPS PA1010D (PID 4415)  25.5 x 25.4 x 8.2 -------------------------
gps_pcb_l        = 25.5;
gps_pcb_w        = 25.4;
gps_ant_l        = 11.0;   // ceramic patch antenna footprint  (VERIFY!)
gps_ant_w        = 11.0;   // antenna pokes UP through a hole this size

// --- LiPo 2000 mAh (PID 2011)  60 x 36 x 7,  lies FLAT on the floor ---------
batt_l           = 62.0;   // sets the box LENGTH
batt_w           = 37.0;
batt_h           = 7.0;

// --- Perma-proto wiring hub (TRIMMED from a half-size 51 x 81 board) ---------
//  Half-size because the quarter board hadn't enough holes. The hub must seat
//  the WHOLE Feather AND give spare rows to wire in the switch + LED strip, so
//  it's 65 x 51 (cut only the 81mm length down to 65; width left uncut at ~51).
//  This board now DRIVES the box length AND width - see inner_l / inner_w.
//  Reference dims for the fit check (verify_fit.py); the proto isn't printed.
proto_l          = 65.0;   // length, cut down from the stock 81
proto_w          = 51.0;   // width, left at the stock 51 (uncut)

// --- Ports (sizes; positions are in LAYOUT / GEOMETRY) ----------------------
usb_w            = 15.0;   // USB-C cutout width  - oversized for position slop
usb_h            = 10.0;   // USB-C cutout height - oversized in case usb_z is off
led_d            = 3.0;    // charge-LED hole / light pipe
grommet_d        = 7.0;    // armband-cable grommet
//  SWITCH: your part is a TOGGLE with a 6mm threaded bushing (6-pin DPDT),
//  NOT a slide switch. So the cutout is a ROUND hole + nut, not a slot.
//  Body ~13(w) x 12(deep) x 10(tall) sits INSIDE the box; lever sticks OUT.
switch_hole_d    = 6.7;   // 6mm thread + clearance (some are 1/4" -> try 6.7)


// ============================================================================
//  ENCLOSURE SHELL
// ============================================================================
inner_l   = 71;    // now set by the 65mm trimmed proto + end slack (the proto is
                   //   the longest thing in the box, not the 60mm battery)
inner_w   = 57;    // holds the 51mm-wide proto hub (centred) with margin
inner_h   = 36;    // ~41mm external. ASSUMES trimmed tails (see stack_envelope).
                   //   battery(7) + proto(2) + stack(25) + clearance(2).
//  L and W are now driven by the wiring hub: it has to seat the whole Feather
//  PLUS spare rows for the switch + LED-strip wiring, so it's 65 x 51.
//  Height is still set by the vertical stack + battery underneath (CoG stays low).

wall      = 2.4;
floor     = 2.4;
lid_th    = 2.6;
corner_r  = 6.0;

// --- lid <-> base mating -----------------------------------------------------
lip_h     = 4.0;
lip_th    = 1.8;
lip_clear = 0.35;

// --- EXTERNAL screw ears (2x, short ends) ------------------------------------
ear_r          = 4.0;
ear_overlap    = 2.0;
ear_pilot_d    = 2.6;
ear_clear_d    = 3.4;
ear_head_d     = 6.2;
ear_head_h     = 2.2;

// --- printed internal mounts (only when mount_features = true) ---------------
post_od        = 5.0;
post_pilot_d   = 2.2;
cradle_wall    = 2.0;
cradle_clear   = 1.0;
cradle_h       = 5.0;

// --- mounting baseplate (separate part: pod-size, sewn on, NO outboard flange)
show_mount     = true;   // draw the baseplate under the pod in the "assembled" view
plate_th       = 3.0;    // plate thickness
mount_radius   = 10000;  // DEFAULT FLAT for printing. A concave dish only touches
                         //   the bed at its rim and FAILS mid-print, so print the
                         //   plate flat and curve it to the brace by HEAT-FORMING
                         //   (heat gun till floppy, press onto the brace, hold to
                         //   cool). Only set a real radius (e.g. 120) if you truly
                         //   intend to print the curve with supports - not advised.
rail_h         = 4.0;    // locating rails the pod body nests between (anti-rock)
rail_t         = 2.0;
mount_screw_d  = 3.2;    // M3 up into the pod's end ears (uses the bottom pilots)
// thread anchors (sew the plate to the brace; no outboard flange needed):
anchor_hole_d  = 2.6;    // pair of these per anchor - sew up one, down the other
anchor_gap     = 6.0;    // hole spacing within a pair
groove_w       = 3.5;    // top groove the thread loop recesses into (pod won't pinch it)
groove_depth   = 1.4;    // leaves ~1.6mm bridge under the thread - don't go deeper


// ============================================================================
//  LAYOUT  —  looking DOWN at the lid. (0,0) = box centre. +X right, +Y top.
// ============================================================================
stack_x = -7;    stack_y = -4;    // display/Feather REAL centre: FLUSH-LEFT (USB left),
                                 //   slightly below centre. From your measurement:
                                 //   proto flush to the bottom wall, Feather bottom
                                 //   13.35mm up -> Feather centre ~ -4 in Y.
                                 //   You soldered the Feather centred (USB end flush,
                                 //   ~centred in width), so the display lives in the
                                 //   MIDDLE - not pushed to an edge. VERIFY against
                                 //   your board: this is ~+7mm toward the USB end and
                                 //   ~1mm off centre in width, from your measurements.
batt_x  = 0;     batt_y  = 4;    // battery on the floor, under the stack

usb_y      = stack_y;     // USB-C/LED follow the Feather centre, on the +X end wall
led_gap    = -9;          // charge-LED hole this far from the USB; NEGATIVE = the
                          //   OTHER side of the USB (toward the bottom). Tune the
                          //   magnitude to your board's actual LED-to-USB spacing.

// Switch points UP through the LID, in the TOP-LEFT (above the down-pushed Feather)
switch_x   = -22;   switch_y = 18;

// GPS body glues ON TOP at the top-right, but its cable is surface-mounted and
// points DOWN - so the cable hole goes at the BOTTOM-RIGHT, where the cable drops
// in (also nearer the low Feather's STEMMA connector):
gps_cable_x = 25;   gps_cable_y = -16;   gps_cable_d = 6;

// LED cable grommet in the +X END WALL (LED-reserve / cut end is on the RIGHT).
// Placed HIGH so you solder the LED wires to the TOP of the proto and run them
// straight out - no underside soldering. Tune grommet_z to your wire height.
grommet_y  = 12;
grommet_z  = 26;
//  NOTE: usb_z (height up the +X wall) is DERIVED below from stack_hang.


// ############################################################################
//  GEOMETRY
// ############################################################################
outer_l = inner_l + 2*wall;
outer_w = inner_w + 2*wall;
inner_r = max(0.8, corner_r - wall);
wall_top_z = floor + inner_h;
ear_x = outer_l/2 + ear_r - ear_overlap;
ear_pos = [ [-ear_x, 12], [ear_x, -12] ];   // -X ear clears the (left) USB; +X ear clears the grommet
plate_l = 2*(ear_x + ear_r);          // reaches the ear mount screws; no flange
plate_w = outer_w + 2*(rail_t + 1.5); // just covers the locating rails
function brace_sag(R, w) = R - sqrt(R*R - pow(w/2, 2));
plate_sag = brace_sag(mount_radius, plate_w);

// USB-C jack sits ~3.2mm above the Feather PCB bottom; centre the cutout there.
usb_z = wall_top_z - stack_hang + 3.2;

// self-checks (read the console after F5)
echo(str("[fit] battery clearance = ", inner_h - stack_envelope - batt_h,
         " mm  (need >= 2; raise inner_h or trim tails if low)"));
echo(str("[fit] USB cutout centre = z ", usb_z, " mm up the +X wall"));

module rbox(l, w, h, r) {
    linear_extrude(height=h) offset(r=r) square([l-2*r, w-2*r], center=true);
}

// ============================================================================
//  BASE  —  deep shell. Print floor-down, opening up.
// ============================================================================
module base() {
    union() {
        difference() {
            union() {
                rbox(outer_l, outer_w, wall_top_z, corner_r);
                base_ears();
            }
            translate([0,0,floor]) rbox(inner_l, inner_w, inner_h+1, inner_r);
            base_ports();
            translate([outer_l/2 - wall/2, grommet_y, grommet_z])    // +X (RIGHT) end wall
                rotate([0,90,0]) cylinder(d=grommet_d, h=wall*3, center=true);
            ear_holes(pilot=true);
        }
        if (mount_features) battery_cradle();
    }
}

module base_ears() {
    for (p = ear_pos) translate([p[0], p[1], 0]) cylinder(r=ear_r, h=wall_top_z);
}

module base_ports() {                                          // switch is on the LID
    translate([-outer_l/2 + wall/2, usb_y, usb_z])              // USB-C, -X (LEFT) end wall
        cube([wall*3, usb_w, usb_h], center=true);
    // Charge-LED end-wall hole REMOVED: the CHG LED faces UP, so an end-wall hole
    // can't see it, and the enlarged USB was overlapping it (that exact touch was
    // the non-manifold warning). Put the indicator in the LID above the LED, or
    // use a light pipe - ask and I'll add it.
}

module battery_cradle() {
    translate([batt_x, batt_y, floor])
        difference() {
            rbox(batt_l + 2*cradle_clear + 2*cradle_wall,
                 batt_w + 2*cradle_clear + 2*cradle_wall, cradle_h, 2);
            translate([0,0,-1])
                rbox(batt_l + 2*cradle_clear, batt_w + 2*cradle_clear, cradle_h+2, 1.5);
            translate([0,0,cradle_h/2]) cube([batt_l + 40, 11, cradle_h], center=true);
        }
}

// ============================================================================
//  LID  —  chassis / skyward face. INSTALLED orientation (features hang down).
// ============================================================================
module lid() {
    union() {
        difference() {
            union() {
                rbox(outer_l, outer_w, lid_th, corner_r);
                base_ears_lid();
            }
            // display window (slides up flush) at the Feather's REAL centre
            translate([stack_x, stack_y, -1])
                rbox(disp_pkg_l - 2*disp_lip, disp_pkg_w - 2*disp_lip, lid_th+2, 1.5);
            // switch bushing - toggle points UP through here; body hangs inside
            translate([switch_x, switch_y, -1]) cylinder(d=switch_hole_d, h=lid_th+2);
            // GPS STEMMA cable hole - GPS sits ON TOP; only the cable passes through
            translate([gps_cable_x, gps_cable_y, -1]) cylinder(d=gps_cable_d, h=lid_th+2);
            ear_holes(pilot=false);
        }
        translate([0,0,-lip_h])
            difference() {
                rbox(inner_l - 2*lip_clear, inner_w - 2*lip_clear, lip_h, inner_r);
                translate([0,0,-1])
                    rbox(inner_l - 2*lip_clear - 2*lip_th,
                         inner_w - 2*lip_clear - 2*lip_th, lip_h+2, inner_r);
            }
        if (mount_features) feather_posts();
    }
}

module base_ears_lid() {
    for (p = ear_pos) translate([p[0], p[1], 0]) cylinder(r=ear_r, h=lid_th);
}

module feather_posts() {
    for (sx=[-1,1], sy=[-1,1])
        translate([stack_x + sx*feather_hole_dl/2, stack_y + sy*feather_hole_dw/2, -stack_hang])
            difference() {
                cylinder(d=post_od, h=stack_hang);
                translate([0,0,-1]) cylinder(d=post_pilot_d, h=8);
            }
}

module ear_holes(pilot) {
    for (p = ear_pos) translate([p[0], p[1], 0]) {
        if (pilot) {
            translate([0,0,wall_top_z-12]) cylinder(d=ear_pilot_d, h=13);   // lid screw (top)
            translate([0,0,-1]) cylinder(d=ear_pilot_d, h=11);              // baseplate screw (bottom)
        } else {
            translate([0,0,-1]) cylinder(d=ear_clear_d, h=lid_th+2);
            translate([0,0,lid_th-ear_head_h]) cylinder(d=ear_head_d, h=ear_head_h+1);
        }
    }
}

// ============================================================================
//  MOUNTING BASEPLATE  —  separate part, sized to the pod (NO outboard flange).
//  Sewn to the brace via THREAD ANCHORS: pairs of holes joined by a recessed
//  groove on the TOP face - sew up one hole, across the groove, down the other,
//  into the fabric. Do this BEFORE bolting the pod on; the pod then covers the
//  recessed thread. Pod bolts on with 2 screws up into the end ears; two rails
//  locate it. Print FLAT (see mount_radius); heat-form to the brace if it rocks.
// ============================================================================
anchor_pts = [ [-36,28],[0,28],[36,28], [-36,-28],[0,-28],[36,-28] ];

module thread_anchors() {                     // subtracted from the plate
    for (p = anchor_pts) {
        for (dx = [-1,1])                     // the pair of through-holes
            translate([p[0] + dx*anchor_gap/2, p[1], -plate_sag-1])
                cylinder(d=anchor_hole_d, h=plate_th+plate_sag+2);
        translate([p[0], p[1], plate_th - groove_depth/2 + 0.25])   // recessed top groove
            cube([anchor_gap+anchor_hole_d+3, groove_w, groove_depth+0.5], center=true);
    }
}

module baseplate() {
    difference() {
        union() {
            translate([0,0,-plate_sag])
                rbox(plate_l, plate_w, plate_th + plate_sag, corner_r);
            for (sy = [-1,1])                                   // locating rails
                translate([0, sy*(outer_w/2 + rail_t/2 + 0.5), plate_th + rail_h/2])
                    cube([outer_l*0.8, rail_t, rail_h], center=true);
        }
        // (near-flat) underside; set mount_radius small only if printing a curve
        translate([0,0,-mount_radius]) rotate([0,90,0])
            cylinder(r=mount_radius, h=plate_l+20, center=true, $fn=200);
        // pod mount-screw holes (up into the ear bottom pilots; match ear_pos)
        for (p = ear_pos) translate([p[0], p[1], -plate_sag-1])
            cylinder(d=mount_screw_d, h=plate_th+plate_sag+rail_h+2);
        thread_anchors();
    }
}

// ============================================================================
//  RENDER SELECTOR
// ============================================================================
if (part == "base") base();
else if (part == "lid") lid();
else if (part == "lid_print") translate([0,0,lid_th]) rotate([180,0,0]) lid();
else if (part == "baseplate") baseplate();
else if (part == "assembled") {
    if (show_mount) color("Tan", 0.9) translate([0,0,-plate_th]) baseplate();
    base();
    color("LightSteelBlue", 0.85) translate([0,0,wall_top_z + lip_h]) lid();
}
