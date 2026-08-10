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
| Available screw hardware | M3 | User has it, but the active stop is explicitly screw-free |
| Power/volume group span | 20–60 mm from landscape top-left | User measurement |
| Power/volume button section | 2 mm wide across tablet thickness, centered; 1 mm edge protrusion | User measurement |

## Active design decisions

- Landscape tablet orientation.
- Simple, sleek, skeletal support rather than a bulky closed enclosure.
- Tablet slides in from the left through narrow long-edge rails.
- V3 uses a fully enclosed removable left cradle wing instead of a separate cap. Three integral tongues slide +X into closed-back right-wing receivers; one tapered printed cross-wedge locks the lower joint and remains removable for tablet service.
- The right edge has a continuous full-depth screen-facing cap backed by internal stops and a solid outer USB-C wall. No tablet-edge or recessed plug-pocket segment is exposed from the front; the low-profile right-angle adapter still turns immediately behind the tablet instead of sending the cable straight out through the right wall.
- The 51.4 mm pigtail and downstream connection remain largely hidden across the open back. The confirmed 3.45 mm braided section snaps into two open rear clips and a rear-facing external sleeve channel, then exits downward near the tube.
- Between the nearer rear clip and sleeve channel, the cable stays in open space: it drops outside the right gusset, passes behind the sleeve, and enters through the channel's rear snap opening. Previewed cable geometry must never cross a holder solid.
- The sleeve channel uses 4.15 mm internal clearance, a 2.8 mm snap opening, and a shallow 1.2 mm embed. It leaves at least 2.8 mm of sleeve wall and does not cut into the tested 32.2 mm tube bore.
- Exposed perimeter, rail, lip, and stop edges use larger plan radii plus 0.65/0.45 mm longitudinal edge fillets so the print feels softer without becoming bulky.
- The holder installs by sliding a closed 32.2 mm ID sleeve down over the accessible top of the vertical tube.
- With the tablet nearly vertical, the sleeve is centered left-to-right and offset 24 mm behind the screen plane.
- The sleeve/collet bottom is level with the installed holder's lower long edge at Z = -64.53 mm. This lowers the complete rear assembly by 14.53 mm without changing sleeve fit or engagement.
- V3 divides the cradle into two rear-face-down wings joined without glue by three integral tongues and one removable lower cross-wedge. The same 4 × 4 mm locking channel can accept an M3 bolt after the actual head/nut/length dimensions are confirmed.
- The rear bracket bonds only to the fixed right cradle wing so the left wing remains removable. The bracket-to-sleeve bond retains one loose-fit 35 × 15 × 1.8 mm printed alignment key; no adhesive belongs on the removable center joint.
- The bracket carries the two open braided-cable clips so the cradle keeps a completely flat rear print datum.
- Routine previews use direct in-memory CadQuery tessellation with a depth-buffered renderer. The headless fallback uses VTK; Blender is reserved for optional polished presentation renders.

## Revision history

### V3 tongue/receiver coupon fits; support-free wedge layout fails — 2026-08-10

- The user reported major bed-adhesion failure, lifted/stringing extrusion, and poor layer quality in the combined PLA coupon. Even with those defects, the production tongue and receiver pieces fit together. This physically passes their insertion-clearance gate; retain 0.50 mm total root and 1.10 mm total lead clearance.
- Wedge retention strength was not confirmed. The wedge/pin needs support in its current exported orientation: the 7 mm pull head establishes the lowest Z datum while the 3.70 mm root body is centered on the same axis, leaving the body approximately (7.00 − 3.70) / 2 = 1.65 mm above the bed at its root.
- Supersede the support-free combined coupon G-code. Before production, either redesign the wedge so its body and pull head share a flat print datum or slice the wedge separately with removable support. Prefer the common-flat redesign because support scarring would alter a fit surface and this PLA already strings badly.
- Do not change the confirmed tongue or receiver clearances, and do not authorize either full cradle wing until the corrected wedge can be inserted, retain the joint, and be removed without cracking.

### Combined three-piece V3 lock coupon print started — 2026-08-09

- The user explicitly authorized printing all three coupon pieces. Added a reproducible 77.91 × 33.12 × 9.00 mm combined CadQuery plate containing the unchanged production tongue crop, receiver crop, and wedge.
- PrusaSlicer retained the modeled rear-face-down orientation and generated zero support extrusion. The job uses PLA, 0.16 mm layers, three walls, 20% grid infill, a 5 mm brim, 205/200 °C nozzle, 60 °C bed, and 1.0 mm direct-drive retraction at 40 mm/s.
- Independent G-code validation reports a 100 × 46 × 9 mm brim-inclusive footprint, 31m 11s estimated time, about 3.1 g, and 6.2 mm³/s peak flow against the 10 mm³/s machine ceiling. The retained pre-macro heat-order and missing-thumbnail warnings do not affect model motion.
- The printer reported ready and cool after its prior job. A fresh 800 × 600 camera snapshot clearly showed the complete visible plate empty. `tablet_stand_v3_lock_coupon_all3_pla.gcode` was uploaded and the print start was accepted; physical fit and retention results are pending.

### Removable tongue-and-wedge center joint supersedes V3 glue seam — 2026-08-09

- The user rejected permanent cradle glue and selected a screw-free removable middle joint, with existing M3 hardware available only if necessary.
- Replaced the stepped glue seam and three loose adhesive splice keys with a straight center split and three integral +X tongues. The upper/lower tongues are 6 mm tall bed-supported blocks in reinforced receivers; the center tongue stays within the 3 mm rear plate. All receivers have open entrances and closed seating backs.
- Each tongue inserts 18 mm. The close seated/root fit has 0.50 mm total clearance and the tapered lead has 1.10 mm total clearance, derived from the physically successful V2 PLA plug result but enlarged substantially for strength.
- Added one removable lower cross-wedge, tapering from 3.70 to 3.30 mm with a 7 mm pull head. It passes along +Y through an aligned 4 × 4 mm channel in the lower tongue and receiver. The channel's 4 mm ceiling is within the confirmed support-free PLA bridge rule.
- The same channel clears an M3 shaft for a bolt/washer/nut fallback. Do not finalize metal hardware pockets until the user's exact M3 head style, length, washer, and nut dimensions are measured.
- The left wing is now 125.00 × 135.50 × 14.20 mm and the right wing 111.33 × 139.00 × 14.20 mm; both are single watertight solids and remain comfortably inside the 220 mm bed.
- Validation confirms zero intersection at seven left-wing insertion positions, no seated wing overlap, a collision-free wedge insertion path, retained button/USB-C geometry, a continuous integral left wall, and watertight production/coupon exports.
- The rear bracket bonds only to the fixed right wing and merely contacts the removable left wing. The bracket-to-sleeve bond keeps one printed alignment key. This makes the tablet serviceable without disturbing the tube mount.
- Exported exact lower-joint left, right, and wedge coupons. A physical coupon test is required before slicing either full cradle wing; do not infer final wedge retention from CAD alone.
- Added a combined `lock_coupon_all3` print-plate export containing one unchanged copy of each coupon component. The three islands have more than 10 mm edge clearance so a 5 mm brim does not join them; this is the authorized single-job layout for the physical test.

### V3 splits the near-bed-width cradle into two printable wings — 2026-08-09 (adhesive joint superseded later the same day)

- The user requested another modeling approach after the full V2 cradle measured 215 mm wide on the 220 mm Ender-3 Pro bed, then authorized a V3 concept for visual review.
- The first V3 render incorrectly retained the separate V2 end cap even though the two-piece cradle itself provides the tablet-loading split. The user rejected that redundancy. V3 now has one continuous rounded left wall integrated into the left wing, and no separate end cap, tapered plug, socket, receiver bulge, screw, or nub.
- V3 assembly now seats the tablet in the USB-C/right wing first, brings the enclosed left wing onto the long edges, and joins the two wings at the center seam. Adhesive assembly captures the tablet, so serviceability must be explicitly accepted before bonding.
- Split the exact tested cradle geometry along a 0.35 mm-clearance stepped planar seam. The seam runs at X = −8 mm near both long rails and X = +8 mm through the center, creating a 16 mm dogleg at Y = ±35 mm without an undercut, trapped support, or tall print orientation.
- The corrected fully enclosed left wing validates at 114.83 × 130.00 × 14.20 mm and the right wing at 119.33 × 130.00 × 14.20 mm. Both are single watertight solids, print rear-face-down, and leave generous margin on the confirmed 220 × 220 mm bed.
- Added three identical 44 × 6 × 1.6 mm loose splice keys in 46 × 7.2 × 1.9 mm rear recesses. One bridges each long rail and one bridges the center spine; all sit 0.20 mm below the rear face. The existing 74 × 36 mm rear bracket also spans and bonds across the center seam.
- Preserve the tested tablet allowance, concealed button groove, open USB-C cable rectangle, tube sleeve, cable route, and exposed fillets. The successful twin tapered coupon remains historical V2 fit evidence but that joint is intentionally absent from corrected V3. V3 is rendered and validated but not yet sliced or approved for printing.
- Keep V2 only as the exact geometry basis during this comparison. If the V3 visual review passes, promote V3 and archive the V2-only workflow rather than maintaining two production versions.

### Twin tapered plug/socket coupon passes — 2026-08-09 (V2 evidence; superseded in V3)

- The user physically tested the tightened rev3 plug against the already-printed enlarged socket and reported that the fit was great. This passes the twin-plug mechanical fit gate for the active screw-free left cap.
- Keep the 0.45 mm total root and 0.85 mm total tip clearances. No further fit-coupon geometry change is needed before production slicing.
- The later V3 split-cradle decision removes the separate cap, plugs, and sockets entirely. Keep this result only as V2 process/fit history; do not reuse any pre-V3 full-part G-code.

### Slightly tighten the successful enlarged socket fit — 2026-08-05

- The enlarged socket and thicker plug fit reliably in the user's PLA, but the user reported slight looseness. Retain the printed socket and tighten only the plug so no second socket print is needed.
- Increase the plug from 2.40 × 3.20 mm at the root / 2.00 × 2.80 mm at the tip to 2.55 × 3.35 mm / 2.15 × 2.95 mm. This targets 0.45 mm total root clearance and 0.85 mm total tip clearance while remaining materially larger than the broken first plug.
- Prepare and validate a plug-only coupon. The revised G-code validates at about 6 min 0 s, 0.3 g, 5.7 mm³/s peak flow, and no support or bed-clearance errors apart from the profile's generic heat-order and thumbnail warnings. Do not print the full cap until this intermediate fit is confirmed.

### Loosen and strengthen twin-plug fit after PLA coupon failure — 2026-08-05

- The user physically tested the first socket/plug pair. It was too tight to seat reliably in the actual PLA, and the small tapered plug broke during fitting. This physical result supersedes the prior 0.25 mm total root-clearance target.
- Enlarged the socket from 2.40 × 3.20 mm to 3.00 × 3.80 mm and enlarged the plug from 2.15 × 2.95 mm at its root / 1.80 × 2.60 mm at its tip to 2.40 × 3.20 mm / 2.00 × 2.80 mm. The new total root clearance is 0.60 mm, with 1.00 mm total tip clearance.
- Increased receiver reinforcement to 5.8 mm across Y and 6.8 mm across Z while preserving at least 1.3 mm of surrounding material. The cradle envelope becomes 215 × 135.6 × 14.8 mm and remains within the confirmed 220 × 220 mm bed.
- Regenerate and physically test the replacement socket and plug coupon before slicing or printing the full cradle/cap. Do not reuse the previous coupon pieces as final fit references.

### Twin tapered rail plugs replace the failed dovetail — 2026-08-04

- The supported dovetail coupon physically failed its serviceability goal: support could not be removed reliably from the narrow captured groove. The user selected twin tapered plugs as the replacement screw-free joint.
- Added one horizontal plug and socket at each long-edge rail. Each 12 mm plug tapers from 2.15 × 2.95 mm at its root to 1.80 × 2.60 mm at its tip; each socket is 2.40 × 3.20 mm with 0.25 mm total root and 0.60 mm total tip clearance.
- Both plug and socket use a house-shaped cross-section. Vertical walls and a two-face 45-degree roof eliminate unsupported flat fit surfaces, while 45-degree underside ramps blend the reinforced socket bodies into the cradle.
- Preserved the concealed 2 mm-high × 1.2 mm-deep top button groove, solid 1.8 mm outer rail wall, rounded cap, and absence of screws, hooks, detents, or a lower nub.
- Validation confirms both seating ends, minimum 1.2/1.3 mm receiver walls, zero intersection at six horizontal insertion positions, watertight production/coupon STLs, and a 215 × 133.6 × 14.2 mm cradle envelope. The multiview and exact coupon preview were regenerated and inspected.
- Prepared the exact socket and plug coupons as separate support-free jobs for the user's string-prone PLA: 0.16 mm layers, three walls, 20% grid, 5 mm brim, 205/200 °C, and 1.0 mm retraction at 40 mm/s. They validate at about 19 min 23 s / 1.0 g and 5 min 44 s / 0.3 g without model-stability warnings.
- All previous full-cradle, supported-cradle, combined-coupon, and end-stop G-code is stale. A physical twin-plug fit test is required before regenerating the complete cradle and cap slices.

### Sleek dovetail stop and clean lower-left corner — 2026-08-03 (superseded 2026-08-04)

- The user rejected the first screw-free implementation's visible landing nub, small rear hooks, and detent bumps in favor of a sleek tongue-and-groove joint like the supplied reference image.
- Replaced the separate hooks and detents with one continuous top-entry dovetail. Its cradle groove has a 1.30 mm mouth and 2.30 mm internal head; its stop tongue has a 1.80 mm head, producing 0.25 mm mechanical capture per side and 0.50 mm total sliding clearance at the head.
- Closed the groove internally at Y = −54.5 mm to establish the seated position without an external ledge. Removed the entire lower landing/nub and restored the cradle envelope to 215 × 130 × 14.2 mm.
- Rounded the stop's outside plan corner to 1.70 mm and its exposed edges to 0.70 mm, preserving the clean continuous lower-left outline.
- Sampled the complete top-down insertion path at thirteen offsets from 130 mm to fully seated; every position has zero solid intersection. The cradle, stop, and exact two-piece coupon remain watertight.
- Updated ADR-0002 as an implementation refinement: the accepted screw-free guided-slide decision remains, while its former landing/hook/detent implementation is superseded.
- Regenerated the two-piece left-slide PLA coupon with a 5 mm removable brim and no supports; validation reports 33 min 13 s, about 5.8 g, and 7.6 mm³/s peak flow. It was not uploaded or started.
- Regenerated the full-cradle support review. The recommended support-free job validates at 4 h 8 min, 60.7 g, and X = 3–217 mm; the snug-support comparison validates at 4 h 28 min, 67.4 g, and places support on the long lips and end features. Neither was uploaded or started.
- Prepared the separate end stop bridge-face down with a 5 mm brim and no supports; validation reports 49 min 22 s and 9.2 g. It was not uploaded or started.

### Supported left-slide coupon retry for string-prone PLA — 2026-08-03 (superseded 2026-08-04)

- The first physical two-piece left-slide coupon failed as a print: the stop crop developed loose/collapsed extrusion beneath its ledge and the shared job showed severe travel stringing. This result does not establish dovetail fit and overrides the earlier support-free slice recommendation.
- Kept the exact production tongue, groove, closed bottom, and fit clearance unchanged. Rotated the stop onto its broad outside wall face so its dovetail builds vertically; this changes only manufacturing orientation, lowers the full stop from 14.2 mm to about 6.8 mm, and increases its estimated bed contact from 803 mm² to 1,778 mm². Increased the combined plate's inter-part spacing from 10 mm to 28 mm, leaving an 18 mm clear gap between separate 5 mm brims.
- The retry uses 45-degree grid supports, a cooler 200 °C nozzle after a 205 °C first layer, and slower external/perimeter motion for the user's confirmed dry but string-prone PLA. The full cradle and end-stop G-code remain unapproved pending a successful physical coupon.
- The validated retry uses 0.16 mm layers, three walls, 20% grid infill, 45-degree grid supports with 0.2 mm Z / 0.4 mm XY gaps, a 5 mm brim, 1.0 mm retraction at 40 mm/s, 25 mm/s external perimeters, and 30 mm/s perimeters. It estimates 40 min 49 s and 5.0 g with 7.5 mm³/s peak flow; actual support paths were rendered and visually inspected before upload.
- Started the corrected coupon after printer status reported ready/complete and a fresh camera image clearly showed the visible build plate empty. Moonraker confirmed the uploaded file's 0.16 mm layers, 205/200 °C temperatures, 14.2 mm height, and 2,449 s estimate before the job entered `printing` and began heating the bed to 60 °C.

### Screw-free slide stop and softened outside edges — 2026-08-02 (joint geometry superseded 2026-08-03)

- The user rejected the M3 hole and requested a left edge that simply slides downward, seats on a projecting lower-left cradle edge, stays through friction, and can optionally receive a drop of glue.
- Removed the complete M3 boss, pilot, stop tab, and clearance hole. Added a 7 × 5.5 × 3 mm lower landing, a 4 mm rail-free insertion lead, two 6 mm friction ribs with 0.05 mm nominal insertion interference, matching 6.4 mm detent grooves, and two rear hooks with 0.20 mm clearance below the cradle datum.
- Sampled the stop throughout its local −Y insertion path. Hard geometry remains collision-free; only the intended friction ribs overlap the base edge during travel, at no more than 0.60 mm³ combined, and the fully seated stop has zero overlap.
- Increased exposed plan-corner radii from 1.2 to 1.45 mm on rails/walls and from 0.8 to 0.95 mm on lips. Added 0.65 mm perimeter/rail edge fillets and 0.45 mm lip edge fillets to remove the sharp longitudinal edges reported on the physical print.
- Added two exact production-crop STLs for testing the landing, hook clearance, downward travel, and friction detents before printing the revised 217 × 135 mm cradle.
- ADR-0002 supersedes the M3 clause in ADR-0001 while retaining the four-module support-minimized architecture. The previous full-cradle G-code predates this geometry and is invalid for production.
- Prepared both coupon pieces on one 33.75 × 50 mm plate with a removable 5 mm brim, three walls, 20% grid infill, and no supports. The validated PLA job estimates 38 min 41 s and 6.1 g; it was not uploaded or started.
- Replaced the stale cradle G-code with revised slices. The recommended support-free job validates at 4 h 34 min, 61.1 g, and X = 2–218 mm extrusion; the snug-support comparison validates at 4 h 52 min and 66.8 g but contacts the long rail lips and right-end features. Neither was uploaded or started.

### Archive superseded V1 from the active tree — 2026-08-02

- The user confirmed that V1 is superseded and should no longer consume maintenance or review effort.
- Removed the generated `build/v1/` artifacts, V1 validator, V1 preview entrypoint, and legacy Blender renderer from the active working tree. The complete prior state remains recoverable at Git commit `560c6e8`.
- Renamed and trimmed the former shared source into `cad/tablet_stand_core.py`, which now contains only active measured parameters plus the cradle and sleeve geometry required by V2. V2 no longer imports a module named for V1.
- Reduced the mandatory model workflow to the three active V2 build, validation, and direct-preview commands.

### Full cradle PLA slice and support review — 2026-08-02

- The user authorized preparation of the full tablet-holder print but required visual review of the slice and supports before any printer upload.
- Kept the cradle on its production rear-face datum. Standing it vertically would fit the conservative 210 mm safe envelope but create extensive support, a 216 mm-tall weak print, and poorer rail dimensional fidelity.
- The 216 mm cradle fits the configured 220 mm bed at X = 2–218 mm only after disabling the profile's optional 6 mm skirt. The no-support candidate validates at 4 h 39 min, about 61.8 g, and 7.5 mm³/s peak flow.
- Generated a snug 45-degree support comparison. It adds about 29 minutes and 9.4 g, reaches the complete X = 0–220 mm span, and places support along the long retaining rails and right-end features.
- Selected the support-free slice as the recommended candidate because production-orientation coupons already validated the short unsupported rail geometry, while supports consume all bed margin and contact fit-critical surfaces. Neither slice was uploaded or started.
- Added `scripts/render_gcode_support_preview.py` and `tablet_stand_v2_cradle_support_review.png` to visualize actual PrusaSlicer model paths in blue and support paths in orange.

### Concealed 2 mm internal button groove — 2026-08-02

- The user rejected the exposed through-slot: the power/volume relief must be a small internal channel rather than an opening through the top rail's outer face.
- Replaced the prior 3 mm through-slot with a 2 mm-high × 1.2 mm-deep groove in the rail's inner face, centered on the measured buttons. The groove clears their 1 mm projection with 0.2 mm depth allowance.
- Preserved a continuous 1.8 mm exterior wall, above the 1.26 mm recommended PLA wall for the confirmed 0.4 mm-nozzle process, plus the complete screen-facing retaining lip.
- Kept the groove open only at the left slide-in entrance and continued it 5 mm beyond the measured seated button group so the insertion path remains unobstructed without exposing the channel on the outside of the holder.
- Regenerated the production-orientation PLA coupon G-code at 0.20 mm layers, three walls, 20% grid infill, and no supports. Validation found 7.5 mm³/s peak flow, a 23 min 20 s estimate, and about 5.3 g of filament; it was not uploaded or started.

### Power/volume slide-through channel — 2026-08-02 (superseded)

- The user measured the complete landscape-top power/volume group from 20 to 60 mm rightward from the tablet's top-left corner. The buttons are 2 mm wide across the 8.4 mm tablet thickness, centered on that thickness, and protrude 1 mm from the tablet edge.
- Added a 3 mm-high opening centered on the buttons, giving 0.5 mm PLA process clearance above and below. This exposed through-slot was rejected and replaced by the concealed 2 mm internal groove above.
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
