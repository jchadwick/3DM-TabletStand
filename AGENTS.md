# 3DM Tablet Stand — Agent Instructions

This repository designs a functional, FDM-printable pedestal stand for a 2024 onn. 8-inch tablet. Treat the dimensions and active decisions in this file as the minimum context required before making changes.

## Mandatory model workflow

For **every** change to model geometry, fit/tolerance values, CAD exports, or model previews/renders:

1. First read and follow the local [`parametric-3d-printing` skill](/Users/jchadwick/.codex/skills/cad-skill/SKILL.md).
2. Use CadQuery as the parametric source of truth; do not edit generated STL or STEP files directly.
3. Build the model, validate watertight output, generate a multi-view preview, inspect it, and update the documentation in the same change.
4. Record any confirmed measurement or design decision in `docs/decision-log.md`; update `docs/current-design.md` and this file when it changes the active specification.
5. Physical measurements and fit tests from the user override visual estimates, generic specifications, or web research.

Routine previews use direct in-memory CadQuery tessellation through `scripts/render_cadquery_preview.py`; generated STL is a manufacturing export, not an input to the preview. `scripts/render_preview.py` is optional Blender-only presentation tooling.

## Active design — do not regress

| Item | Active value / decision |
|---|---|
| Tablet | 2024 onn. 8-inch; supplied OBJ envelope is **200 × 123 × 8.4 mm** |
| Orientation | Landscape; screen faces the user |
| Screen tilt | **10° back from vertical / 80° above horizontal** — not 10° above horizontal |
| Edge direction | Bottom long edge is lower and closer to user; top long edge is higher and farther away |
| Support tube | Existing vertical **32.0 mm OD** tube |
| Tube fit | **32.2 mm ID** is user-tested and intentionally tight |
| Sleeve | Closed cylindrical sleeve slides down over an accessible tube end; 40.2 mm OD, 4.0 mm wall, 51 mm clear engagement, 3.0 mm seating cap |
| Sleeve placement | Centered left-to-right and **24 mm behind the tablet plane**; never move it into the tablet cavity |
| Sleeve vertical alignment | Sleeve/collet bottom is level with the holder's lower long edge at **Z = -64.53 mm**; rear assembly is 14.53 mm below its prior position |
| Tablet retention | Left-side slide-in through narrow long-edge rails; removable left end stop retained by one M3 screw |
| USB-C | Center of right short edge from the front; the right-angle adapter turns immediately behind the tablet rather than exiting straight out to the right |
| Cable | Right-angle pigtail is photo-marked 51.4 mm long; its 0.6 mm flat section and downstream connection stay behind the tablet, then the confirmed 3.45 mm round braided cable routes through open rear clips to the sleeve |
| Sleeve cable channel | Rear-facing snap-in channel on the outside of the sleeve: 4.15 mm ID, 2.8 mm opening, 1.2 mm embed; preserves at least 2.8 mm of sleeve wall and the full 32.2 mm bore |
| Cable unknown | Photo marks 9.6 mm at the downstream connector body, but the measurement axis remains unconfirmed; keep that connector outside all captive features |
| Outside corners | Lightly rounded: 1.2 mm on exposed rails/walls and 0.8 mm on retaining lips |
| Style | Simple, sleek, skeletal/open-back support; avoid a bulky full enclosure |
| Current status | Version 1 is a reviewed concept, not a production-ready print |

Coordinate system in `cad/tablet_stand_v1.py`: X is tablet left (−) to right/USB-C (+); Y is user/bottom edge (−) to far/top edge (+); Z is up. The tablet is rotated +80° around X.

## Source of truth and generated files

- `cad/tablet_stand_v1.py`: all active parametric geometry and named dimensions.
- `docs/current-design.md`: active human-readable design specification.
- `docs/decision-log.md`: chronological decision history and measurement ledger.
- `docs/design-brief.md`: original context, references, and unresolved details.
- `scripts/validate_model.py`: geometry and artifact checks.
- `build/v1/`: generated STEP, STLs, parameters, and previews. Regenerate after CAD changes; do not hand-edit.
- `reference/tablet/tinker.obj`: user-supplied tablet reference mesh; preserve it unchanged.

## Required checks after a model change

```bash
.venv/bin/python cad/tablet_stand_v1.py
.venv/bin/python scripts/validate_model.py
.venv/bin/python scripts/render_cadquery_preview.py
```

Before calling any version final or print-ready, obtain or verify: cable/connector width; button, speaker, camera, and microphone clearances; M3 screw length plus nut/insert strategy; available tube length; printer, nozzle, filament, build volume, and intended print orientation. Print a small fit coupon before committing to the full holder.

## Git workflow

After every significant completed change or action—such as a design decision, CAD/model update, generated artifact update, documentation restructuring, validation-script change, or reference addition—verify the relevant work, commit the complete coherent change set, and push the active branch to GitHub. Do not leave a significant completed change only in the working tree. Use focused, descriptive commit messages and include regenerated CAD artifacts whenever their source changes.

Before committing, inspect `git status` and the diff; preserve unrelated user changes rather than reverting or absorbing them unintentionally. If a push cannot proceed because of authentication, remote divergence, or missing authorization, report the exact blocker and leave the verified commit intact.
