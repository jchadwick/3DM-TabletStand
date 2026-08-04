# ADR-0002: Replace M3 end stop with screw-free slide stop

- Status: superseded
- Date: 2026-08-02
- Deciders: Project maintainers
- Supersedes: ADR-0001
- Superseded by: ADR-0003

## Context

ADR-0001 established the support-minimized four-module V2 layout but retained
one M3 screw for the removable left tablet stop. The user rejected that visible
fastener and requested a left edge that installs by sliding downward and remains
removable through a guided fit or optionally permanent with a small amount of
adhesive. After reviewing the first screw-free implementation, the user also
rejected its projecting landing nub, rear hooks, and detent bumps in favor of a
sleek tongue-and-groove joint. The stop must still print separately,
must not collide with either long rail during insertion, and must preserve the
cradle's broad rear print datum. The user also requested softer exposed edges.

## Decision

Retain ADR-0001's cradle, rear-bracket, sleeve, alignment-key, and print-layout
decisions, but replace the M3-mounted end stop with a screw-free top-down slide
stop. Use one continuous captured dovetail: the production cradle receives a
closed-bottom groove and the separate stop receives a matching undersized tongue.
The narrow groove mouth captures the wider tongue head; the internal closed
bottom establishes the seated position. Do not add rear hooks, detent bumps, or
an external lower landing. Adhesive is optional.

Use an exact two-piece production crop to physically test the slide clearance,
dovetail capture, and closed-bottom seating before the revised full cradle is printed.
Soften exposed perimeter, rail, lip, and stop edges with the active fillet radii
without changing the confirmed tablet-cavity allowances.

## Consequences

### Positive

- Eliminates the only visible mechanical fastener and its unconfirmed screw
  length and pilot strategy.
- The stop remains independently replaceable and can be glued only if desired.
- The closed-bottom groove gives a deterministic seated position while the
  dovetail prevents the stop from peeling away from the cradle.
- Removing the external landing, hooks, and bumps restores a clean rounded
  lower-left silhouette and the cradle's 215 × 130 mm envelope.
- Rounded longitudinal edges make the printed holder less sharp in hand.

### Negative

- The friction fit is printer- and material-dependent and requires a physical
  PLA coupon before the full cradle.
- The long, enclosed sliding surfaces remain sensitive to printed PLA clearance
  and must be physically tested before committing to the full cradle.

## Alternatives considered

### Retain the local-Z M3 screw

Rejected because the user does not want a visible screw or mechanical fastener
on the tablet edge.

### Use separate snap hooks, detents, and a lower landing

Initially implemented, then rejected because the small features and projecting
nub looked vestigial and bulky compared with the requested clean tongue-and-groove
joint.

### Glue the stop permanently with no guides

Rejected because it would make alignment less repeatable and remove the option
to replace or service the tablet without breaking a bond.

## Verification

- `.venv/bin/python cad/tablet_stand_v2.py`
- `.venv/bin/python scripts/validate_model_v2.py`
- `.venv/bin/python scripts/render_cadquery_preview_v2.py`
- Validation samples the complete insertion travel and requires zero solid
  intersection at every sampled offset.
- `build/v2/tablet_stand_v2_left_stop_multiview.png` shows the seated, sliding,
  and transverse dovetail-profile views.
- `tablet_stand_v2_left_slide_coupon_cradle.stl` and
  `tablet_stand_v2_left_slide_coupon_stop.stl` are watertight exact crops for
  the required physical fit test.
