#!/usr/bin/env python3
"""Verify the enclosure fits; draw plan + side elevation. Mirrors enclosure.scad.
Run: python3 cad/verify_fit.py
This rev: Feather/display CENTRED on the proto (~+7,-1); switch points UP through
the LID; GPS sits ON TOP of the lid (only a STEMMA cable hole passes through)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

# ---- params (mirror enclosure.scad) ----
inner_l, inner_w, inner_h = 71, 57, 36
wall, floor, lid_th = 2.4, 2.4, 2.6
stack_hang, stack_envelope, proto_below = 22.0, 27.0, 2.0
proto = (0, 0, 64.62, 50.79)         # fills the box, centred
stack = (-7, -4, 51, 23)             # display/Feather: flush-LEFT (USB left), slightly low
disp_win = (-7, -4, 54, 24)          # window 4mm bigger than the display (2mm slop all round)
batt = (0, 4, 62, 37); batt_h = 7.0
switch_xy = (-22, 18); switch_body = (13, 12)   # toggle hangs from the lid (top-left)
gps_cable = (25, -16); cable_d = 6
usb_side = -1   # USB on the -X (left) wall
switch_hole_r = 3.25
outer_l, outer_w = inner_l+2*wall, inner_w+2*wall
ear_r = 4.0; ear_x = outer_l/2 + ear_r - 2.0
ear_pos = [(-ear_x, 12), (ear_x, -12)]
half_l, half_w = inner_l/2, inner_w/2
wall_top = floor + inner_h
usb_y, usb_z = stack[1], wall_top - stack_hang + 3.2

def bnds(c): x,y,l,w=c; return (x-l/2, x+l/2, y-w/2, y+w/2)
def overlap(a,b):
    ax0,ax1,ay0,ay1=bnds(a); bx0,bx1,by0,by1=bnds(b)
    return (max(0,min(ax1,bx1)-max(ax0,bx0)), max(0,min(ay1,by1)-max(ay0,by0)))
def inside(c, clr=0.5):
    x0,x1,y0,y1=bnds(c)
    return (x0>=-half_l+clr and x1<=half_l-clr and y0>=-half_w+clr and y1<=half_w-clr),(x0,x1,y0,y1)

problems, notes, info = [], [], []
v = inner_h - stack_envelope - proto_below - batt_h
(notes if v>=2 else problems).append(f"Vertical clearance battery->proto = {v:.1f}mm (assumes trimmed tails)")
for c,n in [(proto,"proto"),(stack,"display/Feather"),(batt,"battery")]:
    ok,b = inside(c)
    (notes if ok else problems).append(f"{n} {'fits' if ok else 'OUT OF BOUNDS'} (x {b[0]:.1f}..{b[1]:.1f}, y {b[2]:.1f}..{b[3]:.1f})")
sb = (switch_xy[0], switch_xy[1], switch_body[0], switch_body[1])
ox,oy = overlap(sb, stack)
(problems if (ox>0 and oy>0) else notes).append(
    "switch body vs Feather: " + (f"OVERLAP {ox:.1f}x{oy:.1f} - raise switch_y" if (ox>0 and oy>0)
    else "clear (body hangs over the proto, not the Feather)"))
info.append("GPS is EXTERNAL on top of the lid - only its STEMMA cable hole passes through.")
info.append(f"USB-C on the -X (LEFT) wall at z={usb_z:.0f}mm, y={usb_y:.0f}; LED grommet on the +X (right) wall; ears offset to clear both.")

print("="*64); print("ENCLOSURE FIT CHECK (Feather centred / switch + GPS on lid)"); print("="*64)
print(f"External {outer_l:.1f} x {outer_w:.1f} x {floor+inner_h+lid_th:.1f} mm   cavity {inner_l}x{inner_w}x{inner_h}\n")
print("OK / notes:"); [print("  -",n) for n in notes]
print("\nINFO:"); [print("  *",i) for i in info]
print("\nPROBLEMS: none" if not problems else "\nPROBLEMS:"); [print("  !",p) for p in problems]

# ---- draw ----
fig,(axp,axs) = plt.subplots(1,2,figsize=(13,6))
axp.set_aspect("equal")
pl_l, pl_w = 2*(ear_x+ear_r), outer_w+2*(2+1.5)
axp.add_patch(FancyBboxPatch((-pl_l/2,-pl_w/2),pl_l,pl_w,boxstyle="round,pad=0,rounding_size=6",fill=False,edgecolor="#8c564b",ls="--",lw=1.4,zorder=1))
axp.add_patch(FancyBboxPatch((-outer_l/2,-outer_w/2),outer_l,outer_w,boxstyle="round,pad=0,rounding_size=6",fill=False,edgecolor="black",lw=2))
axp.add_patch(Rectangle((-half_l,-half_w),inner_l,inner_w,fill=False,edgecolor="gray",ls=":",lw=1))
def draw(c,ec,fc,label,ls="-",a=0.15):
    x,y,l,w=c
    if fc: axp.add_patch(Rectangle((x-l/2,y-w/2),l,w,facecolor=fc,edgecolor="none",alpha=a,zorder=2))
    axp.add_patch(Rectangle((x-l/2,y-w/2),l,w,fill=False,edgecolor=ec,lw=1.4,ls=ls,zorder=3))
    if label: axp.text(x,y,label,ha="center",va="center",fontsize=7,zorder=5)
draw(proto,"#9467bd","#9467bd","proto (under)",ls="-.",a=0.07)
draw(batt,"#1f77b4","#1f77b4","battery (floor)",ls="--",a=0.10)
draw(stack,"#d62728","#d62728","DISPLAY / FEATHER",a=0.18)
draw(disp_win,"#d62728",None,"",ls=":")
axp.add_patch(Circle(switch_xy,switch_hole_r,facecolor="none",edgecolor="#ff7f0e",lw=2,zorder=4))
axp.add_patch(Rectangle((switch_xy[0]-switch_body[0]/2,switch_xy[1]-switch_body[1]/2),switch_body[0],switch_body[1],fill=False,edgecolor="#ff7f0e",ls=":",lw=1,zorder=3))
axp.text(switch_xy[0],switch_xy[1]+8,"switch (up thru lid)",ha="center",fontsize=6,color="#cc6600")
gps_body = (22, 21, 25.5, 25.4)   # GPS glued on top, top-right (external), above the display
axp.add_patch(Rectangle((gps_body[0]-gps_body[2]/2,gps_body[1]-gps_body[3]/2),gps_body[2],gps_body[3],fill=False,edgecolor="#2ca02c",ls="--",lw=1.2,zorder=2))
axp.text(gps_body[0],gps_body[1],"GPS\n(glued on top)",ha="center",va="center",fontsize=6,color="#2ca02c",zorder=5)
axp.plot([gps_body[0],gps_cable[0]],[gps_body[1]-gps_body[3]/2,gps_cable[1]],color="#2ca02c",ls=":",lw=1,zorder=3)
axp.add_patch(Circle(gps_cable,cable_d/2,facecolor="#2ca02c",edgecolor="k",zorder=4))
axp.text(gps_cable[0]+8,gps_cable[1],"cable hole",ha="center",fontsize=6,color="#2ca02c")
axp.add_patch(Rectangle((-outer_l/2-2,usb_y-5.5),3,11,facecolor="#b00",edgecolor="k",zorder=4))
axp.text(-outer_l/2-4,usb_y,"USB",fontsize=6,color="#b00",va="center",ha="right")
for (ex,ey) in ear_pos: axp.add_patch(Circle((ex,ey),ear_r,facecolor="#9e9e9e",edgecolor="k",zorder=4))
axp.set_xlim(-pl_l/2-12,pl_l/2+16); axp.set_ylim(-pl_w/2-10,pl_w/2+12)
axp.set_title(f"Plan (top view) — pod {outer_l:.0f}x{outer_w:.0f}, plate {pl_l:.0f}x{pl_w:.0f} mm",fontsize=9.5)
axp.axis("off")

axs.set_aspect("equal")
top = wall_top
axs.add_patch(Rectangle((-outer_l/2,0),outer_l,floor+inner_h+lid_th,fill=False,edgecolor="black",lw=2))
axs.add_patch(Rectangle((-batt[2]/2,floor),batt[2],batt_h,facecolor="#1f77b4",edgecolor="k",alpha=0.5)); axs.text(0,floor+batt_h/2,"battery",ha="center",va="center",fontsize=7)
pb = floor+batt_h+2
axs.add_patch(Rectangle((-proto[2]/2,pb),proto[2],1.6,facecolor="#9467bd",edgecolor="k",alpha=0.6)); axs.text(0,pb+3,"proto",ha="center",fontsize=6)
axs.add_patch(Rectangle((-outer_l/2,top),outer_l,lid_th,facecolor="#b0c4de",edgecolor="k"))
axs.add_patch(Rectangle((stack[0]-25,top-8),50,8,facecolor="#d62728",edgecolor="k",alpha=0.5)); axs.text(stack[0],top-4,"display",ha="center",fontsize=6)
fz = top-stack_hang
axs.add_patch(Rectangle((stack[0]-25.5,fz),51,1.6,facecolor="#888",edgecolor="k")); axs.text(stack[0],fz+2.6,"Feather",ha="center",fontsize=6)
axs.add_patch(Rectangle((-outer_l/2-1.5,usb_z-3),3,6,facecolor="none",edgecolor="#b00",lw=2)); axs.annotate(f"USB z={usb_z:.0f}",xy=(-outer_l/2-4,usb_z),fontsize=7,color="#b00",va="center",ha="right")
axs.set_xlim(-outer_l/2-22,outer_l/2+8); axs.set_ylim(-3,top+lid_th+6)
axs.set_title(f"Side elevation — height {floor+inner_h+lid_th:.0f} mm",fontsize=9.5); axs.axis("off")
plt.tight_layout(); plt.savefig("enclosure_plan.png",dpi=130,bbox_inches="tight"); print("\nSaved enclosure_plan.png")
