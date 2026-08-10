# 3DM Tablet Stand — Agent Instructions

This repository designs a functional, FDM-printable pedestal stand for a 2024 onn. 8-inch tablet. Treat the dimensions and active decisions in this file as the minimum context required before making changes.

## Mandatory model workflow

For **every** change to model geometry, fit/tolerance values, CAD exports, or model previews/renders:

1. First read and follow the local [`3d-model` skill](/Users/jchadwick/.agents/skills/3d-model/SKILL.md).
2. Use CadQuery as the parametric source of truth; do not edit generated STL or STEP files directly.
3. Build the model, validate watertight output, generate a multi-view preview, inspect it, and update the documentation in the same change.
4. Record any confirmed measurement or design decision in `docs/decision-log.md`; update `docs/current-design.md` and this file when it changes the active specification.
5. Physical measurements and fit tests from the user override visual estimates, generic specifications, or web research.

Routine previews use direct in-memory CadQuery tessellation through the active `scripts/render_cadquery_preview_v3.py` and shared `scripts/render_cadquery_helpers.py`; generated STL is a manufacturing export, not an input to the preview.

## Active design — do not regress

| Item | Active value / decision |
|---|---|
| Tablet | 2024 onn. 8-inch; supplied OBJ envelope is **200 × 123 × 8.4 mm** |
| Tablet fit | **1.0 mm total X/Y allowance; 0.8 mm Z allowance** — restored after the zero-nominal Y/Z physical test proved too tight |
| Orientation | Landscape; screen faces the user |
| Screen tilt | **10° back from vertical / 80° above horizontal** — not 10° above horizontal |
| Edge direction | Bottom long edge is lower and closer to user; top long edge is higher and farther away |
| Support tube | Existing vertical **32.0 mm OD** tube |
| Tube fit | **32.2 mm ID** is user-tested and intentionally tight |
| Sleeve | Closed cylindrical sleeve slides down over an accessible tube end; 40.2 mm OD, 4.0 mm wall, 51 mm clear engagement, 3.0 mm seating cap |
| Sleeve placement | Centered left-to-right and **24 mm behind the tablet plane**; never move it into the tablet cavity |
| Sleeve vertical alignment | Sleeve/collet bottom is level with the holder's lower long edge at **Z = -64.53 mm**; rear assembly is 14.53 mm below its prior position |
| Tablet retention | In V3, seat the tablet's USB-C/right edge in the fixed right wing, slide the fully enclosed left wing +X until its three integral tongues reach the closed socket seats, then insert one removable tapered cross-wedge through the lower joint. Pull the wedge and slide the wing off for service. There is no separate cap, cradle adhesive, hook, snap detent, or nub |
| USB-C | Center of right short edge from the front; one **16 mm wide × 8 mm deep** open rectangle replaces the undersized T-shaped rear-floor opening and spans from tablet cavity to outer wall |
| Cable | Right-angle pigtail is photo-marked 51.4 mm long; its 0.6 mm flat section and downstream connection stay behind the tablet, then the confirmed 3.45 mm round braided cable routes through open rear clips to the sleeve |
| Sleeve cable channel | Rear-facing snap-in channel on the outside of the sleeve: 4.15 mm ID, 2.8 mm opening, 1.2 mm embed; preserves at least 2.8 mm of sleeve wall and the full 32.2 mm bore |
| Clip-to-channel route | Preserve the clips; the free cable span drops outside the right gusset, sweeps behind the sleeve, and enters the channel through its rear opening—never route previewed cable through solids |
| V2 module split (historical geometry basis) | Flat-print cradle, foot-down rear tilt bracket, and flange-down/bore-up sleeve; V3 preserves the bracket and sleeve orientations while replacing the cradle |
| V2 structural joints (historical) | Two adhesive bonds with matching cross grooves and two printed keys; superseded in V3 by a right-wing-only bracket bond plus one retained bracket-to-sleeve key |
| V2 clip ownership | The two open braided-cable clips are on the rear tilt bracket so the cradle retains a complete flat rear print datum |
| V2 print layouts (historical) | Cradle rear face down; bracket foot down; sleeve flange down with tube bore open upward; separate left-cap layout is superseded by V3 |
| V3 cradle split | Active candidate replaces the wide cradle and separate cap with a fully enclosed **125.00 × 135.50 × 14.20 mm left wing** and **111.33 × 139.00 × 14.20 mm right wing**. Both print rear-face-down |
| V3 cradle joint | Three integral tongues insert 18 mm along +X into closed-back right-wing receivers with **0.50 mm total root / 1.10 mm total lead clearance**. One printed 3.70→3.30 mm tapered wedge crosses the lower joint through a support-free 4 × 4 mm channel; the same channel accepts an M3 bolt as a measured-hardware fallback |
| V3 bracket attachment | Rear bracket bonds only to the fixed right cradle wing; do not glue it to the removable left wing. The bracket-to-sleeve bond retains one 35 × 15 × 1.8 mm alignment key (`alignment_key` STL quantity 1) |
| Cable unknown | Photo marks 9.6 mm at the downstream connector body, but the measurement axis remains unconfirmed; keep that connector outside all captive features |
| Button clearance | Power/volume group is **20–60 mm from landscape top-left**, **2 mm wide across tablet thickness**, centered, and **1 mm protruding**; use a concealed inner groove **2 mm high × 1.2 mm deep** from the left slide-in end through **5 mm beyond** the seated group, preserving a solid **1.8 mm exterior rail wall** and the upper retaining lip |
| Outside finish | Softer exposed geometry: 1.45 mm plan-corner radius on rails/walls, 0.95 mm on lips, plus 0.65 mm exposed perimeter/rail edge fillets and 0.45 mm lip edge fillets; the slide stop uses a 1.70 mm outside corner radius and 0.70 mm edge fillet |
| Style | Simple, sleek, skeletal/open-back support; avoid a bulky full enclosure |
| Current status | The glue-free V3 tongue/wedge cradle is built, watertight, validated, rendered, and visually inspected. An exact three-piece lower-joint coupon is exported but not yet sliced or printed. No V3 part has been authorized for printing, and all earlier full-cradle G-code is stale |

Coordinate system in `cad/tablet_stand_v3.py`, `cad/tablet_stand_v2.py`, and `cad/tablet_stand_core.py`: X is tablet left (−) to right/USB-C (+); Y is user/bottom edge (−) to far/top edge (+); Z is up. The tablet is rotated +80° around X.

## Source of truth and generated files

- `cad/tablet_stand_v3.py`: active removable tongue/wedge cradle, exact lock coupon, V3 assembly, print orientations, and exports.
- `cad/tablet_stand_v2.py`: tested unsplit geometry basis retained temporarily for the V3 comparison; archive the V2-only path if V3 is approved.
- `cad/tablet_stand_core.py`: active shared measurements and base cradle/sleeve geometry used by V2.
- `docs/current-design.md`: active human-readable design specification.
- `docs/decision-log.md`: chronological decision history and measurement ledger.
- `docs/design-brief.md`: original context, references, and unresolved details.
- `scripts/validate_model_v3.py`: active V3 insertion-path, tongue/socket, wedge/M3 channel, coupon, fit-preservation, print-layout, and artifact checks.
- `build/v3/`: current V3 review STEP, production/coupon STL exports, parameters, and multi-view previews. The sleeve-joint alignment-key and removable locking-wedge STLs are each printed once.
- `build/v2/`: tested V2 fit-coupon evidence and prior comparison artifacts; do not print its stale full-cradle G-code.
- `reference/tablet/tinker.obj`: user-supplied tablet reference mesh; preserve it unchanged.
- Superseded V1 source, validators, renders, and artifacts remain recoverable from Git commit `560c6e8`; do not restore or maintain them in the active tree.

## Required checks after a model change

```bash
.venv/bin/python cad/tablet_stand_v2.py
.venv/bin/python scripts/validate_model_v2.py
.venv/bin/python cad/tablet_stand_v3.py
.venv/bin/python scripts/validate_model_v3.py
.venv/bin/python scripts/render_cadquery_preview_v3.py
```

Before calling any version final or print-ready, obtain or verify: cable/connector width; button, speaker, camera, and microphone clearances; available tube length; printer, nozzle, filament, build volume, intended print orientation, and adhesive/surface preparation. Preserve the completed rail, button, USB-C, sleeve, cable-channel, and alignment-key fit evidence, and physically pass the exact V3 three-piece tongue/wedge lock coupon before committing to the full holder.

## Printer start workflow

When the user has explicitly authorized a print, check the configured printer camera before asking whether the bed is clear:

1. Query current printer/job status and require the machine to be reachable and ready.
2. Capture a fresh camera snapshot and inspect the complete visible build plate.
3. If the view clearly shows an empty plate with no prior part, tools, clips, or other obstruction, treat that visual inspection as the bed-clear confirmation and start the authorized print without asking the user again.
4. If the camera is unavailable, stale, obstructed, does not show enough of the plate, or the view is ambiguous, do not infer clearance; ask the user before starting.

Camera inspection confirms physical readiness only. It never supplies authorization for a print the user did not request.

## Git workflow

After every significant completed change or action—such as a design decision, CAD/model update, generated artifact update, documentation restructuring, validation-script change, or reference addition—verify the relevant work, commit the complete coherent change set, and push the active branch to GitHub. Do not leave a significant completed change only in the working tree. Use focused, descriptive commit messages and include regenerated CAD artifacts whenever their source changes.

Before committing, inspect `git status` and the diff; preserve unrelated user changes rather than reverting or absorbing them unintentionally. If a push cannot proceed because of authentication, remote divergence, or missing authorization, report the exact blocker and leave the verified commit intact.
