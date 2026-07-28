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
- Both V2 glue joints use matching shallow cross grooves and one 36 × 16 × 2 mm printed key; the alignment-key STL is printed twice. The user confirmed that gluing the main body parts is acceptable.
- The bracket carries the two open braided-cable clips so the cradle keeps a completely flat rear print datum.
- The removable V2 end stop retains one M3 screw, now on a local-Z boss outside the tablet cavity so neither the cradle nor stop inherits V1's rear-projecting pad.
- Routine previews use direct in-memory CadQuery tessellation with Trimesh's depth-buffered renderer. Blender is reserved for optional polished presentation renders.

## Revision history

### Support-minimized keyed-glue V2 — 2026-07-28

- Evaluated the monolithic V1 main STL in its viable sleeve-vertical orientation. Approximate triangle analysis flagged about 7,700 mm² of downward-facing surface beyond a 45-degree support rule, including the full-width upper rail and the 32.2 mm sleeve-cap ceiling.
- Split the active V2 main structure into a cradle, rear tilt bracket, and sleeve while preserving the 200 × 123 × 8.4 mm tablet envelope, 80-degree screen angle, 32.2 mm tested bore, 51 mm engagement, 3 mm seating cap, 24 mm rear offset, and Z = -64.53 mm sleeve-bottom alignment.
- The cradle prints on a 216 × 137.5 mm rear datum; the bracket prints on a 60 × 28 mm foot; and the sleeve prints upside down on a 60 × 46 mm flange with its tube-entry bore open upward.
- The user confirmed that the main structural parts may be glued. Removed the provisional eight-screw structural scheme and retained only the removable end stop's single M3 screw.
- Added matching half-depth cross grooves to both glue joints and one 36 × 16 × 2 mm alignment-key STL to print twice. Each groove is 1.15 mm deep with 0.25 mm planar clearance.
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
