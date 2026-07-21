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
| Retaining screw | M3 | User hardware |

## Active design decisions

- Landscape tablet orientation.
- Simple, sleek, skeletal support rather than a bulky closed enclosure.
- Tablet slides in from the left through narrow long-edge rails.
- A removable left end stop secured by one M3 screw provides retention more secure than snap clips.
- The right edge uses internal corner stops plus a closed outer end that contains the low-profile USB-C plug. The tablet may slide onto a plug positioned in the pocket.
- The outer end has a broad centered groove for the 0.6 mm flat cable; connector/cable width remains unconfirmed, so the groove must not become close-fitting.
- Exposed outside corners are lightly filleted to remove sharp edges without making the skeletal holder bulky.
- The holder installs by sliding a closed 32.2 mm ID sleeve down over the accessible top of the vertical tube.
- With the tablet nearly vertical, the sleeve is centered left-to-right but offset behind the screen plane; version 1 uses a 24 mm Y offset and two structural ribs.
- Routine previews use direct in-memory CadQuery tessellation with Trimesh's depth-buffered renderer. Blender is reserved for optional polished presentation renders.

## Revision history

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
