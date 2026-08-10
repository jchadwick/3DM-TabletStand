# Version 3 removable split cradle

V3 preserves the physically tested tablet, button, USB-C, tube, and cable
interfaces. It replaces the 215 mm cradle and separate left cap with two
bed-friendly wings joined without cradle glue.

## Review files

- `tablet_stand_v3_multiview.png`: installed, enclosed-left-edge, removable
  joint, and print-layout views.
- `tablet_stand_v3_preview.png`: installed assembly with the two wings in
  different blues and the locking wedge in orange.
- `tablet_stand_v3_left_edge.png`: continuous integral left wall.
- `tablet_stand_v3_rear_joint.png`: exploded view of the three tongues,
  receivers, and lower cross-wedge.
- `tablet_stand_v3_print_layout.png`: two independent rear-face-down wings and
  one locking wedge.
- `tablet_stand_v3.step`: installed assembly.

## Production-oriented exports

- `tablet_stand_v3_cradle_left.stl`: 125.00 × 135.50 × 14.20 mm; rear face
  down; includes the enclosed rounded left edge and all three tongues.
- `tablet_stand_v3_cradle_right.stl`: 111.33 × 139.00 × 14.20 mm; rear face
  down; includes the three matching receivers and lower locking channel.
- `tablet_stand_v3_locking_wedge.stl`: print one; removable tapered cross-lock.
- `tablet_stand_v3_rear_bracket.stl`: bonds only to the fixed right wing.
- `tablet_stand_v3_sleeve.stl`: unchanged tested 32.2 mm sleeve.
- `tablet_stand_v3_alignment_key_print_1.stl`: print one for the unchanged
  rear-bracket-to-sleeve adhesive joint.

## Exact joint coupon

- `tablet_stand_v3_lock_coupon_left.stl`: production lower tongue crop.
- `tablet_stand_v3_lock_coupon_right.stl`: production lower receiver crop.
- `tablet_stand_v3_lock_coupon_wedge.stl`: production locking wedge.
- `tablet_stand_v3_lock_coupon_all3.stl`: all three exact coupon parts spaced
  on one bed datum for the combined print job.
- `tablet_stand_v3_lock_coupon_plate.png`: direct CadQuery preview of that
  combined three-piece layout.

The first combined support-free plate was physically tested. Despite major
adhesion/stringing defects, the tongue and receiver fit together. The wedge
layout failed because its larger pull head put the narrower body about 1.65 mm
above the bed. Do not reuse the combined G-code; give the wedge a common flat
datum or removable support before its next print.

## Removable joint

The left wing slides +X. Its upper, center, and lower tongues enter 18 mm-deep
closed-back receivers. Seated/root clearance is 0.50 mm total; the tapered lead
has 1.10 mm total clearance.

The lower tongue and receiver have an aligned 4 × 4 mm transverse channel. A
printed wedge tapers from 3.70 to 3.30 mm and has a 7 mm pull head. If it proves
unreliable in the user's PLA, the same channel clears an M3 shaft; exact bolt,
washer, nut, and head pockets must wait for physical hardware measurements.

The rear bracket is glued only to the fixed right wing. Do not put adhesive on
the left wing, tongues, receivers, or wedge. Pulling the wedge and sliding the
left wing off must remain possible for tablet service.

All current STL exports are single watertight solids. V3 has not been sliced,
uploaded, or authorized for a full-part print.

## Active coupon print

- `tablet_stand_v3_lock_coupon_all3_pla.gcode`: combined PLA job; 0.16 mm
  layers, three walls, 20% grid infill, 5 mm brim, 205/200 °C nozzle, 60 °C
  bed, supports disabled, and 1.0 mm retraction at 40 mm/s.
- `tablet_stand_v3_lock_coupon_toolpath.png`: actual PrusaSlicer extrusion-path
  review; it contains all three model islands and zero support extrusion.
- `tablet_stand_v3_lock_coupon_geometry.json` and
  `tablet_stand_v3_lock_coupon_brief.json`: inspected geometry and confirmed
  per-print decisions.

Independent G-code validation reports a 100 × 46 × 9 mm brim-inclusive
footprint, 31m 11s estimated time, about 3.1 g of PLA, and 6.2 mm³/s peak flow.
The only retained warnings are the profile's pre-macro bed heat and missing UI
thumbnail. The user authorized all three coupon pieces, the camera showed an
empty bed, and the job was started on 2026-08-09. On 2026-08-10 the user
reported major adhesion failure but confirmed that the tongue and receiver
still fit. The corrected wedge/pin then retained and released successfully.
The combined coupon G-code is stale; fresh full-part slices are now the next
gate.
