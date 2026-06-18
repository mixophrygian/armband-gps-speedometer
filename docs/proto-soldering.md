# Proto Board Soldering Walkthrough

This is the bridge between the bench bring-up and the enclosure. You finished
`bench-bringup.md` with everything working on a breadboard with jumper wires.
This doc moves that exact circuit onto a **perma-proto board** as a permanent
wiring hub, using **long wires** so the box can be decided later. Nothing here
forces an enclosure decision.

Read this all the way through before heating the iron.

## The one big idea: a perma-proto is a soldered breadboard

An Adafruit perma-proto has the **same pre-connected layout as a breadboard**:

- Each **row** (the 5 holes on one side of the center channel) is one connected
  node. The two halves of a row are separated by the center channel.
- The strips along the long edges are the `+` and `-` **power rails**.

So the move is simple: **recreate the wiring you already had on the breadboard —
same rows, same rails — and solder it down.** Parts in the same row are already
joined; you only add a wire when two *different* rows (or a row and a rail) need
to connect.

This doc assumes the **half-size** perma-proto with `+`/`-` rails you have. (If
you ever use a plain perfboard with no rails, see the footnote at the end — you
build the rails yourself.)

## What changes and what doesn't

| Part | On the breadboard now | After this doc |
| --- | --- | --- |
| Feather + display stack | tails in breadboard | tails soldered into the perma-proto |
| 330 ohm resistor | breadboard | soldered to the perma-proto |
| DPDT switch | jumpers to breadboard | long wires soldered to the perma-proto |
| LED lane | jumpers to breadboard | hardwired 3-conductor cable soldered to the perma-proto |
| GPS (PA1010D) | STEMMA QT plug | **unchanged — stays a plug into the Feather** |
| LiPo battery | JST-PH plug | **unchanged — stays a plug into the Feather** |
| 100 uF capacitor | (you never installed one) | **optional; if added, on the armband — see `wiring.md`** |

The GPS and battery never touch the perma-proto. They plug into the Feather's own
connectors and stay fully detachable, so the GPS can live outside the box.

## Assumptions (tell me if any are wrong)

1. **Board:** Adafruit perma-proto, half-size, with `+`/`-` rails.
2. **Feather attach:** the Feather's stacking-header **tails are soldered
   directly into the perma-proto rows.** If you want it removable, solder female
   headers in and plug the Feather into those instead — but that adds ~8 mm of
   height, tight in the pod. This doc assumes direct solder.
3. You are using the **330 ohm** data resistor confirmed in `bom.md`.

## Tools and materials

- Soldering iron (~350 C / 650 F) with a clean, tinned tip
- Rosin-core solder (60/40 leaded is easiest to learn on; lead-free is fine)
- Flush cutters and wire strippers
- **Stranded silicone wire, 22-26 AWG**, in at least three colors (red `+`,
  black `GND`, a third for data) — cut these **long**, trim later
- A couple of short jumper wires (for row-to-rail hops)
- Heat-shrink tubing + a heat source
- Helping hands or a board vise
- **Multimeter** with continuity (beep) mode — not optional for this

## Soldering primer (read if you've never done this)

- **A good joint:** touch the iron to the pad *and* the lead at the same time for
  ~1 second, then feed solder into the joint (not onto the iron tip). It flows
  and forms a small shiny cone. Solder away, then iron away. ~1-2 seconds total.
- **Cold joint** (dull, blobby, ball sitting on top): reheat, add a touch of
  solder/flux.
- **Bridge** (solder accidentally spanning a row into the next row): wick it off
  or drag it away with the hot tip. Eyeball the underside every few joints.
- Remember the row is *already* connected end to end — you don't need to solder
  every hole in a row, just the one your part/wire sits in.

## The node map (your wiring target)

Six nodes. On a perma-proto a "node" is **a row or a rail**. Keep this next to
you; the final test checks against it.

| Node | What lands on it |
| --- | --- |
| **D6** | Feather `D6` tail + resistor leg 1 (same row = joined) |
| **DATA** | resistor leg 2 + LED cable **data** wire (out to lane `DIN`) |
| **EN** | Feather `EN` tail + switch **pole 1 common** wire |
| **BAT** | Feather `BAT` tail + switch **pole 2 ON-throw** wire |
| **LEDV** | switch **pole 2 common** wire + LED cable **`+`** wire |
| **GND rail** | Feather `GND` tail + switch **pole 1 OFF-throw** wire + LED cable **`GND`** wire |

Switch lugs left **empty**: pole 1 ON-throw and pole 2 OFF-throw.

```text
 row D6   : Feather D6  ===[ 330R ]=== row DATA --> LED cable data --> lane DIN
 row EN   : Feather EN  ------------------------- switch pole1 COMMON
 row BAT  : Feather BAT ------------------------- switch pole2 ON
 row LEDV : switch pole2 COMMON --+--- LED cable + --> lane +
 - rail   : Feather GND --+--- switch pole1 OFF
                          +--- LED cable GND --> lane GND
```

---

## Stage 0: Plan the layout (no soldering)

1. Unplug USB and the LiPo. Set the GPS aside.
2. Dry-fit the Feather (display still stacked) so its two header rows **straddle
   the center channel**, tails into the holes — exactly like on the breadboard.
3. Find the rows its key pins land in: **`D6`, `BAT`, `EN`, `GND`** (the Feather
   pins are silkscreened — `6` is D6). Note them.
4. Pick the **`-` rail** nearest the Feather `GND` row as your GND bus.
5. Pick an empty row next to `D6` for **DATA**, and an empty row for **LEDV**.
6. Plan where the long wires exit (switch wires + the 3-wire LED cable) — toward
   where the cable will leave the future box.
7. Lift the Feather back out. Low-profile parts go in first while the board is
   clear and flat.

Success: you can point to the rows for D6, DATA, EN, BAT, LEDV, and the `-` rail.

## Stage 1: Solder the low-profile parts (Feather out)

1. **Resistor:** bend its legs flat. Put leg 1 in any hole of the **D6 row** and
   leg 2 in the **DATA row**. Solder both, flush-cut the leftover legs. (No
   polarity.) Because the D6 row is one node, the resistor is now joined to
   wherever the D6 tail will land — no extra wire needed.
2. **GND row -> `-` rail jumper:** short wire from any hole of the Feather `GND`
   row to the `-` rail. Solder both ends. Now Feather ground reaches the bus.

Success: resistor bridges D6 row -> DATA row; the GND row beeps to the `-` rail.

## Stage 2: Solder the Feather into the board

1. Reseat the Feather, tails through their rows, straddling the center channel.
   Confirm `D6` lands on the resistor's row and `GND` on the bussed row.
2. **Tack one corner tail,** check the Feather is flat and square, reheat/nudge
   if tilted.
3. Solder the rest of the tails one at a time. At minimum **`D6`, `BAT`, `EN`,
   `GND` plus the four corners** for strength; soldering all that reach holes is
   sturdier. Watch for bridges into neighboring rows.

Success: Feather is rigid, no tilt, no bridged rows.

> The display is stacked on top; soldering the tails underneath won't hurt it.
> Don't dwell on any one pin more than a couple seconds.

## Stage 3: Solder the long switch wires

Cut four wires **long** (reach the switch wherever it lands in the box, plus a
service loop). If the switch already has pigtails from the bench test, solder
their free ends to the board instead.

1. **Pole 1 common -> EN row.**
2. **Pole 1 OFF-throw -> `-` rail.**
3. **Pole 2 common -> LEDV row.**
4. **Pole 2 ON-throw -> BAT row.**
5. Leave pole 1 ON-throw and pole 2 OFF-throw **empty.**
6. Heat-shrink each switch-lug joint so adjacent lugs can't touch.

If unsure which lug is which, redo the common/throw multimeter check from
`bench-bringup.md` Stage 8 before soldering.

Success: four wires run board->switch; two lugs empty; lug joints insulated.

## Stage 4: Solder the hardwired LED cable

The 3-conductor cable that leaves the pod and runs to the armband lane. Cut it
**long** with extra service slack. Colors: red `+`, black `GND`, third = data.

1. **Data wire:** **DATA row** -> lane **`DIN`** pad.
2. **`+` wire:** **LEDV row** (shares the row with the switch pole-2 common wire)
   -> lane **`+`** pad.
3. **`GND` wire:** **`-` rail** -> lane **`GND`** pad.
4. Heat-shrink every joint at the lane end. Strain-relieve the cable at the lane
   end now; the pod-wall strain relief waits for the enclosure.

> A 100 uF cap is optional for this build (you've run fine without one). If you
> add it, it goes across the lane's `+` and `GND` **at the armband**, polarity
> observed — see `wiring.md`. Not on this board.

Success: three wires run board->lane; lane joints insulated and strain-relieved.

## Stage 5: Continuity test before any power

Multimeter on continuity. LiPo and USB disconnected. Check every node connects
and nothing shorts:

- D6 -> resistor -> DATA -> LED data wire: ~330 ohm end to end (not a beep).
- Feather GND -> `-` rail -> switch pole-1 OFF-throw -> LED GND wire: all beep.
- Feather BAT -> switch pole-2 ON-throw: beep.
- Feather EN -> switch pole-1 common: beep.
- LEDV (switch pole-2 common) -> LED `+` wire: beep.
- **Critical short check:** BAT to GND must **NOT** beep (switch ON or OFF).
  LEDV to GND must not beep. D6 to GND must not beep.

Then exercise the switch:
- **ON:** EN to GND should **not** beep (EN floats high = Feather on); BAT to
  LEDV **should** beep (LED power connected).
- **OFF:** EN to GND **should** beep (Feather disabled); BAT to LEDV should
  **not** beep (LED power cut).

Success: every node connects, no power-to-ground short, switch flips both
behaviors. **Do not power up until this passes.**

## Stage 6: Power-up smoke test

1. Plug the GPS back into the Feather's STEMMA QT.
2. Plug in the LiPo, then USB.
3. Same as `bench-bringup.md` Stage 9 — confirm the boot sweep, then the
   no-fix / normal / stale LED states and the mph display behave exactly as they
   did on the breadboard. Take it outside for a fix.

If something changed from the breadboard:
- A state that worked before now fails -> suspect a cold joint or a bridge on
  that node. Reflow it and re-run the Stage 5 checks.
- Nothing lights / no display -> recheck the GND rail jumper and Feather GND.
- LEDs dead but display fine -> recheck LEDV/switch pole 2 and the data path.

Success: identical behavior to the end of bench bring-up, now on a solid board.

## What is still deferred to the enclosure

You have committed only the *electrical* build. Still open, and fine to leave so:

- Where the switch bushing pokes through a wall (mount it from inside later).
- Where the LED cable exits (a slit/grommet, cut later).
- Mounting the board stack and padding the LiPo.
- The USB-C and GPS openings.
- Cable strain relief at the pod wall.

Keep all the long wires coiled with service loops until then.

---

## Footnote: plain perfboard (no rails)

If you ever build this on a plain perfboard instead, the difference is that
**nothing is pre-connected** — every hole is isolated. Then:

- Build the **GND bus yourself**: lay a bare wire across a line of holes and
  solder each, and use that everywhere this doc says "`-` rail."
- Each node that this doc gets "for free" from a shared row must be made by a
  short wire on the underside (e.g. D6 blob -> resistor leg). The Feather's
  soldered pins give you an underside solder blob per pin to wire from; more than
  one wire can share one blob.

Everything else — the node map, the stage order, the tests — is identical.
