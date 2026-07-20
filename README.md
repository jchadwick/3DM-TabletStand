# 3DM Tablet Stand

A 3D-printable, pedestal-mounted holder for a 2024 onn. 8-inch tablet. The holder is intended to slide onto an existing vertical 32 mm OD tube and present the tablet in landscape orientation at 10 degrees above horizontal.

The project is currently in the design-brief stage. The source tablet mesh and visual references are preserved under [`reference/`](reference/), and the decisions from the initial design conversation are recorded in [`docs/design-brief.md`](docs/design-brief.md).

## Locked design inputs

- Tablet envelope from the supplied OBJ: **200 x 123 x 8.4 mm**.
- Landscape orientation; USB-C is centered on the right short edge as viewed from the screen side.
- Existing support: **32 mm OD vertical tube**.
- Proven printed fit: **32.2 mm ID closed sleeve**, installed by sliding the holder down over the tube end.
- Screen angle: **10 degrees above horizontal**, with the near/bottom edge lower and the far/top edge higher.
- Styling: simple and sleek, with sturdy support but minimal enclosure.
- Retention direction: slide-in edge rails with a removable one-screw end stop using M3 hardware.
- Cable: a slim plug protrudes 0.256 in (6.50 mm) from the tablet; its flat cable section is 0.6 mm thick for roughly 2 in before transitioning to braided cable.

## Repository layout

```text
docs/                 Design decisions and open measurements
reference/images/     Uploaded visual references
reference/tablet/     Supplied OBJ and material file
```

## Status

1. Preserve source material and design brief.
2. Generate the first parametric CAD concept and preview.
3. Test-print critical interfaces before committing to a full-size print.

