# Project Decision Log

This file is the durable record of confirmed dimensions, design choices, and later corrections. Update it whenever a decision is made or revised; do not rely only on conversation history.

## Persistent project rule

- Record every confirmed dimension and design decision in this repository as work progresses.
- Preserve superseded decisions as history, but clearly label them superseded and update the active design brief, parameters, generated metadata, and previews.
- Treat direct physical measurements and fit-test results as authoritative over web specifications or visual estimates.
- Keep `docs/current-design.md` and the root `AGENTS.md` synchronized with every active design change so new sessions load the correct model context immediately.

## Confirmed dimensions

| Item | Confirmed value | Source/status |
|---|---:|---|
| Tablet envelope | 200 x 123 x 8.4 mm | Supplied `tinker.obj` bounding box |
| Existing tube OD | 32.0 mm | User measurement |
| Printed sleeve ID | 32.2 mm | User fit-tested; tight working fit |
| Sleeve body length | 50 mm | Version 1 design value; physical tube availability still to confirm |
| Clear tube engagement | 51 mm | Version 1 design value with 3 mm solid seating cap |
| Sleeve seating cap | 3.0 mm | Version 1 deterministic insertion stop |
| Sleeve wall | 4.0 mm | Version 1 design value |
| Tablet fit allowance | 1.0 mm total X/Y; 0.8 mm Z | Version 1; test coupon required |
| Screen tilt | 10 degrees back from vertical / 80 degrees above horizontal | Corrected user decision; kiosk-like |
| Long-edge relationship | Top is higher and farther from user; bottom is lower and nearer | Confirmed user decision |
| USB-C location | Center of right short edge in landscape | User measurement |
| Plug projection | 0.256 in / 6.50 mm | User measurement |
| Flat cable thickness | 0.6 mm | User measurement |
| Flat cable length | About 2 in / 50.8 mm before braided transition | User measurement |
| Right-angle pigtail reach | 51.4 mm marked length | User photo; precise endpoints still to confirm |
| Downstream connector body | 9.6 mm marked dimension | User photo; axis/meaning still to confirm |
| Round braided cable diameter | 3.45 mm | User measurement; cable after the pictured adapter |
| Retaining screw | M3 | User hardware |
| Power/volume group span | 20–60 mm from landscape top-left | User measurement |
| Power/volume button section | 2 mm wide across tablet thickness, centered; 1 mm edge protrusion | User measurement |

## Active design decisions

- Landscape tablet orientation.
- Simple, sleek, skeletal support rather than a bulky closed enclosure.
- Tablet slides in from the left through narrow long-edge rails.
- A removable left end stop secured by one M3 screw provides retention more secure than snap clips.
- The right edge has a continuous full-depth screen-facing cap backed by internal stops and a solid outer USB-C wall. No tablet-edge or recessed plug-pocket segment is exposed from the front; the low-profile right-angle adapter still turns immediately behind the tablet instead of sending the cable straight out through the right wall.
- The 51.4 mm pigtail and downstream connection remain largely hidden across the open back. The confirmed 3.45 mm braided section snaps into two open rear clips and a rear-facing external sleeve channel, then exits downward near the tube.
- Between the nearer rear clip and sleeve channel, the cable stays in open space: it drops outside the right gusset, passes behind the sleeve, and enters through the channel's rear snap opening. Previewed cable geometry must never cross a holder solid.
- The sleeve channel uses 4.15 mm internal clearance, a 2.8 mm snap opening, and a shallow 1.2 mm embed. It leaves at least 2.8 mm of sleeve wall and does not cut into the tested 32.2 mm tube bore.
- Exposed outside corners are lightly filleted to remove sharp edges without making the skeletal holder bulky.
- The holder installs by sliding a closed 32.2 mm ID sleeve down over the accessible top of the vertical tube.
- With the tablet nearly vertical, the sleeve is centered left-to-right and offset 24 mm behind the screen plane.
- The sleeve/collet bottom is level with the installed holder's lower long edge at Z = -64.53 mm. This lowers the complete rear assembly by 14.53 mm without changing sleeve fit or engagement.
- V2 is the active support-minimized concept. Its main body is a flat-print cradle, a foot-down rear tilt bracket, and a flange-down/bore-up sleeve joined with two adhesive bonds.
- Both V2 glue joints use matching shallow cross grooves and one loose-fit 35 × 15 × 1.8 mm printed key; the alignment-key STL is printed twice because the two keys occupy separate structural joints. The retained grooves provide at least 1.25 mm total planar clearance and 0.50 mm total thickness clearance. The user confirmed that gluing the main body parts is acceptable.
- The bracket carries the two open braided-cable clips so the cradle keeps a completely flat rear print datum.
- The removable V2 end stop retains one M3 screw, now on a local-Z boss outside the tablet cavity so neither the cradle nor stop inherits V1's rear-projecting pad.
- Routine previews use direct in-memory CadQuery tessellation with Trimesh's depth-buffered renderer. Blender is reserved for optional polished presentation renders.

## Revision history

### Power/volume slide-through channel — 2026-08-02

- The user measured the complete landscape-top power/volume group from 20 to 60 mm rightward from the tablet's top-left corner. The buttons are 2 mm wide across the 8.4 mm tablet thickness, centered on that thickness, and protrude 1 mm from the tablet edge.
- Added a 3 mm-high opening centered on the buttons, giving 0.5 mm PLA process clearance above and below. The channel is open at the left rail entrance so the buttons cannot be pressed during insertion and continues 5 mm past the measured seated group end.
- Preserved the continuous screen-facing retaining lip and the lower rail wall outside the button-height band. The channel ends in intact top-rail wall after its 5 mm overrun.
- Added `tablet_stand_v2_button_fit_coupon.stl`, an exact 73.5 × 11 × 14.2 mm crop of the production top-left rail, for physical insertion and seated-clearance testing before a full cradle print.
- Prepared its production-orientation PLA G-code at 0.20 mm layers, three walls, 20% grid infill, and no supports. Validation found 7.5 mm³/s peak flow, a 21 min 51 s estimate, and about 4.8 g of filament; it was not uploaded or started.

### Restore rail allowances and simplify cable opening — 2026-08-02

- The second physical fit test showed that removing the Y/Z allowances was the wrong direction. Restored the original 1.0 mm total X/Y and 0.8 mm Z tablet allowances.
- The cable still could not pass through the T-shaped combination of a 3 × 16 mm slot and 6 × 8.5 mm notch because the original narrow section would not accept the cable's thick portion.
- Replaced the complete T-shaped opening with one rectangular opening that retains the original 16 mm width and spans the full 8 mm pocket depth from the tablet cavity to the outer wall.
- **Superseded by the 2026-08-02 power/volume channel revision:** at this point the top long-edge rail was still continuous and button measurements had not yet been supplied.
- Regenerated and validated the PLA right-side fit-test G-code at 0.20 mm layers, three walls, 20% infill, and no supports. It estimates 1 h 25 min and 18.6 g and was not started.

### Tightened tablet rail fit on both tested axes — 2026-08-02

- The user confirmed that the first PLA right-side coupon was loose both between the two long-edge rails and front-to-back under the retaining lips.
- Reduced total Y allowance from 1.0 mm to 0.0 mm and Z allowance from 0.8 mm to 0.0 mm, using the measured 123 × 8.4 mm tablet envelope directly on both tested rail axes. Preserved the 1.0 mm total X allowance for slide-in length and end-stop tolerance.
- Kept the holder's 130 mm outer Y span fixed. Each long-edge wall grows inward by 0.5 mm, avoiding any change to the outside frame, Z = -64.53 mm lower-edge/sleeve alignment, or already-printed rear bracket and sleeve.
- Started the second PLA right-side test piece after a fresh camera check showed the complete build plate clearly empty. It uses the established 0.20 mm, three-wall, 20% grid, support-free process and is estimated at 1 h 23 min and 18.0 g.
- This is intentionally a physical-test-driven nominal fit; verify that the second PLA coupon slides without force before committing to the full cradle.

### Open cable-body notch from physical coupon test — 2026-08-02 (superseded)

- The user reported that the first PLA right-side coupon fit the tablet reasonably well but the attached right-angle USB-C cable body could not enter the closed rear-turn slot.
- The user's physical test and photo establish an 8.5 × 6 mm required notch. The active design now opens that measured Y × X notch from the tablet cavity into the existing 3 × 16 mm rear pigtail slot.
- Preserved the continuous screen-facing cap, solid outer USB-C wall, 8.0 mm-clear plug pocket, and existing broad flat-pigtail slot. The new notch is confined to the rear pocket floor and provides a lateral installation path for the attached cable.
- Regenerated the PLA coupon G-code with the established 0.20 mm, three-wall, 20% infill, support-free process. The revised validated job estimates 1 h 25 min and 18.7 g; it was prepared but not started.
- The user also reported that tablet retention was slightly loose by about 1 mm on both rail axes; the subsequent fit revision supersedes the original Y/Z allowances.

### Right-side tablet and USB-C fit coupon — 2026-08-02

- Selected a right-end coupon instead of a left/end-stop coupon so one small print tests the uncertain production rail fit and the actual USB-C adapter route together.
- The coupon is an exact X = 78.0–111.5 mm crop of the active V2 cradle, retaining 33.5 mm of both long-edge rails, the full right-side cap and internal stops, the 8.0 mm-clear plug pocket, solid outer wall, and 3 × 16 mm rear-turn slot.
- The coupon preserves the production cradle's rear-face-down print orientation and its 1.0 mm total X/Y and 0.8 mm Z tablet allowances. PLA is the user-selected test material.
- Started the physical coupon on the confirmed Ender-3 Pro profile at 0.20 mm layers, three walls, 20% grid infill, 210 °C PLA / 60 °C bed, and no supports. The unsupported short rails and right-side bridges intentionally reproduce the production cradle's print conditions; the validated G-code estimates 1 h 25 min and 18.8 g.
- A successful physical test requires the tablet to slide without force, seat at the right stop without rocking, accept the USB-C adapter, and let the flat pigtail turn behind the tablet without pinching.

### Loose-fit glue alignment keys — 2026-08-01

- A user PLA+ print test found the original cross keys would not enter their grooves; the prior 0.25 mm total planar allowance was inadequate in the actual process.
- Retained the existing 36.25 × 16.25 × 4.25 mm groove profiles so replacement keys remain compatible with modules that may already be printed.
- Reduced each key to 35 × 15 × 1.8 mm, yielding at least 1.25 mm total in-plane clearance and 0.50 mm total thickness clearance, and added 0.4 mm top/bottom edge relief against first-layer flare.
- Kept two separate keys: one aligns the cradle-to-bracket joint and the other aligns the bracket-to-sleeve joint. The keys locate parts during cure; adhesive carries the finished joints.

### Support-minimized keyed-glue V2 — 2026-07-28

- Evaluated the monolithic V1 main STL in its viable sleeve-vertical orientation. Approximate triangle analysis flagged about 7,700 mm² of downward-facing surface beyond a 45-degree support rule, including the full-width upper rail and the 32.2 mm sleeve-cap ceiling.
- Split the active V2 main structure into a cradle, rear tilt bracket, and sleeve while preserving the 200 × 123 × 8.4 mm tablet envelope, 80-degree screen angle, 32.2 mm tested bore, 51 mm engagement, 3 mm seating cap, 24 mm rear offset, and Z = -64.53 mm sleeve-bottom alignment.
- The cradle prints on a 216 × 137.5 mm rear datum; the bracket prints on a 60 × 28 mm foot; and the sleeve prints upside down on a 60 × 46 mm flange with its tube-entry bore open upward.
- The user confirmed that the main structural parts may be glued. Removed the provisional eight-screw structural scheme and retained only the removable end stop's single M3 screw.
- **Superseded by the 2026-08-01 fit-test correction:** added matching half-depth cross grooves to both glue joints and one 36 × 16 × 2 mm alignment-key STL to print twice. Each groove is 1.15 mm deep with 0.25 mm planar clearance.
- Relocated the two open cable clips to the rear bracket and moved the end-stop screw to a front-accessible local-Z boss outside the tablet cavity.
- All five V2 STL files validate as watertight single components. Approximate flagged overhang area is about 2,870 mm² across all parts, primarily short rail lips, shallow groove roofs, and small clip details rather than tall support towers.

### Fully enclosed right-side face — 2026-07-21

- Replaced the two separated screen-facing right retaining pads and narrow central pocket ceiling with one continuous full-depth cap spanning the entire tablet short edge and plug-pocket depth.
- Preserved the two internal locating walls, solid outer USB-C end wall, 8.0 mm clear plug pocket, and 3 × 16 mm rear pigtail turn slot.
- Neither the tablet's right edge nor the recessed pocket is partially exposed in the front view; cable installation and the left-to-right slide-in path remain unchanged.

### Preserve clips; route between solids — 2026-07-21

- Restored the two open rear C-clips and the external sleeve snap channel after rejecting connector-pass eyelets.
- Corrected only the free cable span: it now drops outside the right gusset, sweeps behind the sleeve with cable-radius clearance, and enters the channel through its rear opening.
- The cable does not pass through the backplate, gussets, sleeve wall, or tube bore.

### Rear sleeve lowered to holder bottom — 2026-07-20

- Lowered the complete sleeve/collet and its external cable channel by 14.53 mm so the sleeve bottom and holder's lower long edge share Z = -64.53 mm in the installed orientation.
- Preserved the 32.2 mm tested bore, 40.2 mm OD, 51 mm clear engagement, 3 mm seating cap, and 24 mm rear offset.
- Extended the two gussets down to the new sleeve position while retaining their original holder-side anchors.
- The open cable span now runs visibly downward and backward from the center rear clips into the lowered sleeve channel; no larger connector is made captive.

### Braided cable channel implemented — 2026-07-20

- Confirmed the cable after the pictured right-angle adapter is 3.45 mm diameter round braided wire.
- Replaced the generated straight-out right-wall groove with a solid outer wall and a 3 × 16 mm rear turn slot for the flat pigtail.
- Added two open rear C-clips and a downward, rear-facing sleeve channel sized to 4.15 mm ID with a 2.8 mm snap opening.
- The sleeve channel embeds only 1.2 mm into the 4 mm sleeve wall, leaving 2.8 mm minimum material over the unchanged 32.2 mm tube bore.
- The larger 9.6 mm-marked connector stays outside every captive feature for installation and service.

### Rear-hidden right-angle cable route — 2026-07-20

- **Superseded:** the V1 straight-out flat-cable groove through the outer right wall.
- **Active intent:** the right-angle adapter wraps immediately behind the tablet; its photo-marked 51.4 mm pigtail and downstream connection stay behind the open back, and the cable then routes to a groove/clip on the sleeve or collet before exiting near the tube.
- The user photo marks 9.6 mm at the downstream connector body, but the measurement axis was not yet confirmed. At this stage the downstream cable diameter and final sleeve exit direction were also still required before changing fit-critical sleeve geometry.
- Prefer open, serviceable rear clips/channel features that do not require feeding the larger connector through a closed tunnel and do not reduce the proven 32.2 mm sleeve bore.

### Closed USB-C end and softened corners — 2026-07-20

- **Superseded:** separated right corner stops with an entirely open center and exposed cable saddle.
- **Active:** the corner stops still locate the tablet, but a closed outer right end encloses the measured 6.50 mm plug projection. Its chamber is open toward the tablet so the cable can be positioned first and the tablet slid onto the connector from the left.
- Version 1 uses 1.50 mm extra plug-depth clearance, giving an 8.0 mm clear pocket, and a provisional 24 mm wide × 1.8 mm high exit groove around the 0.6 mm flat cable. Width remains a required measurement before printing.
- Version 1 rounds exposed wall/rail corners by 1.2 mm and lip corners by 0.8 mm.

### Kiosk-angle correction

- **Superseded:** 10 degrees above horizontal, nearly flat.
- **Active:** 10 degrees back from vertical, equivalently 80 degrees above horizontal, nearly upright like a kiosk.
- The top remains higher and farther from the user than the bottom.
- This correction changes the mount from an underside pedestal junction to a rear-offset sleeve-and-gusset junction.
