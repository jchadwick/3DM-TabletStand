# Version 3 removable split cradle

V3 preserves the physically tested tablet, button, USB-C, tube, and cable
interfaces. It replaces the 215 mm cradle and separate left cap with two
bed-friendly wings joined without cradle glue.

## Review files

- `tablet_stand_v3_multiview.png`: installed, enclosed-left-edge, USB/cable,
  removable-joint, and print-layout views of the smooth unified front ring.
- `tablet_stand_v3_preview.png`: installed assembly with the two wings in
  different blues and the locking wedge in orange.
- `tablet_stand_v3_left_edge.png`: continuous integral left wall with no
  obsolete end-stop/slider step.
- `tablet_stand_v3_button_channel.png`: inner-side detail of the full-travel
  concealed 2.0 × 1.2 mm left-wing button groove, highlighted in green.
- `tablet_stand_v3_rear_joint.png`: exploded view of the three tongues,
  receivers, and lower cross-wedge.
- `tablet_stand_v3_print_layout.png`: two independent rear-face-down wings and
  one locking wedge.
- `tablet_stand_v3_assembly_grooves.png`: annotated view of the matching
  cross-grooves on the bracket foot and sleeve flange.
- `tablet_stand_v3_bracket_to_cradle_bond.png`: annotated unkeyed adhesive
  contact areas between the fixed right wing and rear bracket.
- `tablet_stand_v3_rear_bracket_print.png`: active broad-plate-down bracket
  orientation with its single 12 mm cable channel opening upward.
- `tablet_stand_v3.step`: installed assembly.

## Production-oriented exports

- `tablet_stand_v3_cradle_left.stl`: 125.00 × 139.00 × 14.20 mm; rear face
  down; includes the enclosed rounded left edge and all three tongues.
- `tablet_stand_v3_cradle_right.stl`: 111.33 × 139.00 × 14.20 mm; rear face
  down; includes the three matching receivers and lower locking channel.
- `tablet_stand_v3_locking_wedge.stl`: print one; removable tapered cross-lock.
- `tablet_stand_v3_rear_bracket.stl`: bonds only to the fixed right wing;
  exported broad cradle-bond plate down with the one 12 mm cable channel up.
- `tablet_stand_v3_sleeve.stl`: unchanged tested 32.2 mm sleeve.
- `tablet_stand_v3_alignment_key_print_1.stl`: print one for the unchanged
  rear-bracket-to-sleeve adhesive joint.

## Active replacement-bracket print

- `tablet_stand_v3_rear_bracket_clips_up_pla.gcode`: validated functional PLA
  slice; 0.20 mm layers, five walls, 40% grid infill, no supports, no brim.
- `tablet_stand_v3_rear_bracket_clips_up_pla.ini`: resolved slicer settings
  extracted from the generated G-code configuration block.
- `tablet_stand_v3_rear_bracket_clips_up_validation.txt`: clean bounds,
  temperature, flow, thumbnail, and Klipper-macro validation.
- `tablet_stand_v3_rear_bracket_clips_up_print_record.json`: hashes, settings,
  camera clearance evidence, upload/start result, and job status.

The user explicitly authorized this replacement print. A fresh camera snapshot
showed the complete bed empty, Moonraker accepted the start at 2026-08-27
04:48:05 UTC, and the printer reported the job in progress.

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
above the bed. Its stale combined G-code has been removed from the active tree;
give the wedge a common flat datum or removable support before any new print.

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

The visible front perimeter is one continuous 2 mm ring across both wings,
with only the flush center split; separately stacked V2 lips, caps, bezel, and
coplanar shroud faces are gone. The concealed top-button groove runs from the
integral left closure-side interior to the center seam while retaining its
1.8 mm exterior wall.

Each individual-part STL export is a single watertight solid; the combined
three-piece lock-coupon plate intentionally contains three watertight components.
The pre-revision right-wing STL was sliced with snug 45° supports and a 5 mm brim,
independently validated, uploaded, and completed on 2026-08-10. The user
reported that the supports were difficult to distinguish/remove in this PLA.
The active rounded-finish geometry supersedes that G-code; all three stale
right-wing slices and their associated INI/print-record/validation files have
been removed from the active tree. Subsequent reprints should preserve the more
removable support strategy. On 2026-08-27 the user reported that all production
parts printed well and fit
great; permanent bracket/sleeve adhesive assembly remained to be completed.

## Historical coupon print evidence

- `tablet_stand_v3_lock_coupon_toolpath.png`: actual PrusaSlicer extrusion-path
  review from the physically tested combined job; it contains all three model
  islands and zero support extrusion.
- `tablet_stand_v3_lock_coupon_geometry.json` and
  `tablet_stand_v3_lock_coupon_brief.json`: inspected geometry and confirmed
  per-print decisions retained as fit evidence.

The user authorized and started that combined job on 2026-08-09. On 2026-08-10
the user reported major adhesion failure but confirmed that the tongue and
receiver still fit; the corrected wedge/pin then retained and released
successfully. The stale combined coupon G-code has been removed and remains
recoverable from Git history. Fresh full-part slices are now the next gate.
