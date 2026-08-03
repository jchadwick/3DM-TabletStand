# ADR-0002: Replace M3 end stop with screw-free slide stop

- Status: accepted
- Date: 2026-08-02
- Deciders: Project maintainers
- Supersedes: ADR-0001
- Superseded by: None

## Context

ADR-0001 established the support-minimized four-module V2 layout but retained
one M3 screw for the removable left tablet stop. The user rejected that visible
fastener and requested a left edge that installs by sliding downward, seats on
a cradle projection, and remains removable through friction or optionally
permanent with a small amount of adhesive. The stop must still print separately,
must not collide with either long rail during insertion, and must preserve the
cradle's broad rear print datum. The user also requested softer exposed edges.

## Decision

Retain ADR-0001's cradle, rear-bracket, sleeve, alignment-key, and print-layout
decisions, but replace the M3-mounted end stop with a screw-free top-down slide
stop. The production cradle receives a lower-left landing ledge, a 4 mm rail-free
entry lead, and two shallow detent grooves. The separate stop receives matching
friction ribs plus two hooks that travel below the cradle's rear face and prevent
lateral release. The stop seats against the lower ledge; adhesive is optional.

Use an exact two-piece production crop to physically test the slide, detents,
rear-hook clearance, and final seating before the revised full cradle is printed.
Soften exposed perimeter, rail, lip, and stop edges with the active fillet radii
without changing the confirmed tablet-cavity allowances.

## Consequences

### Positive

- Eliminates the only visible mechanical fastener and its unconfirmed screw
  length and pilot strategy.
- The stop remains independently replaceable and can be glued only if desired.
- The lower landing gives a deterministic seated position while the rear hooks
  prevent the stop from peeling away from the cradle.
- Rounded longitudinal edges make the printed holder less sharp in hand.

### Negative

- The friction fit is printer- and material-dependent and requires a physical
  PLA coupon before the full cradle.
- The cradle grows to 217 mm wide and therefore retains little spare X margin
  on the configured 220 mm bed.
- The stop's small rear hooks require inspection in the slicer and careful
  removal from the bed.

## Alternatives considered

### Retain the local-Z M3 screw

Rejected because the user does not want a visible screw or mechanical fastener
on the tablet edge.

### Use a snap tab without a lower landing

Rejected because a cantilever snap would concentrate strain in PLA and provide
a less deterministic seated position than a guided slide resting on a ledge.

### Glue the stop permanently with no guides

Rejected because it would make alignment less repeatable and remove the option
to replace or service the tablet without breaking a bond.

## Verification

- `.venv/bin/python cad/tablet_stand_v2.py`
- `.venv/bin/python scripts/validate_model_v2.py`
- `.venv/bin/python scripts/render_cadquery_preview_v2.py`
- Validation samples the complete insertion travel and permits only the tiny
  intentional friction-rib interference before confirming zero final overlap.
- `build/v2/tablet_stand_v2_left_stop_multiview.png` shows the seated, sliding,
  and rear-hook views.
- `tablet_stand_v2_left_slide_coupon_cradle.stl` and
  `tablet_stand_v2_left_slide_coupon_stop.stl` are watertight exact crops for
  the required physical fit test.
