"""V3 split-cradle tablet stand concept.

V3 preserves the physically tested V2 tablet, button, USB-C, tube, and cable
geometry.  The wide flat cradle is divided into two bed-friendly wings.  The
left wing has an integral continuous end wall, so it replaces the separate V2
cap.  Three large integral tongues slide into support-free receivers in the
right wing.  A removable tapered cross-wedge locks the lower receiver; the same
4 mm channel accepts a hidden M3 bolt and nut as a fallback.  No cradle glue is
required, and the left wing remains removable for tablet service.

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


# The straight split leaves a printable glue-free joint at the holder center.
# All three tongues move in +X as the enclosed left wing closes around the
# tablet.  The user-tested PLA clearances inform the close root / loose lead.
CRADLE_SEAM_X = 0.0
CRADLE_SEAM_CLEARANCE = 0.35
JOINT_TONGUE_ROOT_X = -7.0
JOINT_TONGUE_TIP_X = 18.0
JOINT_SOCKET_BACK_X = 19.0
JOINT_RECEIVER_BACK_X = 22.0
JOINT_ROOT_CLEARANCE_TOTAL = 0.50
JOINT_TIP_CLEARANCE_TOTAL = 1.10

# Finish-only radii for the integral left closure. These are intentionally
# separate from the superseded V2 end-stop constants so the active V3 visual
# treatment can evolve without changing the historical cap geometry.
LEFT_CLOSURE_CORNER_R = 1.70
LEFT_CLOSURE_EDGE_R = 0.85

# Upper and lower receivers sit just outside the tablet cavity, overlap the
# existing long-edge walls, and use an open bed-side floor plus an 8.5 mm roof
# bridge (below the confirmed 10 mm PLA rule).  The center tongue stays within
# the 3 mm rear plate and enters a through-depth planar pocket.
OUTER_JOINT_CENTER_Y = (-65.75, 65.75)
OUTER_TONGUE_ROOT_Y = 4.0
OUTER_TONGUE_TIP_Y = 3.6
OUTER_TONGUE_Z = 6.0
OUTER_RECEIVER_Y = 7.5
OUTER_RECEIVER_Z = 8.5
OUTER_SOCKET_ROOT_Y = OUTER_TONGUE_ROOT_Y + JOINT_ROOT_CLEARANCE_TOTAL
OUTER_SOCKET_TIP_Y = OUTER_TONGUE_TIP_Y + JOINT_TIP_CLEARANCE_TOTAL
OUTER_SOCKET_Z = OUTER_TONGUE_Z + 0.50
CENTER_TONGUE_ROOT_Y = 20.0
CENTER_TONGUE_TIP_Y = 18.0
CENTER_SOCKET_ROOT_Y = CENTER_TONGUE_ROOT_Y + JOINT_ROOT_CLEARANCE_TOTAL
CENTER_SOCKET_TIP_Y = CENTER_TONGUE_TIP_Y + JOINT_TIP_CLEARANCE_TOTAL

# A transverse square channel through the lower receiver and tongue accepts a
# printed tapered wedge.  Its 4 mm bridge is comfortably support-free.  If the
# wedge does not hold in the actual filament, the same channel accepts an M3
# bolt with washers and a nut without changing either cradle wing.
LOCK_CENTER_X = 10.0
LOCK_CENTER_Y = OUTER_JOINT_CENTER_Y[0]
LOCK_CHANNEL_X = 4.0
LOCK_CHANNEL_Y = 14.0
LOCK_CHANNEL_Z = 4.0
LOCK_WEDGE_ROOT_XZ = 3.70
LOCK_WEDGE_TIP_XZ = 3.30
LOCK_WEDGE_BODY_Y0 = -71.0
LOCK_WEDGE_BODY_Y1 = -62.0
LOCK_WEDGE_HEAD_XZ = 7.0
LOCK_WEDGE_HEAD_Y = 2.0
LOCK_WEDGE_QUANTITY = 1
M3_FALLBACK_DIAMETER = 3.0

# Exact lower-joint crop for testing insertion, seating, wedge retention, and
# the optional M3 channel before either full cradle wing is printed.
LOCK_COUPON_X_MIN = -13.0
LOCK_COUPON_X_MAX = 25.0
LOCK_COUPON_Y_MIN = -73.0
LOCK_COUPON_Y_MAX = -58.0
LOCK_COUPON_Z_MIN = -3.1
LOCK_COUPON_Z_MAX = 6.0
# Bed-center targets for a single job containing one copy of every coupon
# component.  The 10+ mm edge gaps leave room for a 5 mm brim around each
# island without fusing the parts together.
LOCK_COUPON_PLATE_CENTERS = ((-25.0, 0.0), (25.0, 0.0), (0.0, 22.0))

LINEAR_TOLERANCE = 0.05
ANGULAR_TOLERANCE = 0.1


def _seam_mask(left: bool) -> cq.Workplane:
    """Return one clearance-offset half of the straight XY split mask."""
    margin = 150.0
    half_gap = CRADLE_SEAM_CLEARANCE / 2.0
    center_x = CRADLE_SEAM_X + (-half_gap if left else half_gap)
    width = margin + center_x if left else margin - center_x
    x_center = (-margin + center_x) / 2.0 if left else (margin + center_x) / 2.0
    return cq.Workplane("XY").box(width, 180.0, 50.0).translate((x_center, 0.0, 5.0))


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
        LEFT_CLOSURE_CORNER_R,
        LEFT_CLOSURE_EDGE_R,
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


def continuous_front_edge_rails() -> cq.Workplane:
    """Shroud the outer joint blocks inside straight, smooth top/bottom rails.

    The structural tongue/receiver hardware remains accessible from the rear
    side of each wing, while the screen-facing perimeter reads as one straight
    edge instead of two small joiner bumps.
    """
    cavity_x = core.TABLET_X + core.FIT_X
    cavity_y = core.TABLET_Y + core.FIT_Y
    rail_top = core.TABLET_Z + core.FIT_Z + core.LIP_T
    wall_h = core.BASE_T + rail_top
    outer_x = cavity_x + 2.0 * core.WALL_T
    cradle_left_x = -outer_x / 2.0
    rail_left_x = cradle_left_x + core.LEFT_RAIL_ENTRY_RELIEF_X
    outer_wall_inner_x = cavity_x / 2.0 + core.USB_POCKET_INNER_X
    outer_wall_x = outer_wall_inner_x + core.USB_END_WALL_T
    rail_x = outer_wall_x - rail_left_x
    rail_center_x = (outer_wall_x + rail_left_x) / 2.0
    inner_y = cavity_y / 2.0 + core.BUTTON_CHANNEL_DEPTH_Y
    outer_y = abs(OUTER_JOINT_CENTER_Y[0]) + OUTER_RECEIVER_Y / 2.0
    shroud_y = outer_y - inner_y
    shroud_center_y = (outer_y + inner_y) / 2.0

    rails: cq.Workplane | None = None
    for sign in (-1.0, 1.0):
        rail = core.softened_plate(
            rail_x,
            shroud_y,
            wall_h,
            -core.BASE_T,
            core.EXPOSED_CORNER_R,
            core.EXPOSED_EDGE_R,
        ).translate((rail_center_x, sign * shroud_center_y, 0.0))
        rails = rail if rails is None else rails.union(rail)
    assert rails is not None
    return rails


def integral_full_cradle() -> cq.Workplane:
    """Return the tested cradle interfaces with the V3 integral left closure."""
    # The rear bracket is bonded only to the fixed right wing so the left wing
    # can slide off for tablet service.  Therefore V3 intentionally omits the
    # old centered cradle-to-bracket alignment-key groove.
    return (
        core.flat_main_holder()
        .union(integral_left_closure())
        .union(continuous_front_edge_rails())
    )


def split_cradle_source() -> cq.Workplane:
    """Return the integral V3 cradle before the removable center joint."""
    return integral_full_cradle()


def tapered_plan_prism(
    x0: float,
    x1: float,
    center_y: float,
    width0: float,
    width1: float,
    z0: float,
    height: float,
) -> cq.Workplane:
    """Return an X-directed trapezoid in plan, extruded upward from ``z0``."""
    points = (
        (x0, center_y - width0 / 2.0),
        (x0, center_y + width0 / 2.0),
        (x1, center_y + width1 / 2.0),
        (x1, center_y - width1 / 2.0),
    )
    return cq.Workplane("XY").workplane(offset=z0).polyline(points).close().extrude(height)


def joint_tongues() -> cq.Workplane:
    """Return the three integral, bed-supported tongues on the left wing."""
    tongues: cq.Workplane | None = None
    for center_y in OUTER_JOINT_CENTER_Y:
        tongue = tapered_plan_prism(
            JOINT_TONGUE_ROOT_X,
            JOINT_TONGUE_TIP_X,
            center_y,
            OUTER_TONGUE_ROOT_Y,
            OUTER_TONGUE_TIP_Y,
            -core.BASE_T,
            OUTER_TONGUE_Z,
        )
        tongues = tongue if tongues is None else tongues.union(tongue)
    center = tapered_plan_prism(
        JOINT_TONGUE_ROOT_X,
        JOINT_TONGUE_TIP_X,
        0.0,
        CENTER_TONGUE_ROOT_Y,
        CENTER_TONGUE_TIP_Y,
        -core.BASE_T,
        core.BASE_T,
    )
    assert tongues is not None
    return tongues.union(center)


def outer_joint_receivers() -> cq.Workplane:
    """Return reinforced upper/lower shells with bed-open support-free floors."""
    x0 = CRADLE_SEAM_CLEARANCE / 2.0
    receiver_x = JOINT_RECEIVER_BACK_X - x0
    receivers: cq.Workplane | None = None
    for center_y in OUTER_JOINT_CENTER_Y:
        receiver = core.softened_plate(
            receiver_x,
            OUTER_RECEIVER_Y,
            OUTER_RECEIVER_Z,
            -core.BASE_T,
            0.8,
            core.EXPOSED_EDGE_R,
        ).translate(((x0 + JOINT_RECEIVER_BACK_X) / 2.0, center_y, 0.0))
        receivers = receiver if receivers is None else receivers.union(receiver)
    assert receivers is not None
    return receivers


def joint_socket_cutters() -> cq.Workplane:
    """Return the two outer socket tunnels and center planar tongue pocket."""
    cutters: cq.Workplane | None = None
    for center_y in OUTER_JOINT_CENTER_Y:
        cutter = tapered_plan_prism(
            -0.75,
            JOINT_SOCKET_BACK_X,
            center_y,
            OUTER_SOCKET_ROOT_Y,
            OUTER_SOCKET_TIP_Y,
            -core.BASE_T - 0.05,
            OUTER_SOCKET_Z + 0.05,
        )
        cutters = cutter if cutters is None else cutters.union(cutter)
    center = tapered_plan_prism(
        -0.75,
        JOINT_SOCKET_BACK_X,
        0.0,
        CENTER_SOCKET_ROOT_Y,
        CENTER_SOCKET_TIP_Y,
        -core.BASE_T - 0.05,
        core.BASE_T + 0.10,
    )
    assert cutters is not None
    return cutters.union(center)


def locking_channel() -> cq.Workplane:
    """Return the transverse wedge/M3 channel through the lower joint."""
    return (
        cq.Workplane("XY")
        .box(LOCK_CHANNEL_X, LOCK_CHANNEL_Y, LOCK_CHANNEL_Z)
        .translate((LOCK_CENTER_X, LOCK_CENTER_Y, 0.0))
    )


def cradle_halves() -> tuple[cq.Workplane, cq.Workplane]:
    """Return the removable left and fixed right cradle wings in assembly space."""
    source = split_cradle_source()
    left = source.intersect(_seam_mask(True)).union(joint_tongues()).cut(locking_channel())
    right = (
        source.intersect(_seam_mask(False))
        .union(outer_joint_receivers(), clean=False)
        .cut(joint_socket_cutters(), clean=False)
        .cut(locking_channel(), clean=False)
    )
    return left, right


def locking_wedge() -> cq.Workplane:
    """Return the removable tapered cross-wedge with an external pull head."""
    plane = cq.Plane(
        origin=(LOCK_CENTER_X, LOCK_WEDGE_BODY_Y0, 0.0),
        xDir=(1.0, 0.0, 0.0),
        normal=(0.0, 1.0, 0.0),
    )
    body = (
        cq.Workplane(plane)
        .rect(LOCK_WEDGE_ROOT_XZ, LOCK_WEDGE_ROOT_XZ)
        .workplane(offset=LOCK_WEDGE_BODY_Y1 - LOCK_WEDGE_BODY_Y0)
        .rect(LOCK_WEDGE_TIP_XZ, LOCK_WEDGE_TIP_XZ)
        .loft(combine=True)
    )
    head_center_y = LOCK_WEDGE_BODY_Y0 - LOCK_WEDGE_HEAD_Y / 2.0 + 0.25
    head = (
        cq.Workplane("XY")
        .box(LOCK_WEDGE_HEAD_XZ, LOCK_WEDGE_HEAD_Y, LOCK_WEDGE_HEAD_XZ)
        .translate((LOCK_CENTER_X, head_center_y, 0.0))
    )
    return body.union(head)


def locking_wedge_installed() -> cq.Workplane:
    """Return the seated wedge in cradle coordinates."""
    return locking_wedge()


def lock_coupon_parts() -> tuple[cq.Workplane, cq.Workplane, cq.Workplane]:
    """Return exact lower tongue/receiver crops plus the production wedge."""
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=LOCK_COUPON_Z_MIN)
        .box(
            LOCK_COUPON_X_MAX - LOCK_COUPON_X_MIN,
            LOCK_COUPON_Y_MAX - LOCK_COUPON_Y_MIN,
            LOCK_COUPON_Z_MAX - LOCK_COUPON_Z_MIN,
            centered=(True, True, False),
        )
        .translate(
            (
                (LOCK_COUPON_X_MIN + LOCK_COUPON_X_MAX) / 2.0,
                (LOCK_COUPON_Y_MIN + LOCK_COUPON_Y_MAX) / 2.0,
                0.0,
            )
        )
    )
    left, right = cradle_halves()
    return (
        left.intersect(cutter, clean=False),
        right.intersect(cutter, clean=False),
        locking_wedge(),
    )


def lock_coupon_print_plate_parts() -> tuple[cq.Workplane, cq.Workplane, cq.Workplane]:
    """Place one exact copy of each coupon component on a shared bed datum."""
    placed = []
    for part, (target_x, target_y) in zip(lock_coupon_parts(), LOCK_COUPON_PLATE_CENTERS):
        bed_part = v2.shift_to_bed(part)
        bounds = bed_part.val().BoundingBox()
        placed.append(
            bed_part.translate(
                (
                    target_x - (bounds.xmin + bounds.xmax) / 2.0,
                    target_y - (bounds.ymin + bounds.ymax) / 2.0,
                    0.0,
                )
            )
        )
    return tuple(placed)


def lock_coupon_print_plate() -> cq.Workplane:
    """Return the three spaced coupon solids as one reproducible STL export."""
    compound = cq.Compound.makeCompound(
        [part.val() for part in lock_coupon_print_plate_parts()]
    )
    return cq.Workplane("XY").newObject([compound])


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


def installed_locking_wedge() -> cq.Workplane:
    """Return the removable cross-wedge in installed orientation."""
    tilt = core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG
    return locking_wedge_installed().rotate((0, 0, 0), (1, 0, 0), tilt)


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
        v2.shift_to_bed(locking_wedge()),
    )


def export() -> None:
    """Export the V3 concept as production-oriented STL and installed STEP."""
    OUT.mkdir(parents=True, exist_ok=True)
    left, right, bracket, sleeve, alignment_key, wedge = print_parts()
    coupon_left, coupon_right, coupon_wedge = lock_coupon_parts()
    coupon_plate = lock_coupon_print_plate()
    exports = {
        "tablet_stand_v3_cradle_left.stl": left,
        "tablet_stand_v3_cradle_right.stl": right,
        "tablet_stand_v3_rear_bracket.stl": bracket,
        "tablet_stand_v3_sleeve.stl": sleeve,
        "tablet_stand_v3_alignment_key_print_1.stl": alignment_key,
        "tablet_stand_v3_locking_wedge.stl": wedge,
        "tablet_stand_v3_lock_coupon_left.stl": v2.shift_to_bed(coupon_left),
        "tablet_stand_v3_lock_coupon_right.stl": v2.shift_to_bed(coupon_right),
        "tablet_stand_v3_lock_coupon_wedge.stl": v2.shift_to_bed(coupon_wedge),
        "tablet_stand_v3_lock_coupon_all3.stl": coupon_plate,
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
    assembly.add(
        installed_locking_wedge(),
        name="removable_locking_wedge",
        color=cq.Color(0.90, 0.50, 0.12),
    )
    assembly.save(str(OUT / "tablet_stand_v3.step"))

    left_bb = left.val().BoundingBox()
    right_bb = right.val().BoundingBox()
    coupon_plate_bb = coupon_plate.val().BoundingBox()
    metadata = {
        "units": "mm",
        "revision": "v3 removable tongue-and-wedge split cradle",
        "material": "PLA",
        "machine": "Creality Ender-3 Pro, 220 x 220 x 250 mm, 0.4 mm nozzle",
        "preserved_geometry_source": "V2 tested tablet, USB-C, button, tube, and cable geometry",
        "finish": {
            "front_frame_inner_corner_radius": core.FRAME_INNER_CORNER_R,
            "front_frame_outer_corner_radius": core.FRAME_OUTER_CORNER_R,
            "rail_wall_plan_corner_radius": core.EXPOSED_CORNER_R,
            "lip_plan_corner_radius": core.LIP_CORNER_R,
            "rail_wall_edge_fillet": core.EXPOSED_EDGE_R,
            "lip_edge_fillet": core.LIP_EDGE_R,
            "left_closure_plan_corner_radius": LEFT_CLOSURE_CORNER_R,
            "left_closure_edge_fillet": LEFT_CLOSURE_EDGE_R,
            "front_frame_corner_source": "supplied tablet mesh; approximately 7 mm tablet plan radius",
            "continuous_front_edge_rails": True,
        },
        "tablet_loading": (
            "seat tablet in right wing, slide integral enclosed left wing +X until all three "
            "tongues seat, then insert lower cross-wedge"
        ),
        "separate_left_cap": False,
        "cradle_split": {
            "method": "straight removable split with three integral tapered tongues and receivers",
            "seam_x": CRADLE_SEAM_X,
            "total_clearance": CRADLE_SEAM_CLEARANCE,
            "left_print_envelope": [left_bb.xlen, left_bb.ylen, left_bb.zlen],
            "right_print_envelope": [right_bb.xlen, right_bb.ylen, right_bb.zlen],
            "rear_bracket_bridges_center_seam": True,
            "adhesive_required": False,
        },
        "removable_joint": {
            "tongue_count": 3,
            "insertion_axis": "+X",
            "tongue_length": JOINT_TONGUE_TIP_X - CRADLE_SEAM_X,
            "receiver_depth": JOINT_SOCKET_BACK_X - CRADLE_SEAM_X,
            "root_clearance_total": JOINT_ROOT_CLEARANCE_TOTAL,
            "tip_clearance_total": JOINT_TIP_CLEARANCE_TOTAL,
            "locking_method": "tapered printed cross-wedge through lower receiver",
            "locking_channel": {
                "x": LOCK_CHANNEL_X,
                "z": LOCK_CHANNEL_Z,
                "bridge": LOCK_CHANNEL_X,
            },
            "wedge_quantity": LOCK_WEDGE_QUANTITY,
            "m3_fallback": "M3 bolt, washers, and nut through the same 4 mm channel",
        },
        "lock_coupon": {
            "uses_exact_production_geometry": True,
            "parts": 3,
            "combined_plate_envelope": [
                coupon_plate_bb.xlen,
                coupon_plate_bb.ylen,
                coupon_plate_bb.zlen,
            ],
            "purpose": "verify tongue insertion, seating, wedge retention, removal, and M3 fallback access",
        },
        "structural_assembly": {
            "rear_bracket_bond": "fixed right cradle wing only",
            "left_wing_contacts_bracket_without_adhesive": True,
            "left_wing_serviceable": True,
            "bracket_to_sleeve_bond": "unchanged V2 adhesive joint",
            "alignment_key_quantity": 1,
        },
        "print_orientation": {
            "cradle_left": "rear face down",
            "cradle_right": "rear face down",
            "locking_wedge": "flat on a broad head/body face; print one",
            "supports": "none intended for split joint",
        },
    }
    (OUT / "model_parameters.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Exported tablet stand V3 concept to {OUT}")


if __name__ == "__main__":
    export()
