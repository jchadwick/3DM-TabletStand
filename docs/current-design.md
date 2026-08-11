# Current Design Specification

## Purpose and status

The project is a simple, sleek, FDM-printable landscape holder for a 2024 onn. 8-inch tablet. It mounts permanently to the accessible top end of a vertical 32 mm OD tube. V3 is the active split-cradle candidate: its physical tongue/receiver coupon fit despite severe print defects, and the corrected wedge retained and released successfully. V3 preserves the tested tablet, button, USB-C, tube, and cable interfaces while replacing both the 215 mm-wide cradle print and separate left cap with two bed-friendly wings. Superseded V1 is archived only in Git history at commit `560c6e8` and is not maintained.

## Orientation and coordinates

The user views the tablet in landscape. The screen faces the user; the bottom long edge is lower and nearer; the top long edge is higher and farther away. The screen is **10 degrees back from vertical**, which is **80 degrees above horizontal**. Do not reintroduce the superseded nearly-flat 10-degrees-above-horizontal interpretation.

In the CadQuery model, X runs left (−) to right/USB-C side (+), Y runs user/bottom (−) to far/top (+), and Z runs up. The tablet plane is rotated +80 degrees about X.

## Fit-critical dimensions

| Feature | Value | Status |
|---|---:|---|
| Tablet envelope | 200 × 123 × 8.4 mm | Measured from supplied OBJ |
| Tablet allowance | 1.0 mm total in X/Y; 0.8 mm in Z | Restored after the zero-nominal Y/Z fit test proved too tight |
| Existing tube | 32.0 mm OD | User measurement |
| Sleeve ID | 32.2 mm | User fit-tested; preserve |
| Sleeve OD / wall | 40.2 mm / 4.0 mm | Active design value |
| Sleeve body / engagement | 50 mm / 51 mm | Active design value |
| Seating cap | 3.0 mm | Deterministic tube stop |
| Sleeve rear offset | 24 mm | Keeps tube out of tablet cavity |
| Sleeve vertical placement | Bottom level with holder's lower long edge (Z = -64.53 mm) | User-requested alignment; rear assembly lowered 14.53 mm |
| V3 center retention | One removable printed tapered cross-wedge through the lower tongue/receiver | No cradle adhesive or screw required; the same 4 × 4 mm channel accepts an M3 bolt, washers, and nut as a fallback after hardware dimensions are confirmed |
| USB-C plug projection | 6.50 mm | User measurement |
| Flat cable thickness / length | 0.6 mm / about 50.8 mm | User measurement |
| Right-angle pigtail reach | 51.4 mm | Marked on user photo; endpoint definition should be confirmed before a close fit |
| Downstream connector body | 9.6 mm marked dimension | User photo; measurement axis/meaning still to confirm |
| Round braided cable diameter | 3.45 mm | User measurement |
| USB-C plug-pocket depth | 8.0 mm clear | 6.50 mm projection plus provisional clearance |
| Rear cable opening | 16 × 8 mm (Y × X) open rectangle | Replaces the undersized T-shaped slot/notch; spans the full pocket depth from tablet cavity to outer wall |
| Power/volume group | 20–60 mm from landscape top-left; 2 mm wide across tablet thickness; centered; 1 mm edge protrusion | User measurements |
| Top button channel | Concealed internal groove, 2 mm high × 1.2 mm deep; runs from left slide-in end through 5 mm beyond the seated button group | Clears the 1 mm button projection while preserving a solid 1.8 mm exterior rail wall and continuous retaining lip |
| Braided-cable channel | 4.15 mm ID / 2.8 mm snap opening | 0.70 mm total clearance around confirmed cable diameter |
| Sleeve channel embed / remaining wall | 1.2 mm / 2.8 mm minimum | Keeps the 32.2 mm tube bore intact |
| Exposed finish | Front-frame opening follows the supplied tablet's approximately 7.0 mm plan corner radius; outer frame radius is now 28.0 mm for a pronounced soft silhouette; continuous top/bottom edge rails shroud the rear joiners while keeping the screen-facing perimeter straight; rails/walls use 1.45 mm plan corners and 0.70 mm edge fillets; lips use 1.05 mm plan corners and 0.60 mm edge fillets | Rounded to match the tablet silhouette and soften the visible holder |
| V2 main-body split | Cradle, rear tilt bracket, sleeve | Separates conflicting print axes |
| Structural glue alignment | 35 × 15 × 1.8 mm cross key, print quantity 1 | Used only for the unchanged rear-bracket-to-sleeve bond; the bracket bonds to the fixed right wing without a cradle key, and the removable left wing receives no adhesive |
| Cradle-to-bracket bond | 74 × 36 mm nominal mating face | Align matching side and top edges |
| Bracket-to-sleeve bond | 60 × 28 mm nominal mating face | Align matching side and front edges |
| V2 left cap (historical) | Horizontal local +X insertion on two enlarged tapered rail-end plugs | Physically fit well, but the entire separate-cap scheme is superseded by the integral V3 left wing |
| V3 cradle split | Left wing 125.00 × 139.00 × 14.20 mm; right wing 111.33 × 139.00 × 14.20 mm | Replaces the 215 mm-wide single cradle print; continuous top/bottom edge rails absorb the outer joiner blocks; both wings remain rear-face-down and fit comfortably on the 220 mm bed |
| V3 removable joint | Three integral +X tongues: one at each long rail and one through the center plate; 18 mm seated insertion | Physical coupon fit despite major adhesion/stringing defects; retain the matching receiver's 0.50 mm total root and 1.10 mm total tip/lead clearances |
| V3 locking wedge | One corrected printed 3.70-to-3.30 mm tapered cross-wedge with a 7 mm pull head | Corrected pin retained and released successfully in the physical coupon; original floating-body G-code is stale; channel can take an M3 bolt if necessary |
| V3 left edge | Fully enclosed, rounded, integral part of the left cradle wing | No separate cap, plugs, sockets, screw, or nub; the left wing itself closes the holder during two-piece tablet assembly |
| Right fit coupon | Exact X = 78.0–111.5 mm crop of V2 cradle | 33.5 × 130 mm plan envelope; tests restored rail fit, right-edge seating, USB-C pocket, and open 16 × 8 mm cable rectangle |
| Button fit coupon | Exact top-left production-rail crop | 73.5 × 11 × 14.8 mm envelope; tests insertion path, seated button clearance, and intact wall after relief |
| Twin-plug coupon (historical) | Exact V2 crops of one rail socket and its identical tapered plug | Physically passed and remains useful process evidence; the joint is absent from V3 |

## Functional design

- The V3 candidate is assembled from two flat-print cradle wings, one removable locking wedge, a rear tilt bracket, and a closed sleeve. There is no separate left end cap and no cradle adhesive. The structural alignment-key STL is printed once for the unchanged bracket-to-sleeve glue joint.
- The left wing retains the tested button channel and adds a continuous rounded left wall and full-width screen-facing cap spanning the complete 139 mm V3 envelope. The right wing retains the tested USB-C housing and open 16 × 8 mm cable rectangle. Any remaining entry relief is confined to the rear/inner slide path; the outside left edge is closed. All V2 cap-specific tapered plugs, sockets, and receiver bulges are absent from V3.
- To load the tablet, seat its USB-C/right edge in the fixed right wing, align the fully enclosed left wing, and slide it +X until all three tongues reach their closed socket seats. Push the tapered wedge through the lower transverse channel. To service the tablet, pull the wedge and slide the left wing back off.
- The two outer tongues are 6 mm tall, bed-supported blocks entering locally reinforced receivers with open bed-side floors and softened exterior edges. Their 4.5 mm maximum socket roofs stay below the confirmed 10 mm PLA bridge rule. The center tongue remains within the 3 mm rear plate and enters a through-depth planar pocket.
- The lower tongue and receiver share a 4 × 4 mm transverse channel. The printed wedge narrows from 3.70 to 3.30 mm for a forgiving lead and snug seated root. If the actual PLA wedge is unreliable, the channel clears an M3 shaft; exact head, washer, nut, and length still require the user's hardware measurements.
- The rear bracket is bonded only to the fixed right wing and the bracket-to-sleeve joint remains glued. The bracket may contact the removable left wing but must receive no adhesive there. This preserves tablet serviceability while the existing 74 × 36 mm plate helps resist out-of-plane movement at the seam.
- The cradle prints with its complete rear frame datum on the bed. Cable clips are on the rear bracket. The previous end-stop screw boss and pilot are removed.
- The rear bracket prints on a 60 × 28 mm horizontal foot. Its 74 × 36 mm tilted plate bonds to the matching upper region of the cradle center plate and retains the two open braided-cable clips.
- The sleeve prints upside down on a 60 × 46 mm flange. Its tube-entry bore therefore remains open upward and its 3 mm seating cap becomes a supported floor rather than a 32.2 mm bridge.
- The rear bracket bonds only to the right cradle wing, using its existing broad face without a cradle alignment key. The bracket-to-sleeve bond retains one loose-fit 35 × 15 × 1.8 mm cross key and the previously validated groove clearance. Adhesive must be selected and prepared for the actual filament, but no adhesive belongs on the removable left wing or tongue/socket joint.
- The holder slides down over the tube using the unchanged closed cylindrical sleeve with a solid seating cap.
- The complete rear sleeve/collet assembly is lowered so its bottom is level with the installed holder's lower long edge. The sleeve dimensions and proven tube fit are unchanged.
- Two rear gussets connect the rear-offset sleeve to the tablet back support.
- The tablet is loaded between the two cradle wings before the wedge is inserted. The integral left wing closes the left edge; no separate cap is printed or installed, and the wing remains removable.
- The landscape-top rail has a concealed 2 mm-high × 1.2 mm-deep groove in its inner face, centered on the tablet's thickness. It begins at the left slide-in entrance and continues to 5 mm past the measured end of the seated 20–60 mm power/volume group. The groove clears the 1 mm button projection without breaking through the rail: a solid 1.8 mm exterior wall and the complete retaining lip remain.
- A continuous screen-facing cap covers the right side from the tablet edge to the solid outer wall; two internal stop walls beneath it locate the tablet while accommodating the 6.50 mm-projecting USB-C plug. The cap remains structurally continuous because the cable opening is in the rear pocket floor, not through the cap.
- The right-angle adapter turns immediately around the tablet's right edge and onto the open back; the flat pigtail and its downstream connection should be largely hidden behind the tablet rather than leaving straight out through the right wall.
- The right side presents a continuous enclosed screen-facing face: the outer wall and full-depth cap now span the complete 139 mm V3 perimeter, including the extended top/bottom corners. The plug chamber remains open toward the tablet cavity. One 16 mm-wide × 8 mm-deep rectangle removes the center rear pocket floor from the tablet cavity to the outer wall so the complete thick cable section can pass without threading through the superseded T-shaped opening.
- The 3.45 mm braided section snaps into two open C-clips on the rear spine. From the nearer clip it drops through open space outside the right gusset, sweeps behind the sleeve, and enters the rear-facing external sleeve channel through its snap opening. No segment passes through a holder, gusset, or sleeve solid, and the 9.6 mm-marked connector body remains accessible outside all captive features.
- The external sleeve channel has 4.15 mm internal clearance and a 2.8 mm snap opening. Its shallow 1.2 mm embed leaves at least 2.8 mm of the original 4 mm sleeve wall and does not intersect the tested 32.2 mm bore.
- Exposed perimeter, rail, lip, and integral-left-wall edges use larger plan-corner radii and longitudinal fillets so the holder feels softer than the earlier sharp-edged print. The front-frame opening follows the supplied tablet mesh's approximately 7 mm corner curve, and the outer frame radius is now 28 mm for a pronounced soft silhouette. Continuous top/bottom edge rails absorb the joiner blocks on the rear so the screen-facing perimeter reads as a straight, uninterrupted line. V3 has no vestigial screw-era projection below the left corner.
- Keep the rear open for material efficiency, airflow, and access. Do not convert this to a full bezel without confirming all device clearance zones.
- Active shared geometry is in `cad/tablet_stand_core.py`; the tested unsplit geometry remains in `cad/tablet_stand_v2.py`, and `cad/tablet_stand_v3.py` owns the removable tongue/wedge split, V3 assembly, and exports. Generated V3 review outputs are under `build/v3/`. If the V3 physical joint coupon passes, promote V3 to the sole production path and archive the V2-only workflow rather than maintaining both indefinitely.
- Before the full cradle, print `tablet_stand_v2_right_fit_coupon.stl` rear-face down in the intended PLA process. Slide the tablet's right edge through the short production rails, seat it against the internal stops, connect the real USB-C adapter, and confirm that the complete thick cable section passes through the open 16 × 8 mm rear rectangle without pinching or forcing the tablet.
- Also print `tablet_stand_v2_button_fit_coupon.stl` rear-face down. Slide it along the tablet's landscape-top edge from the left and confirm that the button group passes freely through the concealed inner groove without being pressed, while the outside of the rail remains closed and smooth.
- The first `tablet_stand_v3_lock_coupon_all3.stl` print physically passed tongue/receiver fit despite severe adhesion and stringing. The corrected pin then retained and released successfully. Do not rescale or change the confirmed tongue/socket clearances. The original combined support-free G-code is stale. The pre-revision right-wing production G-code was sliced with snug 45° supports and a 5 mm brim, independently validated, and completed on 2026-08-10. The user found the support material difficult to distinguish/remove in this PLA; the rounded-finish revision invalidates that G-code and needs a fresh, more removable support strategy. The left wing and remaining parts still require their own review and authorization.

## Full-cradle slice status

- The unsplit V2 cradle is 215 × 135.6 × 14.8 mm and technically fits the confirmed 220 × 220 mm bed, but its narrow margin motivated the V3 split.
- The V3 left and right cradle-wing STLs are each single watertight solids and remain rear-face-down. Their largest plan dimension is 139 mm, leaving generous bed margin.
- Previous full-cradle, end-stop, combined V3 coupon, and both earlier right-wing G-code files are stale. Do not print them. The tongue/receiver fit and wedge retention gates passed. The latest right-wing fit job completed, but it used the pre-correction 130 mm USB-C end-wall/cap span; the active full-span geometry requires a new slice. Do not start the corrected right wing, left wing, or other parts until their fresh slices and support/adhesion review are complete.

## Known unknowns before a full print

- Flat cable and connector-body width.
- Whether the photo's 9.6 mm annotation is connector width, height, or another measurement.
- Speaker, camera, microphone, and any other edge clearances not covered by the measured power/volume group.
- The successful V2 twin-plug coupon remains useful PLA fit evidence, but it does not replace the required V3 tongue/wedge coupon test.
- Unobstructed tube length above its existing mounting point.
- The Ender-3 Pro profile, 0.4 mm nozzle, PLA, 220 × 220 × 250 mm build volume, and rear-face-down cradle orientation are verified. The tongue/receiver physically fit on 2026-08-10 despite major adhesion/stringing defects, and the corrected wedge retained and released successfully. Full production slices and first-layer adhesion strategy remain to be reviewed.
- Adhesive selection, surface preparation, clamp method, and cure time for the selected filament.
