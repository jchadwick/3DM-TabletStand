# ADR-0003: Replace dovetail stop with twin tapered rail plugs

- Status: accepted
- Date: 2026-08-04
- Deciders: Project maintainers
- Supersedes: ADR-0002
- Superseded by: None

## Context

ADR-0002 replaced the visible M3 fastener with a top-down captured dovetail. The
physical coupon could not be cleaned successfully: support was trapped in the
tight groove, while an unsupported attempt collapsed and strung badly with the
user's dry but difficult PLA. The left cap still needs positive alignment and
friction retention without screws, brittle snap hooks, or inaccessible support.

## Decision

Replace the dovetail with two horizontally inserted tapered plugs, one aligned
with each long-edge rail. Each plug has a support-free house profile and tapers
from 2.15 × 2.95 mm at its root to 1.80 × 2.60 mm at its tip over 12 mm. It
enters a matching 2.40 × 3.20 mm open-ended socket with a 45-degree roof and a
closed seating end, providing 0.25 mm total root clearance and 0.60 mm total tip
clearance. Reinforce both rail ends and add 45-degree underside ramps. Preserve
the measured concealed button groove, rounded screw-free silhouette, and
optional adhesive strategy.

Print the socket and plug coupons as two separate, support-free jobs before
re-slicing the complete cradle and cap.

## Consequences

### Positive

- Removes all support from the fit surfaces and leaves both socket mouths open
  for inspection and cleanup.
- Uses two rail-aligned contacts to resist cap rotation while preserving the
  clean rounded edge and screw-free assembly.
- Tapered lead-in reduces sensitivity to the user's string-prone PLA while the
  socket backs provide deterministic seating.

### Negative

- The cradle becomes 3.6 mm wider across Y because of the two subtle receiver
  reinforcements.
- Friction remains process-dependent and requires a physical coupon before the
  long cradle print.
- The full cradle and cap G-code must be regenerated after the coupon passes.

## Alternatives considered

### Retain the supported dovetail

Rejected because the physical coupon showed that support could not be removed
reliably from the narrow captured groove.

### Use snap hooks or detents

Rejected because the user requested a sleek joint without exposed catches, and
small PLA hooks would be brittle and printing-sensitive.

### Use magnets or other hardware

Rejected because the requested closure should not require mechanical hardware.

### Glue the cap with no alignment features

Rejected because it would make placement less repeatable and make service or
replacement more destructive. The twin plugs align the cap whether or not the
user later chooses a drop of glue.

## Verification

- `.venv/bin/python cad/tablet_stand_v2.py`
- `.venv/bin/python scripts/validate_model_v2.py`
- `CAD_PREVIEW_HEADLESS=1 .venv/bin/python scripts/render_cadquery_preview_v2.py`
- Validation samples horizontal insertion at six positions, checks zero
  collision, verifies both seating ends and receiver walls, and requires
  watertight production and coupon exports.
- `build/v2/tablet_stand_v2_left_stop_multiview.png` shows seated, exploded,
  and socket-section views.
- The two individual coupon G-code jobs validate without supports or slicer
  stability warnings; a physical fit test remains required.
