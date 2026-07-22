# Dimensions and requirements

This sheet consolidates only the user's words, measurements, and supplied reference assets. It does not use or describe the existing stand CAD.

## Tablet

| Item | Value / requirement | Basis |
|---|---:|---|
| Device | 2024 onn. 8-inch tablet | User prompt |
| Supplied reference envelope | 200 × 123 × 8.4 mm | Direct min/max measurement of vertices in `assets/tinker.obj` |
| Intended orientation | Landscape | Right-hand short-edge USB-C placement and supplied tablet envelope |
| USB-C location | Center of the right-hand side/short edge when facing the screen | User prompt |
| Final screen angle | 10° back from vertical; equivalently 80° above horizontal | Later user correction; supersedes the early 10°-above-horizontal interpretation |
| Direction of lean | Bottom long edge is closer to the user; top long edge is farther from the user | User clarification |

The OBJ is a device envelope/reference mesh, not a printable stand design. Its raw bounds are X = −93 to 107 mm, Y = −72 to 51 mm, and Z = 0 to 8.4 mm.

## Existing support tube

| Item | Value / requirement | Basis |
|---|---:|---|
| Tube outside diameter | 32.0 mm OD | User measurement |
| Tested mating bore | 32.2 mm ID | User fit test; described as perfectly tight |
| Mounting concept | Stand sits permanently on top of the tube | User prompt |

Do not substitute a generic fit allowance for the 32.2 mm bore without discussing it: that dimension comes from a physical test print on the actual tube.

## USB-C cable and adapter

| Item | Value / requirement | Confidence / note |
|---|---:|---|
| Plug/adapter projection from tablet | 0.256 in = 6.5024 mm | Later prompt explicitly uses an inch mark. The first prompt says `0.256mm`, which conflicts and appears to be a unit typo. Preserve the discrepancy until physically checked. |
| Flat section description | Flat, very low profile | Explicit user description |
| Flat-section transverse measurement | First prompt says `.7mm wide`; prior planning also treated the flat section as about 0.6 mm thick | Measurement axis and exact value should be rechecked before making a close fit |
| Annotated flat pigtail length | 51.4 mm | Handwritten marking in `assets/IMG_7233 Large.jpeg` |
| Annotated downstream connector-body measurement | 9.6 mm | Handwritten marking in the physical photo; the measurement axis is not unambiguous |
| Additional handwritten mark | `2` near the downstream connector body | Units and axis are not sufficiently clear to use as a captive-feature dimension |
| Cable after pictured pigtail | 3.45 mm diameter, round braided wire | Explicit later user measurement |

Cable routing requirements:

- The right-angle USB-C adapter turns immediately behind the tablet.
- The adapter/pigtail should be largely hidden and routed toward a groove in or on the tube collet/sleeve area.
- The tablet should be able to slide into the holder. It is acceptable to plug in the cable first and then slide the tablet into place.
- Keep cable routing open or snap-in. Both ends have USB-C connectors, so do not require a connector to pass through a small captive hole.
- Clips are acceptable and desired; the free cable path must not pass through solid material to reach them.
- The downstream connector body should remain outside close-fitting captive features until its 9.6 mm annotation axis and other body dimensions are confirmed.

## Holder behavior and appearance

- Simple and sleek.
- Sturdy, but do not enclose or “suffocate” the tablet unnecessarily.
- A front bezel is optional; a stable tray or partial wrap is acceptable.
- Retention should be more secure than an occasional snap-out arrangement.
- Outside corners should be lightly rounded/filleted so they are not sharp.
- The right side should be solid and fully enclosed in the front/oblique view, not partially exposing the tablet edge or recessed USB-C pocket; it must still accommodate the USB-C connection and rearward cable turn while supporting slide-in tablet installation.

## Measurements still needed before a close-fitting final design

- Confirm the flat cable's width and thickness axes; reconcile 0.7 mm versus approximately 0.6 mm.
- Confirm the 9.6 mm and `2` markings on the downstream connector body, including axis and units.
- Confirm tablet button, speaker, camera, and microphone locations relative to any rail, bezel, or stop.
- Confirm available tube engagement length.
- Confirm printer, nozzle, material, build volume, and intended print orientation.
