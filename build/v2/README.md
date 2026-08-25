# Version 2 outputs

V2 is retained as the historical geometry basis and fit-coupon evidence while
V3 is the active removable-wing design.

## Print files

- `tablet_stand_v2_cradle.stl`: print rear frame face down.
- `tablet_stand_v2_rear_bracket.stl`: print the horizontal foot down.
- `tablet_stand_v2_sleeve.stl`: print the 60 × 46 mm flange down, with the
  32.2 mm tube-entry bore open upward.
- `tablet_stand_v2_end_stop.stl`: print its broad outside wall face down so the
  two tapered rail plugs build vertically. The cap slides horizontally into
  the cradle's reinforced open-ended rail sockets with no screw, hook, detent,
  projecting lower nub, or support-trapping dovetail.
- `tablet_stand_v2_alignment_key_print_2.stl`: print **two copies** flat.
- `tablet_stand_v2_right_fit_coupon.stl`: print rear face down before the full
  cradle; it is an exact 33.5 mm-wide crop of the production right end and
  tests the restored production rail allowances, right-edge stops, USB-C
  pocket, and the open 16 mm-wide × 8 mm-deep cable rectangle.
- `tablet_stand_v2_button_fit_coupon.stl`: print rear face down before the full
  cradle; it is an exact 73.5 × 11 × 14.8 mm crop of the production top-left
  rail. Slide it along the landscape-top tablet edge to verify that the
  measured 20–60 mm button group passes freely through the concealed 2 mm-high
  × 1.2 mm-deep inner groove without being pressed. The groove begins at the
  insertion end, extends 5 mm beyond the seated button group, and preserves a
  solid 1.8 mm exterior rail wall.
- `tablet_stand_v2_left_slide_coupon_cradle.stl` and
  `tablet_stand_v2_left_slide_coupon_stop.stl`: exact production crops of one
  rail socket and its identical tapered plug. Print them as separate jobs to
  check horizontal insertion, closed-end seating, retention, and real PLA
  clearance. `tablet_stand_v2_left_slide_coupon_plate.stl` is preview-only.
- `tablet_stand_v2_left_slide_coupon_cradle_rev2_pla.gcode` and
  `tablet_stand_v2_left_slide_coupon_stop_rev3_pla.gcode` are retained only as
  evidence for the physically tested V2 socket/plug process. The joint is not
  present in V3; do not use these files for the active holder.
- `tablet_stand_v2_left_slide_coupon_plate_preview.png`: six-view mesh review
  of the separated two-piece coupon plate in its corrected print orientations.
- Stale button-coupon, right-fit-coupon, two-key, full-cradle, and cap G-code
  is intentionally absent. The current V2 coupon STLs and all historical
  slices remain recoverable from Git history; regenerate from the current STL
  only if a new physical test is explicitly authorized.

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
The cradle has a broad 215 × 135.6 mm rear datum, the bracket has a 60 × 28 mm foot, and the
sleeve has a 60 × 46 mm flange. The modular split avoids tall rail-support
towers and the support ceiling inside the sleeve bore.
The remaining flagged overhangs are predominantly the cradle's 2.2 mm lips,
short USB-C bridges, shallow alignment-groove roofs, and the two open cable
clips.

Start with no supports at 0.20 mm layers and inspect the slicer preview. If the
printer struggles with the rear clips, paint support only under those two
features. The cradle cannot be rotated diagonally into a smaller bounding box.
The production plate removes the optional 6 mm skirt and centers the 215 mm
cradle. Do not add a skirt or brim to this job. Test the twin-plug coupon before
uploading the full cradle.

V2 is a validated concept, not a production-ready release. Confirm the remaining
device clearances, physical twin-plug coupon result, tube length, adhesive
choice, and other fit coupons before a full print.
