# Build and Validation

Run the following after any CAD or rendering change. The root [`AGENTS.md`](../AGENTS.md) requires the `3d-model` skill before performing such work.

```bash
.venv/bin/python cad/tablet_stand_v2.py
.venv/bin/python scripts/validate_model_v2.py
.venv/bin/python scripts/render_cadquery_preview_v2.py
```

These commands regenerate the active STEP, production and coupon STL files, parameter JSON, installed preview, rear detail, print layout, and multiview sheets. Validation checks the kiosk angle, tablet and button clearances, USB-C route, clear 32.2 mm tube path, 51 mm engagement, solid seating cap, flat print datums, adhesive-joint groove alignment, two-copy cross key, both screw-free tapered rail plugs and sockets, closed seating ends, root/tip clearances, minimum receiver walls, collision-free horizontal insertion travel, required files, and one watertight component per STL. The preview script renders directly from in-memory CadQuery tessellation; it does not import an STL.

On a headless macOS session, set `CAD_PREVIEW_HEADLESS=1` for the preview command. This uses the VTK depth-buffered fallback while preserving direct in-memory CadQuery tessellation.

Before marking a revision print-ready, visually inspect the generated previews, confirm every requested feature remains visible, and test-slice every manufacturing STL in its documented orientation. A full V2 print also requires physical fit coupons for the rail clearance, end stop, tube sleeve, cable route, and glue-joint alignment key, plus an adhesive test using the selected filament.
