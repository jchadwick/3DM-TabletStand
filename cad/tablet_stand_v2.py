"""Support-minimized V2 tablet stand with four main modules and two keys.

Installed coordinates match V1:
    X: tablet left (-) to right / USB-C side (+)
    Y: viewer / bottom edge (-) to far / top edge (+)
    Z: up

Print orientations:
    cradle: rear frame face on the bed
    rear bracket: horizontal sleeve-interface foot on the bed
    sleeve: flange face on the bed, tube-entry bore open upward
    end stop: screen-facing lip/top face on the bed

All dimensions are millimeters. V1 remains the source for confirmed tablet,
tube, rail, USB-C, cable, and tilt dimensions; this file owns the V2 joints.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "v2"
sys.path.insert(0, str(ROOT))

from cad import tablet_stand_v1 as v1  # noqa: E402

# ============================================================
# PARAMETERS - V2 module joints and print-oriented features
# ============================================================

# Main structural joints are broad, edge-indexed adhesive bonds. The bracket
# plate matches the center plate width and top edge; the foot matches the sleeve
# flange front and side edges.
M3_CLEARANCE = 3.4
CRADLE_BRACKET_BOND_AREA = 74.0 * 36.0
BRACKET_SLEEVE_BOND_AREA = 60.0 * 28.0

# One support-free cross key is printed twice. Each joint receives matching
# half-depth grooves, giving positive X/Y alignment without protrusions on the
# broad print-bed faces.
ALIGNMENT_KEY_LONG = 36.0
ALIGNMENT_KEY_SHORT = 16.0
ALIGNMENT_KEY_WIDTH = 4.0
ALIGNMENT_KEY_T = 2.0
ALIGNMENT_KEY_CLEARANCE = 0.25
ALIGNMENT_GROOVE_DEPTH = 1.15
ALIGNMENT_KEY_QUANTITY = 2

# Bed-compatible V2 end-stop joint. The boss sits completely outside the
# tablet cavity and accepts the same single M3 fastener along local Z.
ENDSTOP_BOSS_X = -100.5
ENDSTOP_BOSS_Y = -68.5
ENDSTOP_BOSS_X_SIZE = 8.0
ENDSTOP_BOSS_Y_SIZE = 8.0
ENDSTOP_BOSS_HEIGHT = 6.0
ENDSTOP_TAB_T = 3.0
ENDSTOP_OUTER_WALL_X = 3.0
ENDSTOP_OUTER_WALL_Y_MIN = -72.5
ENDSTOP_OUTER_WALL_Y_MAX = 65.0
ENDSTOP_CAP_Y = 116.0
ENDSTOP_LOCATOR_Y = (-42.0, 42.0)
ENDSTOP_LOCATOR_Y_SIZE = 18.0
ENDSTOP_SCREW_NOMINAL = "one M3 x 8-10 mm, verify physically"

# Rear bracket: a partial-height plate preserves the open back while its lower
# installed edge stays above the horizontal print foot.
BRACKET_PLATE_X = 74.0
BRACKET_PLATE_Y = 36.0
BRACKET_PLATE_T = 6.0
BRACKET_PLATE_CENTER_Y = 14.0
BRACKET_PLATE_Z0 = -9.0
BRACKET_CORNER_R = 4.0
BRACKET_GUSSET_T = 4.0
BRACKET_CLIP_X = (16.0, 34.0)
BRACKET_CLIP_LOCAL_Y = 2.0

# Sleeve-to-bracket flange and foot. Their matching front and side edges form a
# repeatable glue-up datum while leaving the tested 32.2 mm bore untouched.
SLEEVE_FLANGE_X = 60.0
SLEEVE_FLANGE_Y = 46.0
SLEEVE_FLANGE_CENTER_Y = 26.0
SLEEVE_FLANGE_T = 4.0
SLEEVE_FLANGE_CORNER_R = 5.0
SLEEVE_FLANGE_TOP_Z = v1.SLEEVE_TOP_Z + SLEEVE_FLANGE_T
SLEEVE_FLANGE_BOTTOM_Z = v1.SLEEVE_TOP_Z - 0.10
BRACKET_FOOT_X = 60.0
BRACKET_FOOT_Y = 28.0
BRACKET_FOOT_T = 4.0
BRACKET_FOOT_CENTER_Y = 17.0
BRACKET_FOOT_BOTTOM_Z = SLEEVE_FLANGE_TOP_Z

# Export tessellation
LINEAR_TOLERANCE = 0.08
ANGULAR_TOLERANCE = 0.15


# ============================================================
# GEOMETRY HELPERS
# ============================================================

def shift_to_bed(shape: cq.Workplane) -> cq.Workplane:
    """Translate a part so its lowest Z face is exactly on the print bed."""
    return shape.translate((0.0, 0.0, -shape.val().BoundingBox().zmin))


def cross_key(
    center_x: float,
    center_y: float,
    z0: float,
    thickness: float,
    clearance: float = 0.0,
) -> cq.Workplane:
    """Create a connected cross key or its clearance-expanded groove cutter."""
    long = ALIGNMENT_KEY_LONG + clearance
    short = ALIGNMENT_KEY_SHORT + clearance
    width = ALIGNMENT_KEY_WIDTH + clearance
    horizontal = (
        cq.Workplane("XY")
        .workplane(offset=z0)
        .rect(long, width)
        .extrude(thickness)
        .translate((center_x, center_y, 0.0))
    )
    vertical = (
        cq.Workplane("XY")
        .workplane(offset=z0)
        .rect(width, short)
        .extrude(thickness)
        .translate((center_x, center_y, 0.0))
    )
    return horizontal.union(vertical)


# ============================================================
# PRINTABLE MODULES
# ============================================================

def flat_cradle() -> cq.Workplane:
    """V1 tablet cradle without rear clips, plus the V2 flush screw pattern."""
    cradle = v1.flat_main_holder(
        include_rear_clips=False,
        include_endstop_lug=False,
    )
    endstop_boss = v1.rounded_plate(
        ENDSTOP_BOSS_X_SIZE,
        ENDSTOP_BOSS_Y_SIZE,
        ENDSTOP_BOSS_HEIGHT,
        -v1.BASE_T,
        v1.EXPOSED_CORNER_R,
    ).translate((ENDSTOP_BOSS_X, ENDSTOP_BOSS_Y, 0.0))
    endstop_pilot = (
        cq.Workplane("XY")
        .workplane(offset=-v1.BASE_T - 1.0)
        .center(ENDSTOP_BOSS_X, ENDSTOP_BOSS_Y)
        .circle(v1.M3_PILOT / 2.0)
        .extrude(ENDSTOP_BOSS_HEIGHT + 2.0)
    )
    cradle = cradle.union(endstop_boss).cut(endstop_pilot)
    cradle_groove = cross_key(
        0.0,
        BRACKET_PLATE_CENTER_Y,
        -v1.BASE_T - 0.05,
        ALIGNMENT_GROOVE_DEPTH + 0.05,
        ALIGNMENT_KEY_CLEARANCE,
    )
    return cradle.cut(cradle_groove)


def flat_end_stop() -> cq.Workplane:
    """V2 stop adjacent to, rather than overlapping, the cradle rail ends."""
    cavity_x = v1.TABLET_X + v1.FIT_X
    cavity_y = v1.TABLET_Y + v1.FIT_Y
    rail_top = v1.TABLET_Z + v1.FIT_Z + v1.LIP_T
    wall_h = v1.BASE_T + rail_top
    cradle_left_x = -(cavity_x + 2.0 * v1.WALL_T) / 2.0

    outer_wall_center_x = cradle_left_x - ENDSTOP_OUTER_WALL_X / 2.0
    outer_wall_center_y = (ENDSTOP_OUTER_WALL_Y_MIN + ENDSTOP_OUTER_WALL_Y_MAX) / 2.0
    outer_wall = v1.rounded_plate(
        ENDSTOP_OUTER_WALL_X,
        ENDSTOP_OUTER_WALL_Y_MAX - ENDSTOP_OUTER_WALL_Y_MIN,
        wall_h,
        -v1.BASE_T,
        v1.EXPOSED_CORNER_R,
    ).translate((outer_wall_center_x, outer_wall_center_y, 0.0))

    # The screen-facing cap stops short of the long-edge rail lips. Two local
    # pads below it contact the tablet edge through the otherwise open left end.
    cap_left_x = cradle_left_x - 0.5
    cap_right_x = -cavity_x / 2.0 + v1.LIP_OVERLAP
    cap = v1.rounded_plate(
        cap_right_x - cap_left_x,
        ENDSTOP_CAP_Y,
        v1.LIP_T,
        v1.TABLET_Z + v1.FIT_Z,
        v1.LIP_CORNER_R,
    ).translate(((cap_left_x + cap_right_x) / 2.0, 0.0, 0.0))
    locator = None
    for locator_y in ENDSTOP_LOCATOR_Y:
        pad = v1.rounded_plate(
            v1.WALL_T,
            ENDSTOP_LOCATOR_Y_SIZE,
            v1.TABLET_Z + v1.FIT_Z,
            0.0,
            v1.EXPOSED_CORNER_R,
        ).translate((cradle_left_x + v1.WALL_T / 2.0, locator_y, 0.0))
        locator = pad if locator is None else locator.union(pad)
    assert locator is not None

    tab = v1.rounded_plate(
        ENDSTOP_BOSS_X_SIZE,
        ENDSTOP_BOSS_Y_SIZE,
        ENDSTOP_TAB_T,
        -v1.BASE_T + ENDSTOP_BOSS_HEIGHT,
        v1.EXPOSED_CORNER_R,
    ).translate((ENDSTOP_BOSS_X, ENDSTOP_BOSS_Y, 0.0))
    clearance = (
        cq.Workplane("XY")
        .workplane(offset=-v1.BASE_T + ENDSTOP_BOSS_HEIGHT - 1.0)
        .center(ENDSTOP_BOSS_X, ENDSTOP_BOSS_Y)
        .circle(M3_CLEARANCE / 2.0)
        .extrude(ENDSTOP_TAB_T + 2.0)
    )
    stop = outer_wall.union(cap).union(locator).union(tab).cut(clearance)
    # Remove any residual rail-corner contact volume while retaining adjacent
    # faces; split parts must never depend on V1's overlapping assembly solids.
    return stop.cut(flat_cradle())


def rear_bracket_local_plate() -> cq.Workplane:
    """Cradle-parallel mounting plate with captive nuts and open cable clips."""
    plate = v1.rounded_plate(
        BRACKET_PLATE_X,
        BRACKET_PLATE_Y,
        BRACKET_PLATE_T,
        BRACKET_PLATE_Z0,
        BRACKET_CORNER_R,
    ).translate((0.0, BRACKET_PLATE_CENTER_Y, 0.0))
    plate_groove = cross_key(
        0.0,
        BRACKET_PLATE_CENTER_Y,
        BRACKET_PLATE_Z0 + BRACKET_PLATE_T - ALIGNMENT_GROOVE_DEPTH,
        ALIGNMENT_GROOVE_DEPTH + 0.05,
        ALIGNMENT_KEY_CLEARANCE,
    )
    plate = plate.cut(plate_groove)
    # The clips attach to the rear face of the plate rather than the cradle,
    # leaving the cradle's complete rear frame surface available as a print bed.
    rear_face_z = BRACKET_PLATE_Z0
    clip_center_z = rear_face_z - v1.REAR_CLIP_OUTER_Z / 2.0 + 0.05
    for clip_x in BRACKET_CLIP_X:
        clip_outer = cq.Workplane("XY").box(
            v1.REAR_CLIP_LENGTH,
            v1.REAR_CLIP_OUTER_Y,
            v1.REAR_CLIP_OUTER_Z,
        ).translate((clip_x, BRACKET_CLIP_LOCAL_Y, clip_center_z))
        clip_cavity = v1.x_cylinder(
            v1.BRAIDED_CHANNEL_ID,
            v1.REAR_CLIP_LENGTH + 2.0,
            (
                clip_x - v1.REAR_CLIP_LENGTH / 2.0 - 1.0,
                BRACKET_CLIP_LOCAL_Y,
                clip_center_z,
            ),
        )
        clip_opening = cq.Workplane("XY").box(
            v1.REAR_CLIP_LENGTH + 2.0,
            v1.BRAIDED_CHANNEL_SLOT,
            v1.REAR_CLIP_OUTER_Z,
        ).translate(
            (
                clip_x,
                BRACKET_CLIP_LOCAL_Y,
                clip_center_z - v1.REAR_CLIP_OUTER_Z / 2.0,
            )
        )
        plate = plate.union(clip_outer.cut(clip_cavity).cut(clip_opening))
    return plate


def rear_bracket_installed() -> cq.Workplane:
    """Tilted cradle plate joined to a horizontal, bed-ready sleeve foot."""
    plate = rear_bracket_local_plate().rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        v1.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
    )

    foot = v1.rounded_plate(
        BRACKET_FOOT_X,
        BRACKET_FOOT_Y,
        BRACKET_FOOT_T,
        BRACKET_FOOT_BOTTOM_Z,
        SLEEVE_FLANGE_CORNER_R,
    ).translate((0.0, BRACKET_FOOT_CENTER_Y, 0.0))
    foot_groove = cross_key(
        0.0,
        BRACKET_FOOT_CENTER_Y,
        BRACKET_FOOT_BOTTOM_Z - 0.05,
        ALIGNMENT_GROOVE_DEPTH + 0.05,
        ALIGNMENT_KEY_CLEARANCE,
    )
    foot = foot.cut(foot_groove)
    # Two broad triangular ribs transfer tablet load into the sleeve foot. The
    # complete profile rises from the foot at support-safe angles.
    rib_profile = [
        (7.8, BRACKET_FOOT_BOTTOM_Z + 0.1),
        (13.4, 29.0),
        (18.5, 10.0),
        (26.0, BRACKET_FOOT_BOTTOM_Z + BRACKET_FOOT_T),
        (26.0, BRACKET_FOOT_BOTTOM_Z),
    ]
    ribs = None
    for x in (-13.0, 13.0):
        rib = (
            cq.Workplane("YZ", origin=(x - BRACKET_GUSSET_T / 2.0, 0.0, 0.0))
            .polyline(rib_profile)
            .close()
            .extrude(BRACKET_GUSSET_T)
        )
        ribs = rib if ribs is None else ribs.union(rib)
    assert ribs is not None
    # Re-cut the foot groove after unioning the ribs so no rib material can
    # refill the alignment-key clearance volume.
    return plate.union(foot).union(ribs).cut(foot_groove)


def pedestal_sleeve_installed() -> cq.Workplane:
    """Closed V1 sleeve plus a print bed and captive-nut mounting flange."""
    flange = v1.rounded_plate(
        SLEEVE_FLANGE_X,
        SLEEVE_FLANGE_Y,
        SLEEVE_FLANGE_TOP_Z - SLEEVE_FLANGE_BOTTOM_Z,
        SLEEVE_FLANGE_BOTTOM_Z,
        SLEEVE_FLANGE_CORNER_R,
    ).translate((0.0, SLEEVE_FLANGE_CENTER_Y, 0.0))
    flange_groove = cross_key(
        0.0,
        BRACKET_FOOT_CENTER_Y,
        SLEEVE_FLANGE_TOP_Z - ALIGNMENT_GROOVE_DEPTH,
        ALIGNMENT_GROOVE_DEPTH + 0.05,
        ALIGNMENT_KEY_CLEARANCE,
    )
    flange = flange.cut(flange_groove)
    return v1.vertical_sleeve_with_cable_channel().union(flange)


def alignment_key_print() -> cq.Workplane:
    """Reusable support-free glue-joint key; print two copies."""
    return cross_key(0.0, 0.0, 0.0, ALIGNMENT_KEY_T)


def installed_parts() -> tuple[cq.Workplane, cq.Workplane, cq.Workplane, cq.Workplane]:
    """Return cradle, rear bracket, sleeve, and end stop in assembly position."""
    cradle = flat_cradle().rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        v1.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
    )
    bracket = rear_bracket_installed()
    sleeve = pedestal_sleeve_installed()
    stop = flat_end_stop().rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        v1.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
    )
    return cradle, bracket, sleeve, stop


def print_parts() -> tuple[
    cq.Workplane,
    cq.Workplane,
    cq.Workplane,
    cq.Workplane,
    cq.Workplane,
]:
    """Return all modules in their intended slicer orientations."""
    cradle = shift_to_bed(flat_cradle())
    bracket = shift_to_bed(rear_bracket_installed())
    sleeve = shift_to_bed(
        pedestal_sleeve_installed().rotate(
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            180.0,
        )
    )
    stop = shift_to_bed(
        flat_end_stop().rotate(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            180.0,
        )
    )
    key = shift_to_bed(alignment_key_print())
    return cradle, bracket, sleeve, stop, key


# ============================================================
# EXPORT
# ============================================================

def export() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cradle, bracket, sleeve, stop, key = print_parts()
    cradle_installed, bracket_installed, sleeve_installed, stop_installed = installed_parts()

    exports = {
        "tablet_stand_v2_cradle.stl": cradle,
        "tablet_stand_v2_rear_bracket.stl": bracket,
        "tablet_stand_v2_sleeve.stl": sleeve,
        "tablet_stand_v2_end_stop.stl": stop,
        "tablet_stand_v2_alignment_key_print_2.stl": key,
    }
    for filename, part in exports.items():
        cq.exporters.export(
            part,
            str(OUT / filename),
            tolerance=LINEAR_TOLERANCE,
            angularTolerance=ANGULAR_TOLERANCE,
        )

    assembly = cq.Assembly(name="tablet_stand_v2")
    assembly.add(cradle_installed, name="cradle", color=cq.Color(0.12, 0.14, 0.17))
    assembly.add(bracket_installed, name="rear_bracket", color=cq.Color(0.20, 0.34, 0.50))
    assembly.add(sleeve_installed, name="sleeve", color=cq.Color(0.18, 0.24, 0.32))
    assembly.add(stop_installed, name="m3_end_stop", color=cq.Color(0.10, 0.32, 0.55))
    cradle_key_installed = cross_key(
        0.0,
        BRACKET_PLATE_CENTER_Y,
        -v1.BASE_T - ALIGNMENT_KEY_T / 2.0,
        ALIGNMENT_KEY_T,
    ).rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        v1.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
    )
    sleeve_key_installed = cross_key(
        0.0,
        BRACKET_FOOT_CENTER_Y,
        SLEEVE_FLANGE_TOP_Z - ALIGNMENT_KEY_T / 2.0,
        ALIGNMENT_KEY_T,
    )
    assembly.add(cradle_key_installed, name="cradle_alignment_key", color=cq.Color(0.90, 0.50, 0.12))
    assembly.add(sleeve_key_installed, name="sleeve_alignment_key", color=cq.Color(0.90, 0.50, 0.12))
    assembly.save(str(OUT / "tablet_stand_v2.step"))

    metadata = {
        "units": "mm",
        "revision": "v2 support-minimized modular concept",
        "tablet": {"x": v1.TABLET_X, "y": v1.TABLET_Y, "z": v1.TABLET_Z},
        "fit_allowance_total": {"x": v1.FIT_X, "y": v1.FIT_Y, "z": v1.FIT_Z},
        "tilt_degrees_from_vertical": v1.TILT_FROM_VERTICAL_DEG,
        "screen_angle_degrees_above_horizontal": v1.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
        "tube": {
            "od": 32.0,
            "sleeve_id": v1.SLEEVE_ID,
            "sleeve_od": v1.SLEEVE_OD,
            "engagement": v1.SLEEVE_ENGAGEMENT,
            "seating_cap_thickness": v1.SLEEVE_CAP_T,
            "center_offset_behind_screen_plane_y": v1.SLEEVE_CENTER_Y,
            "bottom_z": v1.SLEEVE_BOTTOM_Z,
        },
        "modules": {
            "cradle": "rear frame face on bed; rail and end-stop features face up",
            "rear_bracket": "horizontal sleeve-interface foot on bed",
            "sleeve": "flange on bed; tube-entry bore open upward",
            "end_stop": "screen-facing lip/top face on bed",
            "alignment_key": "flat on bed; print two identical copies",
        },
        "joints": {
            "end_stop": {
                "count": 1,
                "screw": ENDSTOP_SCREW_NOMINAL,
                "axis": "local Z, front-accessible and outside tablet cavity",
            },
            "cradle_to_bracket": {
                "method": "adhesive bond",
                "nominal_area_mm2": CRADLE_BRACKET_BOND_AREA,
                "alignment": "matching cross grooves plus one printed alignment key",
            },
            "bracket_to_sleeve": {
                "method": "adhesive bond",
                "nominal_area_mm2": BRACKET_SLEEVE_BOND_AREA,
                "alignment": "matching cross grooves plus one printed alignment key",
            },
        },
        "alignment_key": {
            "quantity": ALIGNMENT_KEY_QUANTITY,
            "long": ALIGNMENT_KEY_LONG,
            "short": ALIGNMENT_KEY_SHORT,
            "width": ALIGNMENT_KEY_WIDTH,
            "thickness": ALIGNMENT_KEY_T,
            "groove_depth_each_side": ALIGNMENT_GROOVE_DEPTH,
            "total_clearance": ALIGNMENT_KEY_CLEARANCE,
        },
        "cable": {
            "braided_cable_diameter": v1.BRAIDED_CABLE_D,
            "bracket_clip_x": BRACKET_CLIP_X,
            "sleeve_channel_id": v1.BRAIDED_CHANNEL_ID,
            "sleeve_channel_slot": v1.BRAIDED_CHANNEL_SLOT,
        },
    }
    (OUT / "model_parameters.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Exported tablet stand v2 to {OUT}")


if __name__ == "__main__":
    export()
