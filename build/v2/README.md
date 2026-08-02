# Version 2 outputs

V2 separates the support-conflicted V1 main body into glue-aligned printable
modules while preserving the confirmed tablet, tube, tilt, and cable geometry.

## Print files

- `tablet_stand_v2_cradle.stl`: print rear frame face down.
- `tablet_stand_v2_rear_bracket.stl`: print the horizontal foot down.
- `tablet_stand_v2_sleeve.stl`: print the 60 × 46 mm flange down, with the
  32.2 mm tube-entry bore open upward.
- `tablet_stand_v2_end_stop.stl`: print the screen-facing lip/top face down.
- `tablet_stand_v2_alignment_key_print_2.stl`: print **two copies** flat.
- `tablet_stand_v2_right_fit_coupon.stl`: print rear face down before the full
  cradle; it is an exact 33.5 mm-wide crop of the production right end and
  tests the restored production rail allowances, right-edge stops, USB-C
  pocket, and the open 16 mm-wide × 8 mm-deep cable rectangle.
- `tablet_stand_v2_button_fit_coupon.stl`: print rear face down before the full
  cradle; it is an exact 73.5 × 11 × 14.2 mm crop of the production top-left
  rail. Slide it along the landscape-top tablet edge to verify that the
  measured 20–60 mm button group passes freely through the 3 mm-high channel
  without being pressed. The channel is open at the insertion end and extends
  5 mm beyond the seated button group.
- `tablet_stand_v2_button_fit_coupon_pla.gcode`: validated Ender-3 Pro PLA
  button-coupon job in the exact production orientation; 0.20 mm layers, three
  walls, 20% grid infill, no supports, approximately 22 min and 4.8 g. The
  slicer warns about the intentionally unsupported production rail lip; inspect
  that short 3 mm cantilever after printing.
- `tablet_stand_v2_right_fit_coupon_pla.gcode`: validated Ender-3 Pro PLA
  coupon job; 0.20 mm layers, three walls, 20% grid infill, no supports,
  approximately 1 h 25 min and 18.6 g. Prepared only.

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

All five production STL files and both fit-coupon STLs are single
watertight solids. The alignment-key STL is printed twice. The cradle has a
broad 216 × 137.5 mm rear datum, the bracket has a 60 × 28 mm foot, and the
sleeve has a 60 × 46 mm flange. The split removes the V1 tall rail-support
towers and the support ceiling inside the sleeve bore.
The remaining flagged overhangs are predominantly the cradle's 2.2 mm lips,
short USB-C bridges, shallow alignment-groove roofs, and the two open cable
clips.

Start with no supports at 0.20 mm layers and inspect the slicer preview. If the
printer struggles with the rear clips, paint support only under those two
features. A 216 mm cradle span is still marginal on a nominal 220 mm bed; rotate
it diagonally in the slicer and verify the actual printable area.

V2 is a validated concept, not a production-ready release. Confirm the remaining
device clearances, end-stop screw length, printer/material, tube length, and fit
coupons before a full print.
