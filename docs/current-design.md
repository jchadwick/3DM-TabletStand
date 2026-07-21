# Current Design Specification

## Purpose and status

The project is a simple, sleek, FDM-printable landscape holder for a 2024 onn. 8-inch tablet. It mounts permanently to the accessible top end of a vertical 32 mm OD tube. Version 1 is a concept for review and fit testing; it is not yet print-ready.

## Orientation and coordinates

The user views the tablet in landscape. The screen faces the user; the bottom long edge is lower and nearer; the top long edge is higher and farther away. The screen is **10 degrees back from vertical**, which is **80 degrees above horizontal**. Do not reintroduce the superseded nearly-flat 10-degrees-above-horizontal interpretation.

In the CadQuery model, X runs left (−) to right/USB-C side (+), Y runs user/bottom (−) to far/top (+), and Z runs up. The tablet plane is rotated +80 degrees about X.

## Fit-critical dimensions

| Feature | Value | Status |
|---|---:|---|
| Tablet envelope | 200 × 123 × 8.4 mm | Measured from supplied OBJ |
| Tablet allowance | 1.0 mm total in X/Y; 0.8 mm in Z | V1 design value; requires coupon |
| Existing tube | 32.0 mm OD | User measurement |
| Sleeve ID | 32.2 mm | User fit-tested; preserve |
| Sleeve OD / wall | 40.2 mm / 4.0 mm | V1 design value |
| Sleeve body / engagement | 50 mm / 51 mm | V1 design value |
| Seating cap | 3.0 mm | V1 deterministic tube stop |
| Sleeve rear offset | 24 mm | Keeps tube out of tablet cavity |
| Retaining hardware | M3 screw | User has M3 screws |
| USB-C plug projection | 6.50 mm | User measurement |
| Flat cable thickness / length | 0.6 mm / about 50.8 mm | User measurement |

## Functional design

- The holder slides down over the tube using a closed cylindrical sleeve with a solid seating cap.
- Two rear gussets connect the rear-offset sleeve to the tablet back support.
- The tablet loads from the left through narrow rails on the long edges.
- A removable left end stop secured by one M3 screw prevents the tablet from sliding out.
- Right-side corner stops leave the center of the right edge open for USB-C. Keep cable routing broad and non-captive because its width is not yet verified.
- Keep the rear open for material efficiency, airflow, and access. Do not convert this to a full bezel without confirming all device clearance zones.

## Known unknowns before a full print

- Flat cable and connector-body width.
- Power, volume, speaker, camera, microphone, and any other edge clearances.
- M3 screw length and whether it uses a nut, heat-set insert, or printed pilot hole.
- Unobstructed tube length above its existing mounting point.
- Printer, nozzle, material, usable build area, and desired print orientation.
