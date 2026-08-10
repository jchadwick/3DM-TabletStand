"""V3 split-cradle tablet stand concept.

V3 preserves the physically tested V2 tablet, button, USB-C, tube, and cable
geometry.  The wide flat cradle is divided along a support-free stepped seam
into two bed-friendly wings.  The left wing has an integral continuous end
wall, so it replaces the separate V2 cap, plugs, and sockets.  Three loose,
recessed splice keys align the wings during adhesive assembly, while the
existing rear tilt bracket bridges the center of the seam after glue-up.

Coordinates and installed orientation match ``tablet_stand_v2``.
All dimensions are millimeters.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cadquery as cq


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "v3"
sys.path.insert(0, str(ROOT))

from cad import tablet_stand_core as core  # noqa: E402
from cad import tablet_stand_v2 as v2  # noqa: E402


# The stepped seam moves 16 mm across the center spine.  This resists relative
# Y motion without a print-direction undercut or a support-trapping dovetail.
CRADLE_SEAM_OUTER_X = -8.0
CRADLE_SEAM_CENTER_X = 8.0
CRADLE_SEAM_STEP_Y = 35.0
CRADLE_SEAM_CLEARANCE = 0.35

# Three identical keys sit in rear-facing recesses.  Their 7.2 mm-wide grooves
# bridge cleanly under the 10 mm PLA bridging rule for the confirmed process.
CRADLE_SPLICE_GROOVE_LENGTH = 46.0
CRADLE_SPLICE_GROOVE_WIDTH = 7.2
CRADLE_SPLICE_GROOVE_DEPTH = 1.90
CRADLE_SPLICE_KEY_LENGTH = 44.0
CRADLE_SPLICE_KEY_WIDTH = 6.0
CRADLE_SPLICE_KEY_T = 1.60
CRADLE_SPLICE_KEY_EDGE_CHAMFER = 0.40
CRADLE_SPLICE_KEY_RECESS = 0.20
CRADLE_SPLICE_KEY_Y = (-60.5, 0.0, 60.5)
CRADLE_SPLICE_KEY_X = (
    CRADLE_SEAM_OUTER_X,
    CRADLE_SEAM_CENTER_X,
    CRADLE_SEAM_OUTER_X,
)
CRADLE_SPLICE_KEY_QUANTITY = 3

LINEAR_TOLERANCE = 0.05
ANGULAR_TOLERANCE = 0.1


def _seam_mask(left: bool) -> cq.Workplane:
    """Return one clearance-offset half of the stepped XY split mask."""
    margin = 140.0
    y_limit = 90.0
    half_gap = CRADLE_SEAM_CLEARANCE / 2.0
    if left:
        outer_x = CRADLE_SEAM_OUTER_X - half_gap
        center_x = CRADLE_SEAM_CENTER_X - half_gap
        points = (
            (-margin, -y_limit),
            (outer_x, -y_limit),
            (outer_x, -CRADLE_SEAM_STEP_Y + half_gap),
            (center_x, -CRADLE_SEAM_STEP_Y + half_gap),
            (center_x, CRADLE_SEAM_STEP_Y - half_gap),
            (outer_x, CRADLE_SEAM_STEP_Y - half_gap),
            (outer_x, y_limit),
            (-margin, y_limit),
        )
    else:
        outer_x = CRADLE_SEAM_OUTER_X + half_gap
        center_x = CRADLE_SEAM_CENTER_X + half_gap
        points = (
            (outer_x, -y_limit),
            (margin, -y_limit),
            (margin, y_limit),
            (outer_x, y_limit),
            (outer_x, CRADLE_SEAM_STEP_Y + half_gap),
            (center_x, CRADLE_SEAM_STEP_Y + half_gap),
            (center_x, -CRADLE_SEAM_STEP_Y - half_gap),
            (outer_x, -CRADLE_SEAM_STEP_Y - half_gap),
        )
    return (
        cq.Workplane("XY")
        .workplane(offset=-20.0)
        .polyline(points)
        .close()
        .extrude(50.0)
    )


def cradle_splice_grooves() -> cq.Workplane:
    """Return the three shallow rear-face recess cutters."""
    grooves: cq.Workplane | None = None
    for x_pos, y_pos in zip(CRADLE_SPLICE_KEY_X, CRADLE_SPLICE_KEY_Y, strict=True):
        groove = (
            cq.Workplane("XY")
            .workplane(offset=-core.BASE_T - 0.05)
            .rect(CRADLE_SPLICE_GROOVE_LENGTH, CRADLE_SPLICE_GROOVE_WIDTH)
            .extrude(CRADLE_SPLICE_GROOVE_DEPTH + 0.05)
            .translate((x_pos, y_pos, 0.0))
        )
        grooves = groove if grooves is None else grooves.union(groove)
    assert grooves is not None
    return grooves


def integral_left_closure() -> cq.Workplane:
    """Return the continuous rounded left wall and screen-facing cap."""
    cavity_x = core.TABLET_X + core.FIT_X
    cavity_y = core.TABLET_Y + core.FIT_Y
    rail_top = core.TABLET_Z + core.FIT_Z + core.LIP_T
    wall_h = core.BASE_T + rail_top
    cradle_left_x = -(cavity_x + 2.0 * core.WALL_T) / 2.0
    wall_inner_x = cradle_left_x
    wall_outer_x = wall_inner_x - v2.ENDSTOP_OUTER_WALL_X
    wall_center_x = (wall_inner_x + wall_outer_x) / 2.0

    outer_wall = core.softened_plate(
        v2.ENDSTOP_OUTER_WALL_X,
        core.HOLDER_OUTER_Y,
        wall_h,
        -core.BASE_T,
        v2.ENDSTOP_CORNER_R,
        v2.ENDSTOP_EDGE_R,
    ).translate((wall_center_x, 0.0, 0.0))

    # Extend to and slightly overlap the production rail lead-ins.  Because
    # this cap is integral rather than removable, it can close the corner and
    # form one continuous screen-facing short edge across the full holder Y.
    rail_left_x = cradle_left_x + core.LEFT_RAIL_ENTRY_RELIEF_X
    cap_right_x = rail_left_x + 0.35
    cap = core.softened_plate(
        cap_right_x - wall_outer_x,
        core.HOLDER_OUTER_Y,
        core.LIP_T,
        core.TABLET_Z + core.FIT_Z,
        core.LIP_CORNER_R,
        core.LIP_EDGE_R,
    ).translate(((wall_outer_x + cap_right_x) / 2.0, 0.0, 0.0))

    locator: cq.Workplane | None = None
    for locator_y in v2.ENDSTOP_LOCATOR_Y:
        pad = core.softened_plate(
            core.WALL_T,
            v2.ENDSTOP_LOCATOR_Y_SIZE,
            core.TABLET_Z + core.FIT_Z,
            0.0,
            core.EXPOSED_CORNER_R,
            core.EXPOSED_EDGE_R,
        ).translate((cradle_left_x + core.WALL_T / 2.0, locator_y, 0.0))
        locator = pad if locator is None else locator.union(pad)
    assert locator is not None
    return outer_wall.union(cap).union(locator)


def integral_full_cradle() -> cq.Workplane:
    """Return the tested cradle interfaces with the V3 integral left closure."""
    cradle = core.flat_main_holder().union(integral_left_closure())
    bracket_groove = v2.cross_groove(
        0.0,
        v2.BRACKET_PLATE_CENTER_Y,
        -core.BASE_T - 0.05,
        v2.ALIGNMENT_GROOVE_DEPTH + 0.05,
    )
    return cradle.cut(bracket_groove)


def split_cradle_source() -> cq.Workplane:
    """Return the integral V3 cradle with the three splice recesses added."""
    return integral_full_cradle().cut(cradle_splice_grooves())


def cradle_halves() -> tuple[cq.Workplane, cq.Workplane]:
    """Return the left and right support-free cradle wings in assembly space."""
    source = split_cradle_source()
    return source.intersect(_seam_mask(True)), source.intersect(_seam_mask(False))


def cradle_splice_key() -> cq.Workplane:
    """Return one loose-fit, elephant-foot-relieved rear splice key."""
    key = (
        cq.Workplane("XY")
        .rect(CRADLE_SPLICE_KEY_LENGTH, CRADLE_SPLICE_KEY_WIDTH)
        .extrude(CRADLE_SPLICE_KEY_T)
    )
    key = key.faces("<Z").edges().chamfer(CRADLE_SPLICE_KEY_EDGE_CHAMFER)
    return key.faces(">Z").edges().chamfer(CRADLE_SPLICE_KEY_EDGE_CHAMFER)


def cradle_splice_keys_installed() -> tuple[cq.Workplane, ...]:
    """Return all three keys recessed into the cradle rear face."""
    z0 = -core.BASE_T + CRADLE_SPLICE_KEY_RECESS
    return tuple(
        cradle_splice_key().translate((x_pos, y_pos, z0))
        for x_pos, y_pos in zip(CRADLE_SPLICE_KEY_X, CRADLE_SPLICE_KEY_Y, strict=True)
    )


def installed_parts() -> tuple[cq.Workplane, ...]:
    """Return all V3 modules in assembly position."""
    left, right = cradle_halves()
    tilt = core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG
    return (
        left.rotate((0, 0, 0), (1, 0, 0), tilt),
        right.rotate((0, 0, 0), (1, 0, 0), tilt),
        v2.rear_bracket_installed(),
        v2.pedestal_sleeve_installed(),
    )


def installed_splice_keys() -> tuple[cq.Workplane, ...]:
    """Return the three recessed splice keys in installed orientation."""
    tilt = core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG
    return tuple(
        key.rotate((0, 0, 0), (1, 0, 0), tilt)
        for key in cradle_splice_keys_installed()
    )


def print_parts() -> tuple[cq.Workplane, ...]:
    """Return all unique V3 modules on their intended bed datums."""
    left, right = cradle_halves()
    _, bracket, sleeve, _, alignment_key = v2.print_parts()
    return (
        v2.shift_to_bed(left),
        v2.shift_to_bed(right),
        bracket,
        sleeve,
        alignment_key,
        v2.shift_to_bed(cradle_splice_key()),
    )


def export() -> None:
    """Export the V3 concept as production-oriented STL and installed STEP."""
    OUT.mkdir(parents=True, exist_ok=True)
    left, right, bracket, sleeve, alignment_key, splice_key = print_parts()
    exports = {
        "tablet_stand_v3_cradle_left.stl": left,
        "tablet_stand_v3_cradle_right.stl": right,
        "tablet_stand_v3_rear_bracket.stl": bracket,
        "tablet_stand_v3_sleeve.stl": sleeve,
        "tablet_stand_v3_alignment_key_print_2.stl": alignment_key,
        "tablet_stand_v3_cradle_splice_key_print_3.stl": splice_key,
    }
    for filename, part in exports.items():
        cq.exporters.export(
            part,
            str(OUT / filename),
            tolerance=LINEAR_TOLERANCE,
            angularTolerance=ANGULAR_TOLERANCE,
        )

    left_i, right_i, bracket_i, sleeve_i = installed_parts()
    assembly = cq.Assembly(name="tablet_stand_v3")
    assembly.add(left_i, name="cradle_left", color=cq.Color(0.12, 0.24, 0.38))
    assembly.add(right_i, name="cradle_right", color=cq.Color(0.18, 0.34, 0.52))
    assembly.add(bracket_i, name="rear_bracket", color=cq.Color(0.20, 0.34, 0.50))
    assembly.add(sleeve_i, name="sleeve", color=cq.Color(0.18, 0.24, 0.32))
    for index, key in enumerate(installed_splice_keys(), start=1):
        assembly.add(key, name=f"cradle_splice_key_{index}", color=cq.Color(0.90, 0.50, 0.12))
    assembly.save(str(OUT / "tablet_stand_v3.step"))

    left_bb = left.val().BoundingBox()
    right_bb = right.val().BoundingBox()
    metadata = {
        "units": "mm",
        "revision": "v3 split-cradle concept",
        "material": "PLA",
        "machine": "Creality Ender-3 Pro, 220 x 220 x 250 mm, 0.4 mm nozzle",
        "preserved_geometry_source": "V2 tested tablet, USB-C, button, tube, and cable geometry",
        "tablet_loading": "seat tablet in right wing, bring integral enclosed left wing onto tablet, then join cradle seam",
        "separate_left_cap": False,
        "cradle_split": {
            "method": "support-free stepped planar seam with three recessed adhesive splice keys",
            "outer_seam_x": CRADLE_SEAM_OUTER_X,
            "center_seam_x": CRADLE_SEAM_CENTER_X,
            "step_y": CRADLE_SEAM_STEP_Y,
            "total_clearance": CRADLE_SEAM_CLEARANCE,
            "left_print_envelope": [left_bb.xlen, left_bb.ylen, left_bb.zlen],
            "right_print_envelope": [right_bb.xlen, right_bb.ylen, right_bb.zlen],
            "rear_bracket_bridges_center_seam": True,
        },
        "splice_key": {
            "quantity": CRADLE_SPLICE_KEY_QUANTITY,
            "length": CRADLE_SPLICE_KEY_LENGTH,
            "width": CRADLE_SPLICE_KEY_WIDTH,
            "thickness": CRADLE_SPLICE_KEY_T,
            "groove_length": CRADLE_SPLICE_GROOVE_LENGTH,
            "groove_width": CRADLE_SPLICE_GROOVE_WIDTH,
            "groove_depth": CRADLE_SPLICE_GROOVE_DEPTH,
            "recess_below_rear_face": CRADLE_SPLICE_KEY_RECESS,
            "length_clearance_total": CRADLE_SPLICE_GROOVE_LENGTH - CRADLE_SPLICE_KEY_LENGTH,
            "width_clearance_total": CRADLE_SPLICE_GROOVE_WIDTH - CRADLE_SPLICE_KEY_WIDTH,
            "depth_clearance": CRADLE_SPLICE_GROOVE_DEPTH - CRADLE_SPLICE_KEY_T,
        },
        "print_orientation": {
            "cradle_left": "rear face down",
            "cradle_right": "rear face down",
            "splice_key": "flat; print three",
            "supports": "none intended for split joint",
        },
    }
    (OUT / "model_parameters.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Exported tablet stand V3 concept to {OUT}")


if __name__ == "__main__":
    export()
