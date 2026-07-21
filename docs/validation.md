# Build and Validation

Run the following after any CAD or rendering change. The root [`AGENTS.md`](../AGENTS.md) requires the `parametric-3d-printing` skill before performing such work.

```bash
.venv/bin/python cad/tablet_stand_v1.py
.venv/bin/python scripts/validate_model.py
.venv/bin/python scripts/render_cadquery_preview.py
```

The first command regenerates the V1 STEP, STL, and parameter JSON. The validation script checks the active kiosk angle, clear 32.2 mm tube path, solid seating cap, required generated files, and watertight STL solids. The preview script renders directly from in-memory CadQuery tessellation; it does not import an STL.

Before marking a revision print-ready, visually inspect the generated previews, confirm every requested feature remains visible, and test-slice the model. A full print also requires a physical fit coupon for the rail clearance, end stop, tube sleeve, and cable route.
