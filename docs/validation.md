# Build and Validation

Run the following after any CAD or rendering change. The root [`AGENTS.md`](../AGENTS.md) requires the `parametric-3d-printing` skill before performing such work.

```bash
.venv/bin/python cad/tablet_stand_v1.py
.venv/bin/python scripts/validate_model.py
.venv/bin/python scripts/render_cadquery_preview.py
.venv/bin/python cad/tablet_stand_v2.py
.venv/bin/python scripts/validate_model_v2.py
.venv/bin/python scripts/render_cadquery_preview_v2.py
```

The first three commands preserve and verify V1. The V2 commands regenerate its STEP, five STL files, parameter JSON, installed preview, rear detail, print layout, and multiview sheet. V2 validation checks the kiosk angle, clear 32.2 mm tube path, 51 mm engagement, solid seating cap, flat print datums, adhesive-joint groove alignment, two-copy cross key, relocated end-stop screw, required files, and one watertight component per STL. Both preview scripts render directly from in-memory CadQuery tessellation; they do not import an STL.

Before marking a revision print-ready, visually inspect the generated previews, confirm every requested feature remains visible, and test-slice every manufacturing STL in its documented orientation. A full V2 print also requires physical fit coupons for the rail clearance, end stop, tube sleeve, cable route, and glue-joint alignment key, plus an adhesive test using the selected filament.
