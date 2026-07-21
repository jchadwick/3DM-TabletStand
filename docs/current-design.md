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
| Sleeve vertical placement | Bottom level with holder's lower long edge (Z = -64.53 mm) | User-requested alignment; rear assembly lowered 14.53 mm |
| Retaining hardware | M3 screw | User has M3 screws |
| USB-C plug projection | 6.50 mm | User measurement |
| Flat cable thickness / length | 0.6 mm / about 50.8 mm | User measurement |
| Right-angle pigtail reach | 51.4 mm | Marked on user photo; endpoint definition should be confirmed before a close fit |
| Downstream connector body | 9.6 mm marked dimension | User photo; measurement axis/meaning still to confirm |
| Round braided cable diameter | 3.45 mm | User measurement |
| USB-C plug-pocket depth | 8.0 mm clear | 6.50 mm projection plus provisional clearance |
| Rear turn slot | 3 × 16 mm | Broad opening for the 0.6 mm pigtail to turn behind the tablet |
| Braided-cable channel | 4.15 mm ID / 2.8 mm snap opening | 0.70 mm total clearance around confirmed cable diameter |
| Sleeve channel embed / remaining wall | 1.2 mm / 2.8 mm minimum | Keeps the 32.2 mm tube bore intact |
| Exposed corner radii | 1.2 mm rails/walls; 0.8 mm lips | Rounded to remove sharp outside corners |

## Functional design

- The holder slides down over the tube using a closed cylindrical sleeve with a solid seating cap.
- The complete rear sleeve/collet assembly is lowered so its bottom is level with the installed holder's lower long edge. The sleeve dimensions and proven tube fit are unchanged.
- Two rear gussets connect the rear-offset sleeve to the tablet back support.
- The tablet loads from the left through narrow rails on the long edges.
- A removable left end stop secured by one M3 screw prevents the tablet from sliding out.
- Internal right-side corner stops locate the tablet while accommodating the 6.50 mm-projecting USB-C plug.
- The right-angle adapter turns immediately around the tablet's right edge and onto the open back; the flat pigtail and its downstream connection should be largely hidden behind the tablet rather than leaving straight out through the right wall.
- The right outer wall is solid. A broad slot through the rear floor of the plug pocket lets the 0.6 mm pigtail turn behind the tablet.
- The 3.45 mm braided section snaps into two open C-clips on the rear spine, spans downward and backward through the open rear to the lowered sleeve channel, then snaps into that rear-facing external channel and exits beside the tube. The 9.6 mm-marked connector body remains accessible outside all captive features.
- The external sleeve channel has 4.15 mm internal clearance and a 2.8 mm snap opening. Its shallow 1.2 mm embed leaves at least 2.8 mm of the original 4 mm sleeve wall and does not intersect the tested 32.2 mm bore.
- Exposed rail, end-wall, and removable-stop corners are lightly rounded so the case does not present sharp outside corners.
- Keep the rear open for material efficiency, airflow, and access. Do not convert this to a full bezel without confirming all device clearance zones.

## Known unknowns before a full print

- Flat cable and connector-body width.
- Whether the photo's 9.6 mm annotation is connector width, height, or another measurement.
- Power, volume, speaker, camera, microphone, and any other edge clearances.
- M3 screw length and whether it uses a nut, heat-set insert, or printed pilot hole.
- Unobstructed tube length above its existing mounting point.
- Printer, nozzle, material, usable build area, and desired print orientation.
