# ADR-0001: Split V2 into support-minimized printable modules

- Status: accepted
- Date: 2026-07-28
- Deciders: Project maintainers
- Supersedes: None
- Superseded by: None

## Context

The V1 main STL combines a tablet cradle tilted 80 degrees above horizontal,
a vertical closed tube sleeve, rear gussets, and cable clips. No single FDM
orientation serves all of those axes: printing the sleeve vertically leaves
the long cradle rails and sleeve seating-cap ceiling support-dependent, while
laying the cradle flat turns the fit-critical 32.2 mm bore nearly horizontal.
Support contact on the cradle rails can also consume the 0.5 mm-per-side tablet
clearance. The user requested a V2 optimized for a practical layout with
limited supports while preserving all confirmed tablet, tube, cable, and tilt
dimensions.

## Decision

V2 will be a four-part main assembly:

1. a cradle printed with its rear frame face on the bed;
2. a rear tilt bracket printed on a horizontal sleeve-interface foot;
3. a closed sleeve printed upside down on a flange, with the tube-entry bore
   open upward; and
4. the removable left end stop printed screen-lip face down.

The cradle and tilt bracket will use a broad adhesive bond indexed by matching
74 mm side edges and their shared top edge. The bracket foot and sleeve flange
will use a second broad adhesive bond indexed by matching 60 mm side edges and
their shared front edge. Both joints receive matching shallow cross grooves and
one identical printed alignment key; the key STL is printed twice. The tilt
bracket owns the two open braided-cable clips so the cradle can retain a flat
print face. The removable left end stop remains the only M3-fastened part. V1
remains preserved and reproducible.

## Consequences

### Positive

- The 32.2 mm sleeve bore prints vertically without internal support under its
  3 mm seating cap.
- The cradle's fit-critical long rails print vertically from a broad flat frame
  instead of against tall support towers.
- Support is limited to small bracket/clip details and short bridges that are
  accessible for cleanup.
- Each module can be reprinted independently after a fit change.
- The structural assembly does not depend on unconfirmed screw lengths, insert
  types, or nut access.
- The two keyed glue joints positively constrain X/Y alignment during cure.

### Negative

- Assembly adds two adhesive preparation, alignment, clamping, and cure steps.
- The physical assembly has six pieces because the alignment key is printed
  twice in addition to the four main modules.
- The bonded main-body joints are not intended for routine disassembly.
- Adhesive selection and surface preparation depend on the chosen filament.
- More parts and bonded interfaces create more tolerance stack-up than V1.
- V2 remains a concept until the end-stop fastener, controls, printer, material,
  adhesive, and fit coupons are physically verified.

## Alternatives considered

### Keep the monolithic V1 main part

Rejected because its best orientation still places roughly 7,700 mm2 of
downward-facing surface beyond a 45-degree support rule, including the
fit-critical upper rail and sleeve-cap ceiling.

### Lay the monolithic holder flat

Rejected because it makes the 51 mm sleeve nearly horizontal and introduces
support and distortion inside the user-tested 32.2 mm bore.

### Split only the cradle from an integrated sleeve-and-gusset pedestal

Rejected because the remaining pedestal still combines horizontal, vertical,
and tilted mounting faces without a broad support-free print datum.

## Verification

- `.venv/bin/python cad/tablet_stand_v2.py`
- `.venv/bin/python scripts/validate_model_v2.py`
- `.venv/bin/python scripts/render_cadquery_preview_v2.py`
- `build/v2/tablet_stand_v2_print_layout.png` visually shows every printable
  STL on its intended bed face, with the alignment-key STL printed twice.
- Validation requires one watertight connected component per STL, preserves the
  32.2 mm bore and 51 mm engagement, verifies both keyed glue joints and the
  single M3 end-stop alignment, and rejects installed part interference.
