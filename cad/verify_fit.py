#!/usr/bin/env python3
"""Check nominal bounds and draw an illustrative enclosure layout.

Dimensions are read from enclosure.scad; this is not a collision solver or a
full-size template. Internal component heights and external GPS placement are
schematic. Run: python3 cad/verify_fit.py
"""
from pathlib import Path
import re
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Patch, Rectangle

CAD_DIR = Path(__file__).resolve().parent
INK, CORAL, BLUE, PURPLE, GREEN, ORANGE = (
    "#25303b", "#cd4e4e", "#2876a8", "#8054a5", "#347b47", "#bd650c"
)


def dimensions():
    """Read the numeric inputs used here; fail if an input becomes an expression."""
    source = re.sub(r"//[^\n]*", "", (CAD_DIR / "enclosure.scad").read_text())
    names = """inner_l inner_w inner_h wall floor lid_th corner_r stack_hang
        stack_envelope proto_l proto_w stack_x stack_y feather_l feather_w
        disp_pkg_l disp_pkg_w disp_lip batt_x batt_y batt_l batt_w batt_h
        switch_x switch_y switch_hole_d gps_cable_x gps_cable_y gps_cable_d
        gps_pcb_l gps_pcb_w usb_w usb_h grommet_y grommet_z grommet_d
        ear_r ear_overlap rail_t""".split()
    d = {}
    for name in names:
        match = re.search(rf"\b{re.escape(name)}\s*=\s*(-?\d+(?:\.\d+)?)\s*;", source)
        if match is None:
            raise ValueError(f"Expected a numeric {name} in enclosure.scad")
        d[name] = float(match.group(1))
    d["outer_l"] = d["inner_l"] + 2 * d["wall"]
    d["outer_w"] = d["inner_w"] + 2 * d["wall"]
    d["wall_top"] = d["floor"] + d["inner_h"]
    d["height"] = d["wall_top"] + d["lid_th"]
    d["ear_x"] = d["outer_l"] / 2 + d["ear_r"] - d["ear_overlap"]
    d["plate_l"] = 2 * (d["ear_x"] + d["ear_r"])
    d["plate_w"] = d["outer_w"] + 2 * (d["rail_t"] + 1.5)
    d["usb_z"] = d["wall_top"] - d["stack_hang"] + 3.2
    return d


def check_fit(d):
    print("NOMINAL ENCLOSURE CHECK — physical dry-fit required")
    print(f"Seated shell: {d['outer_l']:.1f} × {d['outer_w']:.1f} × {d['height']:g} mm")
    print("Excludes ears, baseplate, external GPS and switch lever.")
    for name, x, y, length, width in [
        ("proto hub", 0, 0, d["proto_l"], d["proto_w"]),
        ("Feather", d["stack_x"], d["stack_y"], d["feather_l"], d["feather_w"]),
        ("battery", d["batt_x"], d["batt_y"], d["batt_l"], d["batt_w"]),
    ]:
        margin = min(d["inner_l"] / 2 - abs(x) - length / 2,
                     d["inner_w"] / 2 - abs(y) - width / 2)
        print(f"{name}: {'WITHIN' if margin >= 0 else 'OUTSIDE'} rectangular cavity; "
              f"minimum edge margin {margin:g} mm")
    clearance = d["inner_h"] - d["stack_envelope"] - d["batt_h"]
    print(f"Battery-to-tail clearance: {clearance:g} mm BEFORE any hub, solder, "
          "insulation or wiring below the tail tips.")
    if clearance < 2:
        print("WARNING: nominal clearance below 2 mm; measure the complete assembly.")
    print(f"USB: -X wall, {d['usb_w']:g} × {d['usb_h']:g} mm opening, "
          f"centre y={d['stack_y']:g}, z={d['usb_z']:g} mm.")
    print(f"Switch: {d['switch_hole_d']:g} mm lid hole; confirm body and terminals.")
    print("GPS: external; CAD defines only the cable hole, not board position or screws.")
    print("Unchecked: rounded corners, lid lip, optional mounts, wiring and fasteners.")


def render_plan(out, *, large=False):
    d = dimensions()
    fig, (plan, side) = plt.subplots(1, 2, figsize=(14, 7.3) if large else (12, 6.5))
    fig.subplots_adjust(left=0.025, right=0.985, bottom=0.18, top=0.82, wspace=0.07)
    fs = 11 if large else 9
    for ax in (plan, side):
        ax.set_aspect("equal")
        ax.axis("off")
    fig.suptitle("Armband speedometer enclosure", fontsize=20 if large else 17,
                 fontweight="bold", color=INK, y=0.96)
    fig.text(0.5, 0.90,
             f"Seated shell {d['outer_l']:.1f} × {d['outer_w']:.1f} × {d['height']:g} mm"
             "  ·  excludes ears, baseplate, GPS and switch lever",
             ha="center", fontsize=fs, color=INK)

    def rect(ax, x, y, length, width, color, *, fill=True, ls="-", alpha=0.15):
        if fill:
            ax.add_patch(Rectangle((x-length/2, y-width/2), length, width,
                                   facecolor=color, edgecolor="none", alpha=alpha))
        ax.add_patch(Rectangle((x-length/2, y-width/2), length, width,
                               fill=False, edgecolor=color, lw=1.5, ls=ls))

    def label(ax, x, y, text, color=INK, **kwargs):
        ax.text(x, y, text, color=color, fontsize=fs, ha="center", va="center", **kwargs)

    # Plan: CAD shell and cutout dimensions; GPS placement is illustrative.
    for length, width, color, ls in [
        (d["plate_l"], d["plate_w"], "#957454", "--"),
        (d["outer_l"], d["outer_w"], INK, "-"),
    ]:
        plan.add_patch(FancyBboxPatch((-length/2, -width/2), length, width,
            boxstyle=f"round,pad=0,rounding_size={d['corner_r']}",
            fill=False, edgecolor=color, ls=ls, lw=1.7))
    rect(plan, 0, 0, d["inner_l"], d["inner_w"], "#a0a0a0", fill=False, ls=":")
    rect(plan, 0, 0, d["proto_l"], d["proto_w"], PURPLE, ls="-.", alpha=0.06)
    rect(plan, d["batt_x"], d["batt_y"], d["batt_l"], d["batt_w"], BLUE, ls="--", alpha=0.06)
    rect(plan, d["stack_x"], d["stack_y"], d["feather_l"], d["feather_w"], CORAL)
    rect(plan, d["stack_x"], d["stack_y"], d["disp_pkg_l"]-2*d["disp_lip"],
         d["disp_pkg_w"]-2*d["disp_lip"], CORAL, fill=False, ls=":")
    label(plan, d["stack_x"], d["stack_y"]+2, "display / Feather")
    label(plan, d["stack_x"], d["stack_y"]-4, "hub + battery below", "#606060")
    plan.add_patch(Circle((d["switch_x"], d["switch_y"]), d["switch_hole_d"]/2,
                         fill=False, edgecolor=ORANGE, lw=2))
    label(plan, d["switch_x"], d["switch_y"]+8, "switch", ORANGE)
    gps_x, gps_y = 22, 21  # illustrative only; not a mounting location from CAD
    rect(plan, gps_x, gps_y, d["gps_pcb_l"], d["gps_pcb_w"], GREEN, ls="--")
    label(plan, gps_x, gps_y, "GPS\nexternal", GREEN)
    plan.plot([gps_x, d["gps_cable_x"]], [gps_y-d["gps_pcb_w"]/2, d["gps_cable_y"]],
              color=GREEN, ls=":", lw=1.3)
    plan.add_patch(Circle((d["gps_cable_x"], d["gps_cable_y"]), d["gps_cable_d"]/2,
                         facecolor="white", edgecolor=GREEN, lw=1.7))
    plan.annotate("GPS cable", xy=(d["gps_cable_x"], d["gps_cable_y"]),
                  xytext=(27, -26), ha="center", fontsize=fs, color=GREEN,
                  arrowprops={"arrowstyle": "-", "color": GREEN})
    rect(plan, -d["outer_l"]/2, d["stack_y"], d["wall"], d["usb_w"], CORAL, alpha=0.4)
    label(plan, -d["outer_l"]/2-9, d["stack_y"], "USB", CORAL)
    rect(plan, d["outer_l"]/2, d["grommet_y"], d["wall"], d["grommet_d"], INK, alpha=0.2)
    plan.plot([d["outer_l"]/2+2, 51], [d["grommet_y"]]*2, color=INK)
    label(plan, 48, d["grommet_y"]+7, "LED\nwires")
    for x, y in [(-d["ear_x"], 12), (d["ear_x"], -12)]:
        plan.add_patch(Circle((x, y), d["ear_r"], facecolor="#c7c7c7", edgecolor=INK))
    label(plan, 0, -42, f"Baseplate {d['plate_l']:.1f} × {d['plate_w']:.1f} mm", "#806044")
    plan.set_xlim(-54, 58)
    plan.set_ylim(-48, 43)
    plan.set_title("Plan · looking down at the lid", fontsize=fs+2, loc="left", color=INK)

    # X-Z projection: component bodies are schematic, not measured cross-sections.
    top = d["wall_top"]
    rect(side, 0, d["height"]/2, d["outer_l"], d["height"], INK, fill=False)
    rect(side, 0, top+d["lid_th"]/2, d["outer_l"], d["lid_th"], "#728ca1", alpha=0.25)
    rect(side, d["batt_x"], d["floor"]+d["batt_h"]/2, d["batt_l"], d["batt_h"], BLUE, alpha=0.3)
    label(side, d["batt_x"], d["floor"]+d["batt_h"]/2, "LiPo", BLUE)
    proto_z = top-d["stack_envelope"]  # indicative position; actual hub may extend lower
    rect(side, 0, proto_z+0.8, d["proto_l"], 1.6, PURPLE, alpha=0.5)
    side.annotate("proto hub", xy=(27, proto_z+1.6), xytext=(28, 18),
                  ha="center", fontsize=fs, color=PURPLE,
                  arrowprops={"arrowstyle": "-", "color": PURPLE})
    feather_z = top-d["stack_hang"]
    rect(side, d["stack_x"], feather_z+0.8, d["feather_l"], 1.6, "#62686f", alpha=0.5)
    label(side, d["stack_x"]-1, feather_z+5, "Feather")
    rect(side, d["stack_x"], top-4, d["disp_pkg_l"], 8, CORAL, alpha=0.4)
    label(side, d["stack_x"], top-4, "display", CORAL)
    rect(side, d["switch_x"], top-5, 13, 10, ORANGE, fill=False, ls=":")
    side.plot([d["switch_x"]]*2, [d["height"], d["height"]+7], color=ORANGE, lw=3)
    label(side, d["switch_x"]-3, d["height"]+12, "switch", ORANGE)
    rect(side, gps_x, d["height"]+4.1, d["gps_pcb_l"], 8.2, GREEN, alpha=0.2)
    label(side, gps_x, d["height"]+4.1, "GPS", GREEN)
    rect(side, -d["outer_l"]/2, d["usb_z"], d["wall"], d["usb_h"], CORAL, fill=False)
    label(side, -d["outer_l"]/2-9, d["usb_z"], "USB", CORAL)
    rect(side, d["outer_l"]/2, d["grommet_z"], d["wall"], d["grommet_d"], INK, fill=False)
    side.plot([d["outer_l"]/2+2, 51], [d["grommet_z"]]*2, color=INK)
    label(side, 48, d["grommet_z"]+7, "LED\nwires")
    label(side, 0, -7, "Baseplate omitted from this view", "#606060")
    side.set_xlim(-54, 58)
    side.set_ylim(-13, 68)
    side.set_title("Side projection · component heights schematic", fontsize=fs+2, loc="left", color=INK)

    fig.legend(handles=[Patch(facecolor=color, alpha=0.4, label=label_text) for color, label_text in
               [(BLUE, "Battery"), (PURPLE, "Wiring hub"), (CORAL, "Display / USB"),
                (GREEN, "External GPS"), (ORANGE, "Switch")]],
               loc="lower center", bbox_to_anchor=(0.5, 0.065), ncol=5,
               frameon=False, fontsize=fs)
    fig.text(0.5, 0.025,
             "Illustrative layout, not a scale template. GPS position, component bodies and wiring require a physical dry-fit.",
             ha="center", color="#606060", fontsize=fs)
    fig.savefig(out, dpi=200 if large else 150, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def main():
    check_fit(dimensions())
    out = CAD_DIR / "enclosure_plan.png"
    render_plan(out)
    root_copy = CAD_DIR.parent / "enclosure_plan.png"
    shutil.copyfile(out, root_copy)
    print(f"Updated compatibility copy {root_copy}")


if __name__ == "__main__":
    main()
