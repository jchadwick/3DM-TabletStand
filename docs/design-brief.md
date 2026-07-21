# Tablet Stand Design Brief

## Goal

Create a simple, sleek, sturdy FDM-printable holder for a 2024 onn. 8-inch tablet. The assembly will live permanently on top of a vertical 32 mm OD tube. The tablet should be securely retained without a bulky enclosure or unnecessary obstruction of its surfaces.

## Supplied references

- `reference/tablet/tinker.obj`: Tinkercad export of the tablet, with a measured axis-aligned envelope of 200 x 123 x 8.4 mm.
- `reference/tablet/obj.mtl`: material definition accompanying the tablet OBJ.
- `reference/images/slim-usb-c-cable.png`: visual reference for the low-profile USB-C lead.
- `reference/images/tilt-reference.png`: an early side-view sketch retained as source history; its 10-degrees-above-horizontal interpretation is superseded by the kiosk-angle correction below.

Source file SHA-256 checksums:

```text
2c9b8806e64e52a87e7ebacec791b912b9a4fb774c618ab4b1893b57f28cefe8  tinker.obj
fcf8ac13a37b9b38b3052e32e8f2407ed103fb5f62b3468fe42578f922007f8b  obj.mtl
575f7f808ad992e87ae410be5e9742a2c2b65725099cb73130cf4a423226180e  slim-usb-c-cable.png
de3a6b13c21a19f52a0c6697288e47ec1d9f3da20c9b4bcc9ad1b73e86abc622  tilt-reference.png
```

## Geometry and orientation

- Tablet nominal envelope: 200 mm wide, 123 mm deep, and 8.4 mm thick.
- The tablet is landscape when seen by the user.
- The bottom long edge is closest to the user and lower.
- The top long edge is farther from the user and higher.
- The screen plane is **10 degrees back from vertical**, equivalently **80 degrees above horizontal**, and faces the user like a kiosk.
- The top long edge is farther from the user and higher; the bottom long edge is nearer and lower.
- Across the 123 mm tablet depth, an 80-degree rise produces approximately 121.1 mm of vertical elevation and 21.4 mm of horizontal setback between the long edges.
- The USB-C connection is at the midpoint of the right 123 mm edge when viewed from the screen side.

## Pedestal interface

- The existing tube is vertical with a 32 mm outside diameter.
- A previously test-printed cylinder with a 32.2 mm inside diameter fits the tube tightly; preserve that functional ID.
- The stand should use a closed sleeve and install by sliding straight down over the accessible tube end.
- Because the tablet is nearly vertical, the sleeve must sit behind the screen plane rather than intersecting it. Version 1 offsets the sleeve axis 24 mm behind the tablet plane and ties it to the central back support with two ribs.

## Tablet support and retention

Concepts considered:

- **Open gravity tray:** easiest to print and least obstructive, but not secure enough against bumps or lifting.
- **Flexible snap clips:** compact and removable, but rejected because stronger retention is wanted and the printer/filament do not produce consistently tight tolerances.
- **Full screw-together bezel:** very secure, but uses more material, obstructs more of the tablet, and requires detailed cutouts for buttons, speakers, cameras, and screen margins.
- **Selected direction — slide-in rails with one-screw end stop:** narrow fixed rails overlap only the tablet's outer bezel. The tablet slides into a deliberately forgiving channel, and a removable stop secured by one M3 screw blocks the insertion edge. Soft foam or felt can remove rattle and protect the tablet without relying on a precision printed fit.

The selected direction should keep the rear largely open for airflow and material efficiency. Edge rails and the end stop must avoid the USB-C connection and should not cover unknown button, camera, or speaker locations until those locations are verified.

## USB-C routing

- Port location: center of the tablet's right short edge.
- Flat cable section: 0.6 mm thick for approximately 2 in (50.8 mm).
- Plug projection from tablet: 0.256 in (6.50 mm).
- The original width value remains ambiguous, so the first design should use a generous plug chamber and cable groove rather than a close-fitting captive tunnel.
- The right-angle adapter turns immediately behind the tablet. Its photo-marked 51.4 mm pigtail and downstream connection stay behind the open back, then the complete cable routes through wide 18 mm connector-pass eyelets beside the sleeve.
- The downstream cable is confirmed as 3.45 mm diameter round braided wire. Version 1 uses no cable-sized clips or channels; the sleeve-side eyelet openings remain fully outside the sleeve wall and tested bore.
- Any turn in the cable route should be broad and radiused. The printed holder must not clamp the thin flat section, force a sharp bend at the connector, require the larger downstream connector to pass through a captive tunnel, or cut into the tested 32.2 mm sleeve bore.

## First concept intent

- A lightweight skeletal back support with narrow perimeter rails.
- A removable end stop retained by one M3 screw.
- A vertical 32.2 mm ID sleeve centered left-to-right and offset behind the tablet plane.
- Low-profile gussets blending the sleeve into the back support.
- A right-edge USB-C pocket that lets the right-angle pigtail turn behind the tablet, plus a largely hidden and serviceable rear route to the tube sleeve.
- Rounded exterior edges and a visually quiet, symmetric form except where the cable route requires asymmetry.

## Measurements to validate before final print

- Flat cable and connector body width.
- The meaning/axis of the photo-marked 9.6 mm connector dimension.
- Exact locations of power/volume buttons, speakers, cameras, and microphones near any retaining rail.
- Desired sleeve engagement length and available unobstructed tube length.
- M3 screw length and whether a nut, heat-set insert, or tapped plastic hole will be used.
- Printer nozzle, layer height, build volume, filament type, and preferred print orientation.
- Fit allowance around the tablet, ideally checked with a small rail-and-stop test coupon before printing the full holder.

## Version 1 implementation

The first parametric concept is generated by `cad/tablet_stand_v1.py`. It uses a 1.0 mm total allowance in X and Y and 0.8 mm in Z, narrow U-shaped rails on the near and far long edges, internal right corner stops behind a closed USB-C plug housing, and a full-height removable left end stop with an M3 clearance hole. The main body includes a 50 mm sleeve body plus 4 mm upper junction, 32.2 mm ID, 4 mm wall, 51 mm of clear tube engagement, a 3 mm solid seating cap, and two gusset ribs. The corrected kiosk geometry places the screen 80 degrees above horizontal and offsets the sleeve axis 24 mm behind the tablet plane.

With the corrected kiosk orientation and closed cable end, the installed main-body envelope is approximately 216.0 x 66.42 x 130.49 mm. Both exported STL parts are single watertight solids. Version 1 is a form and fit concept—not yet a production-ready print—and should be revised after checking the physical tablet's controls and testing a small fit coupon.
