# Current Design Specification

## Purpose and status

The project is a simple, sleek, FDM-printable landscape holder for a 2024 onn. 8-inch tablet. It mounts permanently to the accessible top end of a vertical 32 mm OD tube. Version 2 is the sole active model; superseded V1 is archived only in Git history at commit `560c6e8` and is not maintained. Exact-production fit coupons cover the right-side rails/USB-C route and landscape-top button channel.

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
| Retaining hardware | M3 screw | User has M3 screws |
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
| Exposed corner radii | 1.2 mm rails/walls; 0.8 mm lips | Rounded to remove sharp outside corners |
| V2 main-body split | Cradle, rear tilt bracket, sleeve | Separates conflicting print axes |
| V2 glue alignment | 35 × 15 × 1.8 mm cross key, print quantity 2 | Existing 36.25 × 16.25 × 4.25 mm grooves retained; at least 1.25 mm total planar clearance, 0.50 mm thickness clearance, and 0.4 mm edge relief; user fit-test correction |
| Cradle-to-bracket bond | 74 × 36 mm nominal mating face | Align matching side and top edges |
| Bracket-to-sleeve bond | 60 × 28 mm nominal mating face | Align matching side and front edges |
| V2 end-stop screw | One M3, vertical local axis outside tablet cavity | Replaces V1 rear-projecting lug; exact length still unconfirmed |
| Right fit coupon | Exact X = 78.0–111.5 mm crop of V2 cradle | 33.5 × 130 mm plan envelope; tests restored rail fit, right-edge seating, USB-C pocket, and open 16 × 8 mm cable rectangle |
| Button fit coupon | Exact top-left production-rail crop | 73.5 × 11 × 14.2 mm envelope; tests insertion path, seated button clearance, and intact wall after relief |

## Functional design

- The active V2 holder is assembled from a flat-print cradle, a rear tilt bracket, a closed sleeve, and the removable end stop. One identical alignment-key STL is printed twice for the two structural glue joints.
- The cradle prints with its complete rear frame datum on the bed. Cable clips are on the rear bracket, and the end-stop screw uses a front-accessible vertical boss outside the tablet cavity.
- The rear bracket prints on a 60 × 28 mm horizontal foot. Its 74 × 36 mm tilted plate bonds to the matching upper region of the cradle center plate and retains the two open braided-cable clips.
- The sleeve prints upside down on a 60 × 46 mm flange. Its tube-entry bore therefore remains open upward and its 3 mm seating cap becomes a supported floor rather than a 32.2 mm bridge.
- Both structural joints are adhesive bonds with matching cross grooves. Each uses one loose-fit 35 × 15 × 1.8 mm printed key to constrain X/Y alignment during cure. The key has at least 1.25 mm total planar clearance, 0.50 mm total thickness clearance, and 0.4 mm edge relief so first-layer flare cannot jam the glue joint. Adhesive—not key friction—carries the joint. Adhesive must be selected and prepared for the actual filament.
- The holder slides down over the tube using the unchanged closed cylindrical sleeve with a solid seating cap.
- The complete rear sleeve/collet assembly is lowered so its bottom is level with the installed holder's lower long edge. The sleeve dimensions and proven tube fit are unchanged.
- Two rear gussets connect the rear-offset sleeve to the tablet back support.
- The tablet loads from the left through narrow rails on the long edges.
- The landscape-top rail has a concealed 2 mm-high × 1.2 mm-deep groove in its inner face, centered on the tablet's thickness. It begins at the left slide-in entrance and continues to 5 mm past the measured end of the seated 20–60 mm power/volume group. The groove clears the 1 mm button projection without breaking through the rail: a solid 1.8 mm exterior wall and the complete retaining lip remain.
- A removable left end stop secured by one M3 screw prevents the tablet from sliding out.
- A continuous screen-facing cap covers the right side from the tablet edge to the solid outer wall; two internal stop walls beneath it locate the tablet while accommodating the 6.50 mm-projecting USB-C plug. The cap remains structurally continuous because the cable opening is in the rear pocket floor, not through the cap.
- The right-angle adapter turns immediately around the tablet's right edge and onto the open back; the flat pigtail and its downstream connection should be largely hidden behind the tablet rather than leaving straight out through the right wall.
- The right side presents a continuous enclosed screen-facing face: the outer wall is solid and a full-depth cap spans the entire short edge. The plug chamber remains open toward the tablet cavity. One 16 mm-wide × 8 mm-deep rectangle removes the center rear pocket floor from the tablet cavity to the outer wall so the complete thick cable section can pass without threading through the superseded T-shaped opening.
- The 3.45 mm braided section snaps into two open C-clips on the rear spine. From the nearer clip it drops through open space outside the right gusset, sweeps behind the sleeve, and enters the rear-facing external sleeve channel through its snap opening. No segment passes through a holder, gusset, or sleeve solid, and the 9.6 mm-marked connector body remains accessible outside all captive features.
- The external sleeve channel has 4.15 mm internal clearance and a 2.8 mm snap opening. Its shallow 1.2 mm embed leaves at least 2.8 mm of the original 4 mm sleeve wall and does not intersect the tested 32.2 mm bore.
- Exposed rail, end-wall, and removable-stop corners are lightly rounded so the case does not present sharp outside corners.
- Keep the rear open for material efficiency, airflow, and access. Do not convert this to a full bezel without confirming all device clearance zones.
- Active shared geometry is in `cad/tablet_stand_core.py`, modular assembly/export logic is in `cad/tablet_stand_v2.py`, and generated outputs are under `build/v2/`. Superseded V1 is intentionally maintained only in Git history.
- Before the full cradle, print `tablet_stand_v2_right_fit_coupon.stl` rear-face down in the intended PLA process. Slide the tablet's right edge through the short production rails, seat it against the internal stops, connect the real USB-C adapter, and confirm that the complete thick cable section passes through the open 16 × 8 mm rear rectangle without pinching or forcing the tablet.
- Also print `tablet_stand_v2_button_fit_coupon.stl` rear-face down. Slide it along the tablet's landscape-top edge from the left and confirm that the button group passes freely through the concealed inner groove without being pressed, while the outside of the rail remains closed and smooth.

## Full-cradle slice review

- The active PLA cradle candidate is `build/v2/tablet_stand_v2_cradle_pla.gcode`: rear face down, 0.20 mm layers, three walls, 20% grid infill, no skirt, and no supports. Validation reports X = 2–218 mm and Y = 41–179 mm, 4 h 39 min, about 61.8 g, and 7.5 mm³/s peak flow.
- `build/v2/tablet_stand_v2_cradle_pla_supports.gcode` is a review-only comparison with snug 45-degree supports. It grows to the complete X = 0–220 mm configured span, adds about 29 minutes and 9.4 g, and places support against the long rail lips and right-end features.
- Prefer the support-free candidate: earlier production-orientation rail coupons printed successfully without support, the remaining unsupported spans are short, and automatic support would consume all X margin and require removal from fit-critical rail surfaces.
- The removable end stop cannot share the nearly full-width cradle plate and must be printed as a separate job.

## Known unknowns before a full print

- Flat cable and connector-body width.
- Whether the photo's 9.6 mm annotation is connector width, height, or another measurement.
- Speaker, camera, microphone, and any other edge clearances not covered by the measured power/volume group.
- M3 end-stop screw length and whether its 2.7 mm printed pilot should be drilled for the selected screw.
- Unobstructed tube length above its existing mounting point.
- The confirmed Ender-3 Pro profile, 0.4 mm nozzle, PLA, 220 × 220 × 250 mm build volume, and rear-face-down cradle orientation are now verified; the support-free cradle uses X = 2–218 mm.
- Adhesive selection, surface preparation, clamp method, and cure time for the selected filament.
