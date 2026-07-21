# Version 1 outputs

This folder contains generated outputs from `cad/tablet_stand_v1.py` and `scripts/render_preview.py`.

- `tablet_stand_v1.step`: two-part CAD assembly with the removable end stop installed.
- `tablet_stand_main.stl`: watertight main holder, sleeve, and gussets in installed orientation.
- `tablet_stand_end_stop.stl`: watertight removable stop in its local modeling orientation.
- `tablet_stand_end_stop_installed.stl`: preview-only copy positioned in the assembly.
- `model_parameters.json`: key dimensions in machine-readable form.
- `tablet_stand_v1_preview.png`: three-quarter assembly preview using the supplied tablet OBJ.
- `tablet_stand_v1_side.png`: edge-on view emphasizing the slope and hidden cable transition.
- `tablet_stand_v1_usb_detail.png`: rear view of the hidden pigtail and three 18 mm connector-pass eyelets.
- `tablet_stand_v1_multiview.png`: combined design-review preview.

## Validation

The preview PNGs are rendered directly from in-memory CadQuery tessellation by `scripts/render_cadquery_preview.py` using Trimesh's depth-buffered renderer; they do not reread the exported STL. Trimesh validation reports one watertight connected component for each printable STL. The kiosk-oriented main envelope is 216.0 x 66.42 x 130.49 mm; the end-stop local envelope remains 10.2 x 130.0 x 19.2 mm.

## Before printing

This first pass is intended for design review. Confirm button/speaker/camera clearances, verify the complete connector passes freely through an 18 mm coupon, and confirm M3 screw length. Test-slice the 216 mm main-body span against the printer's usable bed—not merely its nominal bed size—and decide whether the integrated tilted sleeve needs support or should become a separately printed bracket in version 2.
