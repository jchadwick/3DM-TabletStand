"""Support-minimized V2 tablet stand with four main modules and two keys.

Installed coordinates:
    X: tablet left (-) to right / USB-C side (+)
    Y: viewer / bottom edge (-) to far / top edge (+)
    Z: up

Print orientations:
    cradle: rear frame face on the bed
    rear bracket: horizontal sleeve-interface foot on the bed
    sleeve: flange face on the bed, tube-entry bore open upward
    slide-on left stop: broad outside wall face on the bed; twin pins build vertically

All dimensions are millimeters. ``tablet_stand_core`` owns confirmed tablet,
tube, rail, USB-C, cable, and tilt geometry; this file owns the modular joints.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "v2"
sys.path.insert(0, str(ROOT))

from cad import tablet_stand_core as core  # noqa: E402

# ============================================================
# PARAMETERS - V2 module joints and print-oriented features
# ============================================================

# Main structural joints are broad, edge-indexed adhesive bonds. The bracket
# plate matches the center plate width and top edge; the foot matches the sleeve
# flange front and side edges.
CRADLE_BRACKET_BOND_AREA = 74.0 * 36.0
BRACKET_SLEEVE_BOND_AREA = 60.0 * 28.0

# One support-free cross key is printed twice. The grooves retain their
# original size so replacement keys also fit already-printed V2 modules. A
# physical PLA+ fit test found the original 0.25 mm total planar allowance too
# tight, so the key is deliberately loose for glue assembly: at least 1.25 mm
# total clearance in every in-plane direction plus 0.50 mm through-thickness.
ALIGNMENT_GROOVE_LONG = 36.25
ALIGNMENT_GROOVE_SHORT = 16.25
ALIGNMENT_GROOVE_WIDTH = 4.25
ALIGNMENT_KEY_LONG = 35.0
ALIGNMENT_KEY_SHORT = 15.0
ALIGNMENT_KEY_WIDTH = 3.0
ALIGNMENT_KEY_T = 1.8
ALIGNMENT_KEY_EDGE_CHAMFER = 0.4
ALIGNMENT_GROOVE_DEPTH = 1.15
ALIGNMENT_KEY_QUANTITY = 2

# The left stop pushes horizontally onto two reinforced rail-end receivers.
# Each pin tapers from a forgiving lead to a close seated fit. The matching
# socket is a short house-profile tunnel with a 45-degree peaked roof in the
# cradle's rear-face-down orientation; the pins build vertically when the stop
# rests on its broad outside wall. No fit surface needs generated support.
ENDSTOP_SEAT_CLEARANCE_X = 0.25
ENDSTOP_OUTER_WALL_X = 3.5
ENDSTOP_OUTER_WALL_Y_MIN = -65.0
ENDSTOP_OUTER_WALL_Y_MAX = 65.0
ENDSTOP_CORNER_R = 1.70
ENDSTOP_EDGE_R = 0.70
ENDSTOP_CAP_Y = 116.0
ENDSTOP_LOCATOR_Y = (-42.0, 42.0)
ENDSTOP_LOCATOR_Y_SIZE = 18.0
ENDSTOP_RECEIVER_X_MIN = -103.5
ENDSTOP_RECEIVER_X_MAX = -90.0
ENDSTOP_RECEIVER_INNER_Y = (core.TABLET_Y + core.FIT_Y) / 2.0
ENDSTOP_RECEIVER_Y = 5.8
ENDSTOP_RECEIVER_CENTER_Y = ENDSTOP_RECEIVER_INNER_Y + ENDSTOP_RECEIVER_Y / 2.0
ENDSTOP_RECEIVER_Z0 = 5.0
ENDSTOP_RECEIVER_Z = 6.8
ENDSTOP_RECEIVER_CORNER_R = 0.8
ENDSTOP_RECEIVER_RAMP_INNER_Y = ENDSTOP_RECEIVER_INNER_Y + core.WALL_T - 0.2
ENDSTOP_RECEIVER_RAMP_Z0 = 3.4
ENDSTOP_RECEIVER_RAMP_Z1 = ENDSTOP_RECEIVER_Z0 + 0.2
ENDSTOP_POCKET_X_MIN = -104.0
ENDSTOP_POCKET_X_MAX = -91.1
ENDSTOP_POCKET_Y = 3.00
ENDSTOP_POCKET_Z = 3.80
ENDSTOP_PIN_X_MIN = -104.0
ENDSTOP_PIN_LENGTH = 12.0
ENDSTOP_PIN_CENTER_Z = 8.40
ENDSTOP_PIN_ROOT_Y = 2.40
ENDSTOP_PIN_ROOT_Z = 3.20
ENDSTOP_PIN_TIP_Y = 2.00
ENDSTOP_PIN_TIP_Z = 2.80
ENDSTOP_PIN_ROOT_CLEARANCE_Y = ENDSTOP_POCKET_Y - ENDSTOP_PIN_ROOT_Y
ENDSTOP_PIN_ROOT_CLEARANCE_Z = ENDSTOP_POCKET_Z - ENDSTOP_PIN_ROOT_Z
ENDSTOP_PIN_TIP_CLEARANCE_Y = ENDSTOP_POCKET_Y - ENDSTOP_PIN_TIP_Y
ENDSTOP_PIN_TIP_CLEARANCE_Z = ENDSTOP_POCKET_Z - ENDSTOP_PIN_TIP_Z

# Exact lower-rail crop pair for testing one of the two identical tapered plugs
# before committing the production cradle to a long print.
LEFT_SLIDE_COUPON_X_MIN = -108.0
LEFT_SLIDE_COUPON_X_MAX = -87.0
LEFT_SLIDE_COUPON_Y_MIN = -68.0
LEFT_SLIDE_COUPON_Y_MAX = -62.05
# Keep the two exact-fit pieces well apart on the combined plate.  The first
# physical coupon used a 10 mm gap and this particular PLA strung heavily
# across the repeated inter-part travel; 28 mm leaves an 18 mm clear gap even
# after the 5 mm brim around each piece.
LEFT_SLIDE_COUPON_PLATE_GAP = 28.0

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
SLEEVE_FLANGE_TOP_Z = core.SLEEVE_TOP_Z + SLEEVE_FLANGE_T
SLEEVE_FLANGE_BOTTOM_Z = core.SLEEVE_TOP_Z - 0.10
BRACKET_FOOT_X = 60.0
BRACKET_FOOT_Y = 28.0
BRACKET_FOOT_T = 4.0
BRACKET_FOOT_CENTER_Y = 17.0
BRACKET_FOOT_BOTTOM_Z = SLEEVE_FLANGE_TOP_Z

# Export tessellation
LINEAR_TOLERANCE = 0.08
ANGULAR_TOLERANCE = 0.15

# Right-side fit coupon.  The left cut stays far enough from the USB-C pocket
# to leave a useful rail lead-in while avoiding the cradle's center plate and
# glue joint.  The right limit is the production cradle's finished outer wall.
RIGHT_FIT_COUPON_X_MIN = 78.0
RIGHT_FIT_COUPON_X_MAX = (
    (core.TABLET_X + core.FIT_X) / 2.0
    + core.USB_POCKET_INNER_X
    + core.USB_END_WALL_T
)

# Small exact crop of the production top rail for verifying the measured
# power/volume-button slide-through channel before committing to the cradle.
BUTTON_FIT_COUPON_X_MIN = -(
    core.TABLET_X + core.FIT_X + 2.0 * core.WALL_T
) / 2.0
BUTTON_FIT_COUPON_X_MAX = core.BUTTON_CHANNEL_FINAL_X + 5.0
BUTTON_FIT_COUPON_Y_MIN = (core.TABLET_Y + core.FIT_Y) / 2.0 - 8.0
BUTTON_FIT_COUPON_Y_MAX = core.HOLDER_OUTER_Y / 2.0


# ============================================================
# GEOMETRY HELPERS
# ============================================================

def shift_to_bed(shape: cq.Workplane) -> cq.Workplane:
    """Translate a part so its lowest Z face is exactly on the print bed."""
    return shape.translate((0.0, 0.0, -shape.val().BoundingBox().zmin))


def cross_profile(
    center_x: float,
    center_y: float,
    z0: float,
    thickness: float,
    long: float,
    short: float,
    width: float,
) -> cq.Workplane:
    """Create a connected cross profile with explicit finished dimensions."""
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


def cross_groove(
    center_x: float,
    center_y: float,
    z0: float,
    thickness: float,
) -> cq.Workplane:
    """Create the fixed-size alignment-groove cutter."""
    return cross_profile(
        center_x,
        center_y,
        z0,
        thickness,
        ALIGNMENT_GROOVE_LONG,
        ALIGNMENT_GROOVE_SHORT,
        ALIGNMENT_GROOVE_WIDTH,
    )


def cross_key(
    center_x: float,
    center_y: float,
    z0: float,
    thickness: float,
) -> cq.Workplane:
    """Create the loose-fit glue-alignment key with elephant-foot relief."""
    key = cross_profile(
        center_x,
        center_y,
        z0,
        thickness,
        ALIGNMENT_KEY_LONG,
        ALIGNMENT_KEY_SHORT,
        ALIGNMENT_KEY_WIDTH,
    )
    key = key.faces("<Z").edges().chamfer(ALIGNMENT_KEY_EDGE_CHAMFER)
    return key.faces(">Z").edges().chamfer(ALIGNMENT_KEY_EDGE_CHAMFER)


def endstop_house_profile(width_y: float, height_z: float) -> list[tuple[float, float]]:
    """Return a support-free socket profile with vertical sides and a 45° roof."""
    half_y = width_y / 2.0
    half_z = height_z / 2.0
    roof_eave_z = half_z - half_y
    return [
        (-half_y, -half_z),
        (half_y, -half_z),
        (half_y, roof_eave_z),
        (0.0, half_z),
        (-half_y, roof_eave_z),
    ]


def tapered_x_pin(center_y: float) -> cq.Workplane:
    """Return one house-profile pin, broad at the stop and narrower at its lead."""
    return (
        cq.Workplane(
            "YZ",
            origin=(ENDSTOP_PIN_X_MIN, center_y, ENDSTOP_PIN_CENTER_Z),
        )
        .polyline(endstop_house_profile(ENDSTOP_PIN_ROOT_Y, ENDSTOP_PIN_ROOT_Z))
        .close()
        .workplane(offset=ENDSTOP_PIN_LENGTH)
        .polyline(endstop_house_profile(ENDSTOP_PIN_TIP_Y, ENDSTOP_PIN_TIP_Z))
        .close()
        .loft(combine=True)
    )


def endstop_rail_receivers() -> cq.Workplane:
    """Return the two local rail-end reinforcement solids."""
    receivers = None
    receiver_center_x = (ENDSTOP_RECEIVER_X_MIN + ENDSTOP_RECEIVER_X_MAX) / 2.0
    receiver_center_z = ENDSTOP_RECEIVER_Z0 + ENDSTOP_RECEIVER_Z / 2.0
    for sign in (-1.0, 1.0):
        center_y = sign * ENDSTOP_RECEIVER_CENTER_Y
        receiver = core.rounded_plate(
            ENDSTOP_RECEIVER_X_MAX - ENDSTOP_RECEIVER_X_MIN,
            ENDSTOP_RECEIVER_Y,
            ENDSTOP_RECEIVER_Z,
            ENDSTOP_RECEIVER_Z0,
            ENDSTOP_RECEIVER_CORNER_R,
        ).translate((receiver_center_x, center_y, 0.0))
        inner_y = sign * ENDSTOP_RECEIVER_RAMP_INNER_Y
        outer_y = sign * (
            ENDSTOP_RECEIVER_INNER_Y + ENDSTOP_RECEIVER_Y
        )
        ramp_profile = [
            (inner_y, ENDSTOP_RECEIVER_RAMP_Z0),
            (outer_y, ENDSTOP_RECEIVER_Z0),
            (outer_y, ENDSTOP_RECEIVER_RAMP_Z1),
            (inner_y, ENDSTOP_RECEIVER_RAMP_Z1),
        ]
        if sign < 0.0:
            ramp_profile.reverse()
        ramp = (
            cq.Workplane("YZ", origin=(ENDSTOP_RECEIVER_X_MIN, 0.0, 0.0))
            .polyline(ramp_profile)
            .close()
            .extrude(ENDSTOP_RECEIVER_X_MAX - ENDSTOP_RECEIVER_X_MIN)
        )
        receiver = receiver.union(ramp)
        receivers = receiver if receivers is None else receivers.union(receiver)
    assert receivers is not None
    return receivers


def endstop_rail_pockets() -> cq.Workplane:
    """Return both 45-degree-roof socket cutters; apply after all rail unions."""
    pockets = None
    for sign in (-1.0, 1.0):
        pocket = (
            cq.Workplane(
                "YZ",
                origin=(
                    ENDSTOP_POCKET_X_MIN,
                    sign * ENDSTOP_RECEIVER_CENTER_Y,
                    ENDSTOP_PIN_CENTER_Z,
                ),
            )
            .polyline(endstop_house_profile(ENDSTOP_POCKET_Y, ENDSTOP_POCKET_Z))
            .close()
            .extrude(
                ENDSTOP_POCKET_X_MAX - ENDSTOP_POCKET_X_MIN
            )
        )
        pockets = pocket if pockets is None else pockets.union(pocket)
    assert pockets is not None
    return pockets


def endstop_tapered_pins() -> cq.Workplane:
    """Return the two identical support-free tapered rail plugs."""
    pins = None
    for sign in (-1.0, 1.0):
        pin = tapered_x_pin(sign * ENDSTOP_RECEIVER_CENTER_Y)
        pins = pin if pins is None else pins.union(pin)
    assert pins is not None
    return pins


# ============================================================
# PRINTABLE MODULES
# ============================================================

def flat_cradle() -> cq.Workplane:
    """Active tablet cradle with two reinforced tapered-pin receivers."""
    cradle = (
        core.flat_main_holder()
        .union(endstop_rail_receivers())
        .cut(endstop_rail_pockets())
    )

    cradle_groove = cross_groove(
        0.0,
        BRACKET_PLATE_CENTER_Y,
        -core.BASE_T - 0.05,
        ALIGNMENT_GROOVE_DEPTH + 0.05,
    )
    return cradle.cut(cradle_groove)


def flat_end_stop() -> cq.Workplane:
    """Return the horizontal, twin-pin left end cap in assembly coordinates."""
    cavity_x = core.TABLET_X + core.FIT_X
    cavity_y = core.TABLET_Y + core.FIT_Y
    rail_top = core.TABLET_Z + core.FIT_Z + core.LIP_T
    wall_h = core.BASE_T + rail_top
    cradle_left_x = -(cavity_x + 2.0 * core.WALL_T) / 2.0
    wall_inner_x = cradle_left_x - ENDSTOP_SEAT_CLEARANCE_X
    wall_outer_x = wall_inner_x - ENDSTOP_OUTER_WALL_X

    outer_wall_center_x = (wall_inner_x + wall_outer_x) / 2.0
    outer_wall_center_y = (ENDSTOP_OUTER_WALL_Y_MIN + ENDSTOP_OUTER_WALL_Y_MAX) / 2.0
    outer_wall = core.softened_plate(
        ENDSTOP_OUTER_WALL_X,
        ENDSTOP_OUTER_WALL_Y_MAX - ENDSTOP_OUTER_WALL_Y_MIN,
        wall_h,
        -core.BASE_T,
        ENDSTOP_CORNER_R,
        ENDSTOP_EDGE_R,
    ).translate((outer_wall_center_x, outer_wall_center_y, 0.0))

    # The screen-facing cap stops short of the long-edge rail lips. Two local
    # pads below it contact the tablet edge through the otherwise open left end.
    cap_left_x = wall_outer_x
    # This bridge terminates at the tablet edge. The actual edge contact comes
    # from the two locator pads; avoiding screen overlap lets the cap push
    # horizontally onto its two rail-end sockets after the tablet is seated.
    cap_right_x = -cavity_x / 2.0
    cap = core.softened_plate(
        cap_right_x - cap_left_x,
        ENDSTOP_CAP_Y,
        core.LIP_T,
        core.TABLET_Z + core.FIT_Z,
        core.LIP_CORNER_R,
        core.LIP_EDGE_R,
    ).translate(((cap_left_x + cap_right_x) / 2.0, 0.0, 0.0))
    locator = None
    for locator_y in ENDSTOP_LOCATOR_Y:
        pad = core.softened_plate(
            core.WALL_T,
            ENDSTOP_LOCATOR_Y_SIZE,
            core.TABLET_Z + core.FIT_Z,
            0.0,
            core.EXPOSED_CORNER_R,
            core.EXPOSED_EDGE_R,
        ).translate((cradle_left_x + core.WALL_T / 2.0, locator_y, 0.0))
        locator = pad if locator is None else locator.union(pad)
    assert locator is not None

    return outer_wall.union(cap).union(locator).union(endstop_tapered_pins())


def rear_bracket_local_plate() -> cq.Workplane:
    """Cradle-parallel mounting plate with captive nuts and open cable clips."""
    plate = core.rounded_plate(
        BRACKET_PLATE_X,
        BRACKET_PLATE_Y,
        BRACKET_PLATE_T,
        BRACKET_PLATE_Z0,
        BRACKET_CORNER_R,
    ).translate((0.0, BRACKET_PLATE_CENTER_Y, 0.0))
    plate_groove = cross_groove(
        0.0,
        BRACKET_PLATE_CENTER_Y,
        BRACKET_PLATE_Z0 + BRACKET_PLATE_T - ALIGNMENT_GROOVE_DEPTH,
        ALIGNMENT_GROOVE_DEPTH + 0.05,
    )
    plate = plate.cut(plate_groove)
    # The clips attach to the rear face of the plate rather than the cradle,
    # leaving the cradle's complete rear frame surface available as a print bed.
    rear_face_z = BRACKET_PLATE_Z0
    clip_center_z = rear_face_z - core.REAR_CLIP_OUTER_Z / 2.0 + 0.05
    for clip_x in BRACKET_CLIP_X:
        clip_outer = cq.Workplane("XY").box(
            core.REAR_CLIP_LENGTH,
            core.REAR_CLIP_OUTER_Y,
            core.REAR_CLIP_OUTER_Z,
        ).translate((clip_x, BRACKET_CLIP_LOCAL_Y, clip_center_z))
        clip_cavity = core.x_cylinder(
            core.BRAIDED_CHANNEL_ID,
            core.REAR_CLIP_LENGTH + 2.0,
            (
                clip_x - core.REAR_CLIP_LENGTH / 2.0 - 1.0,
                BRACKET_CLIP_LOCAL_Y,
                clip_center_z,
            ),
        )
        clip_opening = cq.Workplane("XY").box(
            core.REAR_CLIP_LENGTH + 2.0,
            core.BRAIDED_CHANNEL_SLOT,
            core.REAR_CLIP_OUTER_Z,
        ).translate(
            (
                clip_x,
                BRACKET_CLIP_LOCAL_Y,
                clip_center_z - core.REAR_CLIP_OUTER_Z / 2.0,
            )
        )
        plate = plate.union(clip_outer.cut(clip_cavity).cut(clip_opening))
    return plate


def rear_bracket_installed() -> cq.Workplane:
    """Tilted cradle plate joined to a horizontal, bed-ready sleeve foot."""
    plate = rear_bracket_local_plate().rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
    )

    foot = core.rounded_plate(
        BRACKET_FOOT_X,
        BRACKET_FOOT_Y,
        BRACKET_FOOT_T,
        BRACKET_FOOT_BOTTOM_Z,
        SLEEVE_FLANGE_CORNER_R,
    ).translate((0.0, BRACKET_FOOT_CENTER_Y, 0.0))
    foot_groove = cross_groove(
        0.0,
        BRACKET_FOOT_CENTER_Y,
        BRACKET_FOOT_BOTTOM_Z - 0.05,
        ALIGNMENT_GROOVE_DEPTH + 0.05,
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
    """Closed active sleeve plus a print bed and mounting flange."""
    flange = core.rounded_plate(
        SLEEVE_FLANGE_X,
        SLEEVE_FLANGE_Y,
        SLEEVE_FLANGE_TOP_Z - SLEEVE_FLANGE_BOTTOM_Z,
        SLEEVE_FLANGE_BOTTOM_Z,
        SLEEVE_FLANGE_CORNER_R,
    ).translate((0.0, SLEEVE_FLANGE_CENTER_Y, 0.0))
    flange_groove = cross_groove(
        0.0,
        BRACKET_FOOT_CENTER_Y,
        SLEEVE_FLANGE_TOP_Z - ALIGNMENT_GROOVE_DEPTH,
        ALIGNMENT_GROOVE_DEPTH + 0.05,
    )
    flange = flange.cut(flange_groove)
    return core.vertical_sleeve_with_cable_channel().union(flange)


def alignment_key_print() -> cq.Workplane:
    """Reusable support-free glue-joint key; print two copies."""
    return cross_key(0.0, 0.0, 0.0, ALIGNMENT_KEY_T)


def right_fit_coupon() -> cq.Workplane:
    """Exact right-end cradle crop for tablet-rail and USB-C fit testing."""
    width = RIGHT_FIT_COUPON_X_MAX - RIGHT_FIT_COUPON_X_MIN
    cutter = (
        cq.Workplane("XY")
        .box(width, core.HOLDER_OUTER_Y + 4.0, 30.0)
        .translate(
            (
                (RIGHT_FIT_COUPON_X_MIN + RIGHT_FIT_COUPON_X_MAX) / 2.0,
                0.0,
                4.0,
            )
        )
    )
    return flat_cradle().intersect(cutter)


def right_fit_coupon_print() -> cq.Workplane:
    """Return the right-side coupon on the same rear-face print datum as the cradle."""
    return shift_to_bed(right_fit_coupon())


def button_fit_coupon() -> cq.Workplane:
    """Exact top-left rail crop for button-path and seated-clearance testing."""
    width = BUTTON_FIT_COUPON_X_MAX - BUTTON_FIT_COUPON_X_MIN
    depth = BUTTON_FIT_COUPON_Y_MAX - BUTTON_FIT_COUPON_Y_MIN
    cutter = (
        cq.Workplane("XY")
        .box(width, depth, 30.0)
        .translate(
            (
                (BUTTON_FIT_COUPON_X_MIN + BUTTON_FIT_COUPON_X_MAX) / 2.0,
                (BUTTON_FIT_COUPON_Y_MIN + BUTTON_FIT_COUPON_Y_MAX) / 2.0,
                4.0,
            )
        )
    )
    return flat_cradle().intersect(cutter)


def button_fit_coupon_print() -> cq.Workplane:
    """Return the button coupon on the production cradle's rear-face datum."""
    return shift_to_bed(button_fit_coupon())


def left_slide_coupon_parts() -> tuple[cq.Workplane, cq.Workplane]:
    """Return exact lower-rail crops of one tapered socket and matching pin."""
    cutter = (
        cq.Workplane("XY")
        .box(
            LEFT_SLIDE_COUPON_X_MAX - LEFT_SLIDE_COUPON_X_MIN,
            LEFT_SLIDE_COUPON_Y_MAX - LEFT_SLIDE_COUPON_Y_MIN,
            30.0,
        )
        .translate(
            (
                (LEFT_SLIDE_COUPON_X_MIN + LEFT_SLIDE_COUPON_X_MAX) / 2.0,
                (LEFT_SLIDE_COUPON_Y_MIN + LEFT_SLIDE_COUPON_Y_MAX) / 2.0,
                3.0,
            )
        )
    )
    return flat_cradle().intersect(cutter), flat_end_stop().intersect(cutter)


def left_slide_coupon_print_parts() -> tuple[cq.Workplane, cq.Workplane]:
    """Orient the exact rail-socket and end-cap pin crops like production parts."""
    cradle_coupon, stop_coupon = left_slide_coupon_parts()
    return (
        shift_to_bed(cradle_coupon),
        orient_end_stop_for_print(stop_coupon),
    )


def left_slide_coupon_plate() -> cq.Workplane:
    """Arrange both exact coupon pieces on one compact print plate."""
    cradle_coupon, stop_coupon = left_slide_coupon_print_parts()
    cradle_bb = cradle_coupon.val().BoundingBox()
    stop_bb = stop_coupon.val().BoundingBox()
    cradle_placed = cradle_coupon.translate((-cradle_bb.xmin, -cradle_bb.ymin, 0.0))
    stop_placed = stop_coupon.translate(
        (
            -stop_bb.xmin + cradle_bb.xlen + LEFT_SLIDE_COUPON_PLATE_GAP,
            -stop_bb.ymin,
            0.0,
        )
    )
    compound = cq.Compound.makeCompound([cradle_placed.val(), stop_placed.val()])
    return cq.Workplane("XY").newObject([compound])


def installed_parts() -> tuple[cq.Workplane, cq.Workplane, cq.Workplane, cq.Workplane]:
    """Return cradle, rear bracket, sleeve, and end stop in assembly position."""
    cradle = flat_cradle().rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
    )
    bracket = rear_bracket_installed()
    sleeve = pedestal_sleeve_installed()
    stop = flat_end_stop().rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
    )
    return cradle, bracket, sleeve, stop


def orient_end_stop_for_print(stop: cq.Workplane) -> cq.Workplane:
    """Lay the stop on its broad outside wall so both pins grow vertically."""
    bridge_face_down = stop.rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        180.0,
    )
    outside_wall_down = bridge_face_down.rotate(
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        -90.0,
    )
    return shift_to_bed(outside_wall_down)


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
    stop = orient_end_stop_for_print(flat_end_stop())
    key = shift_to_bed(alignment_key_print())
    return cradle, bracket, sleeve, stop, key


# ============================================================
# EXPORT
# ============================================================

def export() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cradle, bracket, sleeve, stop, key = print_parts()
    cradle_installed, bracket_installed, sleeve_installed, stop_installed = installed_parts()
    left_coupon_cradle, left_coupon_stop = left_slide_coupon_print_parts()

    exports = {
        "tablet_stand_v2_cradle.stl": cradle,
        "tablet_stand_v2_rear_bracket.stl": bracket,
        "tablet_stand_v2_sleeve.stl": sleeve,
        "tablet_stand_v2_end_stop.stl": stop,
        "tablet_stand_v2_alignment_key_print_2.stl": key,
        "tablet_stand_v2_right_fit_coupon.stl": right_fit_coupon_print(),
        "tablet_stand_v2_button_fit_coupon.stl": button_fit_coupon_print(),
        "tablet_stand_v2_left_slide_coupon_cradle.stl": left_coupon_cradle,
        "tablet_stand_v2_left_slide_coupon_stop.stl": left_coupon_stop,
        "tablet_stand_v2_left_slide_coupon_plate.stl": left_slide_coupon_plate(),
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
    assembly.add(stop_installed, name="slide_end_stop", color=cq.Color(0.10, 0.32, 0.55))
    cradle_key_installed = cross_key(
        0.0,
        BRACKET_PLATE_CENTER_Y,
        -core.BASE_T - ALIGNMENT_KEY_T / 2.0,
        ALIGNMENT_KEY_T,
    ).rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
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
        "tablet": {"x": core.TABLET_X, "y": core.TABLET_Y, "z": core.TABLET_Z},
        "fit_allowance_total": {"x": core.FIT_X, "y": core.FIT_Y, "z": core.FIT_Z},
        "tilt_degrees_from_vertical": core.TILT_FROM_VERTICAL_DEG,
        "screen_angle_degrees_above_horizontal": core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
        "tube": {
            "od": 32.0,
            "sleeve_id": core.SLEEVE_ID,
            "sleeve_od": core.SLEEVE_OD,
            "engagement": core.SLEEVE_ENGAGEMENT,
            "seating_cap_thickness": core.SLEEVE_CAP_T,
            "center_offset_behind_screen_plane_y": core.SLEEVE_CENTER_Y,
            "bottom_z": core.SLEEVE_BOTTOM_Z,
        },
        "modules": {
            "cradle": "rear frame face on bed; rail and end-stop features face up",
            "rear_bracket": "horizontal sleeve-interface foot on bed",
            "sleeve": "flange on bed; tube-entry bore open upward",
            "end_stop": "broad outside wall face on bed; twin tapered pins build vertically",
            "alignment_key": "flat on bed; print two identical copies",
            "right_fit_coupon": (
                "rear face on bed; exact 33.5 mm crop of production cradle right end"
            ),
            "button_fit_coupon": (
                "rear face on bed; exact top-left production rail crop"
            ),
            "left_slide_coupon": (
                "exact lower-rail socket/pin crops; cradle rear face down and stop outside wall down"
            ),
        },
        "right_fit_coupon": {
            "purpose": "verify tablet rails, right-edge seating, and USB-C rear turn",
            "x_min": RIGHT_FIT_COUPON_X_MIN,
            "x_max": RIGHT_FIT_COUPON_X_MAX,
            "width": RIGHT_FIT_COUPON_X_MAX - RIGHT_FIT_COUPON_X_MIN,
            "uses_exact_cradle_geometry": True,
        },
        "button_fit_coupon": {
            "purpose": "verify button slide-through path and seated clearance",
            "x_min": BUTTON_FIT_COUPON_X_MIN,
            "x_max": BUTTON_FIT_COUPON_X_MAX,
            "y_min": BUTTON_FIT_COUPON_Y_MIN,
            "y_max": BUTTON_FIT_COUPON_Y_MAX,
            "uses_exact_cradle_geometry": True,
        },
        "left_slide_coupon": {
            "purpose": "verify one support-free tapered rail plug and socket fit",
            "x_min": LEFT_SLIDE_COUPON_X_MIN,
            "x_max": LEFT_SLIDE_COUPON_X_MAX,
            "y_min": LEFT_SLIDE_COUPON_Y_MIN,
            "y_max": LEFT_SLIDE_COUPON_Y_MAX,
            "plate_gap": LEFT_SLIDE_COUPON_PLATE_GAP,
            "uses_exact_cradle_geometry": True,
        },
        "buttons": {
            "edge": "landscape top",
            "group_start_from_top_left": core.BUTTON_GROUP_START_FROM_LEFT,
            "group_end_from_top_left": core.BUTTON_GROUP_END_FROM_LEFT,
            "width_across_tablet_thickness": core.BUTTON_WIDTH_Z,
            "protrusion_from_tablet_edge": core.BUTTON_PROTRUSION_Y,
            "channel_height": core.BUTTON_CHANNEL_Z,
            "channel_depth_into_inner_wall": core.BUTTON_CHANNEL_DEPTH_Y,
            "remaining_outer_wall": core.BUTTON_CHANNEL_REMAINING_OUTER_WALL,
            "channel_end_clearance": core.BUTTON_CHANNEL_END_CLEARANCE_X,
            "channel_open_to_slide_in_end": True,
            "channel_open_through_outer_wall": False,
        },
        "joints": {
            "end_stop": {
                "count": 1,
                "method": "horizontal twin tapered rail plugs; optional adhesive",
                "mechanical_fasteners": 0,
                "travel_axis": "local +X from the open left end",
                "external_landing": False,
                "rear_hooks": 0,
                "pin_count": 2,
                "pin_length": ENDSTOP_PIN_LENGTH,
                "socket_length": ENDSTOP_POCKET_X_MAX - ENDSTOP_POCKET_X_MIN,
                "socket_y": ENDSTOP_POCKET_Y,
                "socket_z": ENDSTOP_POCKET_Z,
                "pin_root_y": ENDSTOP_PIN_ROOT_Y,
                "pin_root_z": ENDSTOP_PIN_ROOT_Z,
                "pin_tip_y": ENDSTOP_PIN_TIP_Y,
                "pin_tip_z": ENDSTOP_PIN_TIP_Z,
                "root_clearance_y_total": ENDSTOP_PIN_ROOT_CLEARANCE_Y,
                "root_clearance_z_total": ENDSTOP_PIN_ROOT_CLEARANCE_Z,
                "tip_clearance_y_total": ENDSTOP_PIN_TIP_CLEARANCE_Y,
                "tip_clearance_z_total": ENDSTOP_PIN_TIP_CLEARANCE_Z,
                "receiver_min_wall": min(
                    (ENDSTOP_RECEIVER_Y - ENDSTOP_POCKET_Y) / 2.0,
                    (ENDSTOP_RECEIVER_Z - ENDSTOP_POCKET_Z) / 2.0,
                ),
            },
            "cradle_to_bracket": {
                "method": "adhesive bond",
                "nominal_area_mm2": CRADLE_BRACKET_BOND_AREA,
                "alignment": "matching cross grooves plus one loose-fit printed alignment key",
            },
            "bracket_to_sleeve": {
                "method": "adhesive bond",
                "nominal_area_mm2": BRACKET_SLEEVE_BOND_AREA,
                "alignment": "matching cross grooves plus one loose-fit printed alignment key",
            },
        },
        "alignment_key": {
            "quantity": ALIGNMENT_KEY_QUANTITY,
            "long": ALIGNMENT_KEY_LONG,
            "short": ALIGNMENT_KEY_SHORT,
            "width": ALIGNMENT_KEY_WIDTH,
            "thickness": ALIGNMENT_KEY_T,
            "edge_chamfer": ALIGNMENT_KEY_EDGE_CHAMFER,
            "groove_long": ALIGNMENT_GROOVE_LONG,
            "groove_short": ALIGNMENT_GROOVE_SHORT,
            "groove_width": ALIGNMENT_GROOVE_WIDTH,
            "groove_depth_each_side": ALIGNMENT_GROOVE_DEPTH,
            "total_clearance_long": ALIGNMENT_GROOVE_LONG - ALIGNMENT_KEY_LONG,
            "total_clearance_short": ALIGNMENT_GROOVE_SHORT - ALIGNMENT_KEY_SHORT,
            "total_clearance_width": ALIGNMENT_GROOVE_WIDTH - ALIGNMENT_KEY_WIDTH,
            "total_clearance_thickness": 2.0 * ALIGNMENT_GROOVE_DEPTH - ALIGNMENT_KEY_T,
        },
        "cable": {
            "braided_cable_diameter": core.BRAIDED_CABLE_D,
            "bracket_clip_x": BRACKET_CLIP_X,
            "sleeve_channel_id": core.BRAIDED_CHANNEL_ID,
            "sleeve_channel_slot": core.BRAIDED_CHANNEL_SLOT,
            "usb_rear_turn_open_rectangle": {
                "x": core.USB_REAR_TURN_SLOT_X,
                "y": core.USB_REAR_TURN_SLOT_Y,
            },
        },
    }
    (OUT / "model_parameters.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Exported tablet stand v2 to {OUT}")


if __name__ == "__main__":
    export()
