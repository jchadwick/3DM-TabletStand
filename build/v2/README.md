# Version 2 outputs

The active design uses glue-aligned printable modules while preserving the
confirmed tablet, tube, tilt, and cable geometry.

## Print files

- `tablet_stand_v2_cradle.stl`: print rear frame face down.
- `tablet_stand_v2_rear_bracket.stl`: print the horizontal foot down.
- `tablet_stand_v2_sleeve.stl`: print the 60 × 46 mm flange down, with the
  32.2 mm tube-entry bore open upward.
- `tablet_stand_v2_end_stop.stl`: print its broad outside wall face down so the
  dovetail builds vertically instead of cantilevering into open air. Its tongue
  slides downward into the cradle's closed-bottom groove with no screw, hook,
  detent, or projecting lower nub.
- `tablet_stand_v2_alignment_key_print_2.stl`: print **two copies** flat.
- `tablet_stand_v2_right_fit_coupon.stl`: print rear face down before the full
  cradle; it is an exact 33.5 mm-wide crop of the production right end and
  tests the restored production rail allowances, right-edge stops, USB-C
  pocket, and the open 16 mm-wide × 8 mm-deep cable rectangle.
- `tablet_stand_v2_button_fit_coupon.stl`: print rear face down before the full
  cradle; it is an exact 73.5 × 11 × 14.2 mm crop of the production top-left
  rail. Slide it along the landscape-top tablet edge to verify that the
  measured 20–60 mm button group passes freely through the concealed 2 mm-high
  × 1.2 mm-deep inner groove without being pressed. The groove begins at the
  insertion end, extends 5 mm beyond the seated button group, and preserves a
  solid 1.8 mm exterior rail wall.
- `tablet_stand_v2_left_slide_coupon_cradle.stl` and
  `tablet_stand_v2_left_slide_coupon_stop.stl`: exact lower-left production
  crops for checking dovetail capture, downward travel, closed-bottom seating,
  and real PLA slide clearance. `tablet_stand_v2_left_slide_coupon_plate.stl` arranges both pieces
  together with a 28 mm inter-part gap for the prepared coupon job.
- `tablet_stand_v2_left_slide_coupon_pla.gcode`: corrected two-piece retry at
  0.16 mm layers, three walls, 20% grid infill, a removable 5 mm brim, and
  45-degree grid supports. It uses 205 °C for the first layer, then 200 °C,
  with 1.0 mm retraction at 40 mm/s; approximately 40 min 49 s and 5.0 g.
- `tablet_stand_v2_left_slide_coupon_support_review.png`: actual model paths
  in blue and support paths in orange for the corrected retry.
- `tablet_stand_v2_left_slide_coupon_plate_preview.png`: six-view mesh review
  of the separated two-piece coupon plate in its corrected print orientations.
- `tablet_stand_v2_button_fit_coupon_pla.gcode`: validated Ender-3 Pro PLA
  button-coupon job in the exact production orientation; 0.20 mm layers, three
  walls, 20% grid infill, no supports, approximately 23 min and 5.3 g. Inspect
  the short internal groove and smooth closed outside wall after printing.
- `tablet_stand_v2_right_fit_coupon_pla.gcode`: validated Ender-3 Pro PLA
  coupon job; 0.20 mm layers, three walls, 20% grid infill, no supports,
  approximately 1 h 25 min and 18.6 g. Prepared only.
- `tablet_stand_v2_cradle_pla.gcode`: support-free full-cradle PLA candidate;
  rear face down, 0.20 mm layers, three walls, 20% grid infill, no skirt, and
  no supports; approximately 4 h 8 min and 60.7 g. Its extrusion footprint is
  X = 3–217 mm and Y = 45–175 mm.
- `tablet_stand_v2_cradle_pla_supports.gcode`: review-only snug 45-degree support
  comparison with 0.25 mm XY spacing; approximately 4 h 28 min and 67.4 g. It
  places support on the long rail lips and end features, so it is not the
  recommended upload candidate.
- `tablet_stand_v2_end_stop_pla.gcode`: stale bridge-face-down slice invalidated
  by the first physical coupon failure; do not print it. Re-slice after the
  outside-wall-down coupon passes.
- `tablet_stand_v2_cradle_support_review.png`: top, front, and per-layer views
  of actual PrusaSlicer model and support extrusion paths.

`tablet_stand_v2.step` is the installed assembly. `model_parameters.json`
records the module orientations, glue joints, key dimensions, and preserved
fit-critical values.

## Alignment and assembly

Each structural glue joint uses one loose-fit 35 × 15 × 1.8 mm cross key. The
mating parts retain 36.25 × 16.25 × 4.25 mm cross grooves that are 1.15 mm deep
per side, leaving at least 1.25 mm total planar clearance and 0.50 mm total
thickness clearance for adhesive and print variation.

1. Bond the rear bracket plate to the cradle. Match the bracket's 74 mm side
   edges and top edge to the cradle center plate.
2. Bond the bracket foot to the sleeve flange. Match the 60 mm side edges and
   front edges.
3. Keep adhesive out of the tablet cavity, tube bore, cable features, and
   removable end-stop path.
4. Clamp each joint against a flat reference until fully cured.

Choose adhesive for the printed material: two-part epoxy is the conservative
general choice; use a plastic-specific adhesive for PETG and roughen/clean both
bond faces according to the adhesive instructions.

## Printability

All five production STL files and four individual fit-coupon part STLs are
single watertight solids. The combined left-slide coupon plate intentionally
contains those two watertight pieces. The alignment-key STL is printed twice.
The cradle has a broad 215 × 130 mm rear datum, the bracket has a 60 × 28 mm foot, and the
sleeve has a 60 × 46 mm flange. The modular split avoids tall rail-support
towers and the support ceiling inside the sleeve bore.
The remaining flagged overhangs are predominantly the cradle's 2.2 mm lips,
short USB-C bridges, shallow alignment-groove roofs, and the two open cable
clips.

Start with no supports at 0.20 mm layers and inspect the slicer preview. If the
printer struggles with the rear clips, paint support only under those two
features. The cradle cannot be rotated diagonally into a smaller bounding box.
The production plate removes the optional 6 mm skirt and centers the 215 mm
cradle. Do not add a skirt or brim to this job. Test the left-slide coupon before
uploading the full cradle.

V2 is a validated concept, not a production-ready release. Confirm the remaining
device clearances, physical left-slide coupon result, tube length, adhesive
choice, and other fit coupons before a full print.
