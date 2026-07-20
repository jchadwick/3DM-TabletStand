# Tablet Stand Design Brief

## Goal

Create a simple, sleek, sturdy FDM-printable holder for a 2024 onn. 8-inch tablet. The assembly will live permanently on top of a vertical 32 mm OD tube. The tablet should be securely retained without a bulky enclosure or unnecessary obstruction of its surfaces.

## Supplied references

- `reference/tablet/tinker.obj`: Tinkercad export of the tablet, with a measured axis-aligned envelope of 200 x 123 x 8.4 mm.
- `reference/tablet/obj.mtl`: material definition accompanying the tablet OBJ.
- `reference/images/slim-usb-c-cable.png`: visual reference for the low-profile USB-C lead.
- `reference/images/tilt-reference.png`: the accepted side-view interpretation of the 10-degree tilt.

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
- The screen plane is 10 degrees above horizontal and faces upward/toward the user.
- Rotating the 123 mm tablet depth through 10 degrees produces approximately 21.4 mm of elevation change between the two long edges.
- The USB-C connection is at the midpoint of the right 123 mm edge when viewed from the screen side.

## Pedestal interface

- The existing tube is vertical with a 32 mm outside diameter.
- A previously test-printed cylinder with a 32.2 mm inside diameter fits the tube tightly; preserve that functional ID.
- The stand should use a closed sleeve and install by sliding straight down over the accessible tube end.
- The sleeve should meet the underside near the tablet's center of gravity, with broad transitions or ribs to resist bending and rotation without looking bulky.

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
- The original width value remains ambiguous, so the first design should use a generous, open-sided relief rather than a close-fitting captive tunnel.
- Any turn in the cable route should be broad and radiused. The printed holder must not clamp the thin flat section or force a sharp bend at the connector.

## First concept intent

- A lightweight skeletal back support with narrow perimeter rails.
- A removable end stop retained by one M3 screw.
- A centered vertical 32.2 mm ID sleeve below the tablet.
- Low-profile gussets blending the sleeve into the back support.
- An open USB-C relief and cable path on the right side.
- Rounded exterior edges and a visually quiet, symmetric form except where the cable route requires asymmetry.

## Measurements to validate before final print

- Flat cable and connector body width.
- Exact locations of power/volume buttons, speakers, cameras, and microphones near any retaining rail.
- Desired sleeve engagement length and available unobstructed tube length.
- M3 screw length and whether a nut, heat-set insert, or tapped plastic hole will be used.
- Printer nozzle, layer height, build volume, filament type, and preferred print orientation.
- Fit allowance around the tablet, ideally checked with a small rail-and-stop test coupon before printing the full holder.

