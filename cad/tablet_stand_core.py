"""Active shared measurements and base geometry for the V2 tablet stand.

Coordinates:
    X: tablet left (-) to right / USB-C side (+)
    Y: viewer / bottom edge (-) to far / top edge (+)
    Z: up

The tablet plane is 10 degrees back from vertical (80 degrees above horizontal).
All dimensions are millimeters. This module owns the measured cradle, sleeve,
button, and cable geometry used by the modular V2 assembly.
"""

from __future__ import annotations

import math

import cadquery as cq

# Tablet and fit
TABLET_X = 200.0
TABLET_Y = 123.0
TABLET_Z = 8.4
FIT_X = 1.0
FIT_Y = 1.0
FIT_Z = 0.8
TILT_FROM_VERTICAL_DEG = 10.0
SCREEN_ANGLE_FROM_HORIZONTAL_DEG = 90.0 - TILT_FROM_VERTICAL_DEG

# Skeletal frame and retaining rails
BASE_T = 3.0
FRAME_W = 10.0
WALL_T = 3.0
# The supplied tablet mesh has an approximately 7 mm plan corner radius. The
# front-frame opening follows that curve; the outer radius is deliberately much
# larger to give the visible holder a pronounced, soft silhouette.
FRAME_INNER_CORNER_R = 7.0
FRAME_OUTER_CORNER_R = 28.0
# Rail walls are 3 mm thick, so their plan fillet is capped just below the
# 1.5 mm half-thickness; the larger frame corners above carry the visual change.
EXPOSED_CORNER_R = 1.45
LIP_CORNER_R = 1.05
EXPOSED_EDGE_R = 0.70
LIP_EDGE_R = 0.60
LIP_OVERLAP = 2.2
LIP_T = 2.0
LEFT_RAIL_ENTRY_RELIEF_X = 4.0
RIGHT_STOP_SPAN = 25.0
CENTER_PLATE_X = 74.0
CENTER_PLATE_Y = 64.0
SPINE_W = 12.0
HOLDER_OUTER_Y = TABLET_Y + FIT_Y + 2.0 * WALL_T
HOLDER_BOTTOM_Z = (
    -HOLDER_OUTER_Y / 2.0 * math.sin(math.radians(SCREEN_ANGLE_FROM_HORIZONTAL_DEG))
    - BASE_T * math.cos(math.radians(SCREEN_ANGLE_FROM_HORIZONTAL_DEG))
)

# User-measured power/volume group on the landscape top edge. Distances run
# rightward from the tablet's top-left corner. The buttons project outward from
# the long edge and are centered across the tablet's 8.4 mm thickness.
BUTTON_GROUP_START_FROM_LEFT = 20.0
BUTTON_GROUP_END_FROM_LEFT = 60.0
BUTTON_WIDTH_Z = 2.0
BUTTON_PROTRUSION_Y = 1.0
BUTTON_CHANNEL_DEPTH_Y = 1.2
BUTTON_CHANNEL_END_CLEARANCE_X = 5.0
BUTTON_CHANNEL_FINAL_X = (
    -TABLET_X / 2.0
    + BUTTON_GROUP_END_FROM_LEFT
    + BUTTON_CHANNEL_END_CLEARANCE_X
)
BUTTON_CHANNEL_Z0 = (TABLET_Z - BUTTON_WIDTH_Z) / 2.0
BUTTON_CHANNEL_Z = BUTTON_WIDTH_Z
BUTTON_CHANNEL_REMAINING_OUTER_WALL = WALL_T - BUTTON_CHANNEL_DEPTH_Y

# USB-C plug pocket and rear-hidden cable route.
USB_PLUG_PROJECTION = 6.50
USB_POCKET_X_CLEARANCE = 1.50
USB_POCKET_INNER_X = USB_PLUG_PROJECTION + USB_POCKET_X_CLEARANCE
USB_POCKET_Y = 30.0
USB_END_WALL_T = 3.0
USB_POCKET_CEILING_T = 2.0
# Physical cable tests superseded the earlier T-shaped 3 x 16 mm slot plus
# 6 x 8.5 mm entry notch.  Preserve the complete original 16 x 8 mm opening
# from the tablet edge through the plug-pocket floor, then add the user's
# green-marked 4 mm inboard relief.  The rear-floor opening is therefore
# 16 x 12 mm overall (Y x X), while the full 8 mm-deep plug chamber above it
# remains unchanged for the measured 6.50 mm plug projection.
USB_REAR_TURN_SLOT_INBOARD_X = 4.0
USB_REAR_TURN_SLOT_OUTBOARD_X = 8.0
USB_REAR_TURN_SLOT_X = USB_REAR_TURN_SLOT_INBOARD_X + USB_REAR_TURN_SLOT_OUTBOARD_X
USB_REAR_TURN_SLOT_Y = 16.0
RIGHT_ANGLE_PIGTAIL_LENGTH = 51.4
RIGHT_ANGLE_FLAT_T = 0.6
DOWNSTREAM_CONNECTOR_BODY = 9.6

# Confirmed round braided cable and open snap-in routing features.  The channel
# is external to the sleeve so the tested 32.2 mm bore remains untouched.
BRAIDED_CABLE_D = 3.45
BRAIDED_CHANNEL_CLEARANCE = 0.70
BRAIDED_CHANNEL_ID = BRAIDED_CABLE_D + BRAIDED_CHANNEL_CLEARANCE
BRAIDED_CHANNEL_SLOT = 2.8
BRAIDED_CHANNEL_OUTER_X = 7.2
BRAIDED_CHANNEL_OUTER_Y = 4.6
BRAIDED_CHANNEL_EMBED = 1.2
REAR_CLIP_LENGTH = 6.0
REAR_CLIP_OUTER_Y = 7.2
REAR_CLIP_OUTER_Z = 5.2
REAR_CLIP_CENTER_Z = -5.4

# Pedestal sleeve and reinforcement
SLEEVE_ID = 32.2
SLEEVE_WALL = 4.0
SLEEVE_OD = SLEEVE_ID + 2.0 * SLEEVE_WALL
SLEEVE_LENGTH = 50.0
# Lower the complete rear sleeve assembly until its bottom is level with the
# installed holder's lower long edge. The sleeve's 54 mm overall body height,
# 51 mm clear engagement, and 3 mm seating cap remain unchanged.
SLEEVE_BOTTOM_Z = HOLDER_BOTTOM_Z
SLEEVE_TOP_Z = SLEEVE_BOTTOM_Z + SLEEVE_LENGTH + 4.0
SLEEVE_CAP_T = 3.0
SLEEVE_ENGAGEMENT = SLEEVE_TOP_Z - SLEEVE_BOTTOM_Z - SLEEVE_CAP_T
SLEEVE_CENTER_Y = 24.0
BRAIDED_CHANNEL_TOP_Z = SLEEVE_TOP_Z - 4.0
BRAIDED_CHANNEL_BOTTOM_Z = BRAIDED_CHANNEL_TOP_Z - 50.0

def rounded_plate(x: float, y: float, z: float, z0: float, radius: float) -> cq.Workplane:
    """Create a rectangular prism with rounded vertical corners."""
    result = cq.Workplane("XY").workplane(offset=z0).rect(x, y).extrude(z)
    if radius > 0:
        result = result.edges("|Z").fillet(radius)
    return result


def softened_plate(
    x: float,
    y: float,
    z: float,
    z0: float,
    corner_radius: float,
    edge_radius: float,
) -> cq.Workplane:
    """Create a rounded plate with its remaining top/bottom edges filleted."""
    result = rounded_plate(x, y, z, z0, corner_radius)
    if edge_radius > 0:
        result = result.edges("not |Z").fillet(edge_radius)
    return result


def front_softened_plate(
    x: float,
    y: float,
    z: float,
    z0: float,
    corner_radius: float,
    edge_radius: float,
) -> cq.Workplane:
    """Create a rounded plate with only its screen/front-side edges filleted.

    This keeps a complete flat rear print datum when a V3 perimeter wall is
    fused into the rear frame, avoiding tangent duplicate edges in tessellation.
    """
    result = rounded_plate(x, y, z, z0, corner_radius)
    if edge_radius > 0:
        result = result.edges(">Z").fillet(edge_radius)
    return result


def x_cylinder(diameter: float, length: float, origin: tuple[float, float, float]) -> cq.Workplane:
    """Create a cylinder whose axis points in +X."""
    return cq.Workplane("YZ", origin=origin).circle(diameter / 2.0).extrude(length)


def flat_main_holder(
    exposed_edge_radius: float = EXPOSED_EDGE_R,
    lip_edge_radius: float = LIP_EDGE_R,
    rail_entry_relief_x: float = LEFT_RAIL_ENTRY_RELIEF_X,
    button_channel_x_end: float = BUTTON_CHANNEL_FINAL_X,
    include_lips: bool = True,
    include_right_cap: bool = True,
) -> cq.Workplane:
    """Return the active V2 cradle base before modular joint features.

    V2 retains the tested defaults. V3 can close the historical left rail lead,
    extend the concealed button groove, and replace the overlapping individual
    lips/cap with one continuous screen-facing perimeter without changing the
    historical V2 geometry or any mating dimensions.
    """
    cavity_x = TABLET_X + FIT_X
    cavity_y = TABLET_Y + FIT_Y
    outer_x = cavity_x + 2.0 * WALL_T
    outer_y = HOLDER_OUTER_Y
    rail_top = TABLET_Z + FIT_Z + LIP_T

    # Open-backed perimeter with a central plate and four connecting spokes.
    outer = softened_plate(
        outer_x,
        outer_y,
        BASE_T,
        -BASE_T,
        FRAME_OUTER_CORNER_R,
        exposed_edge_radius,
    )
    inner = rounded_plate(
        outer_x - 2.0 * FRAME_W,
        outer_y - 2.0 * FRAME_W,
        BASE_T + 2.0,
        -BASE_T - 1.0,
        FRAME_INNER_CORNER_R,
    )
    frame = outer.cut(inner)
    center = rounded_plate(CENTER_PLATE_X, CENTER_PLATE_Y, BASE_T, -BASE_T, 5.0)
    x_spine = cq.Workplane("XY").box(outer_x - 12.0, SPINE_W, BASE_T).translate((0, 0, -BASE_T / 2.0))
    y_spine = cq.Workplane("XY").box(SPINE_W, outer_y - 12.0, BASE_T).translate((0, 0, -BASE_T / 2.0))
    main = frame.union(center).union(x_spine).union(y_spine)

    # Long-edge U rails. Their right ends reach the closed USB-C housing. V2
    # keeps the historical rail-free lead for its separate end stop; active V3
    # overrides it so the integral left closure meets each rail continuously.
    wall_h = BASE_T + rail_top
    rail_left_x = -outer_x / 2.0 + rail_entry_relief_x
    usb_end_wall_inner_x = cavity_x / 2.0 + USB_POCKET_INNER_X
    usb_end_wall_center_x = usb_end_wall_inner_x + USB_END_WALL_T / 2.0
    usb_outer_x = usb_end_wall_inner_x + USB_END_WALL_T
    rail_x = usb_outer_x - rail_left_x
    rail_center_x = (usb_outer_x + rail_left_x) / 2.0
    for sign in (-1.0, 1.0):
        wall_y = sign * (cavity_y / 2.0 + WALL_T / 2.0)
        wall = softened_plate(
            rail_x,
            WALL_T,
            wall_h,
            -BASE_T,
            EXPOSED_CORNER_R,
            exposed_edge_radius,
        ).translate(
            (rail_center_x, wall_y, 0)
        )
        main = main.union(wall)
        if include_lips:
            lip_y = sign * (cavity_y / 2.0 - LIP_OVERLAP / 2.0)
            lip = softened_plate(
                rail_x,
                LIP_OVERLAP,
                LIP_T,
                TABLET_Z + FIT_Z,
                LIP_CORNER_R,
                lip_edge_radius,
            ).translate(
                (rail_center_x, lip_y, 0)
            )
            main = main.union(lip)

    # Recess only the inner face of the top rail at button height. The 1.2 mm
    # depth clears the 1 mm projection while preserving a continuous 1.8 mm
    # exterior wall and the screen-facing retaining perimeter. V2 ends 5 mm
    # beyond the seated group; V3 extends the same concealed groove to its seam.
    button_channel_x0 = rail_left_x - 0.2
    button_channel_x = button_channel_x_end - button_channel_x0
    button_channel_y0 = cavity_y / 2.0 - 0.2
    button_channel_y1 = cavity_y / 2.0 + BUTTON_CHANNEL_DEPTH_Y
    button_channel = (
        cq.Workplane("XY")
        .workplane(offset=BUTTON_CHANNEL_Z0)
        .rect(button_channel_x, button_channel_y1 - button_channel_y0)
        .extrude(BUTTON_CHANNEL_Z)
        .translate(
            (
                (button_channel_x0 + button_channel_x_end) / 2.0,
                (button_channel_y0 + button_channel_y1) / 2.0,
                0.0,
            )
        )
    )
    main = main.cut(button_channel)

    # A continuous, full-depth screen-facing cap covers the complete right side
    # from the tablet edge to the solid outer USB-C wall. Behind it, two
    # internal stop walls locate the tablet while their central gap still lets
    # the tablet slide onto a USB-C plug resting in the pocket.
    stop_x = cavity_x / 2.0 + WALL_T / 2.0
    right_cap_left_x = cavity_x / 2.0 - LIP_OVERLAP
    right_cap_x = usb_outer_x - right_cap_left_x
    if include_right_cap:
        right_cap = rounded_plate(
            right_cap_x,
            outer_y,
            USB_POCKET_CEILING_T,
            TABLET_Z + FIT_Z,
            LIP_CORNER_R,
        ).translate(((right_cap_left_x + usb_outer_x) / 2.0, 0, 0))
        main = main.union(right_cap)
    for sign in (-1.0, 1.0):
        stop_y = sign * (cavity_y / 2.0 - RIGHT_STOP_SPAN / 2.0)
        wall = rounded_plate(WALL_T, RIGHT_STOP_SPAN, wall_h, -BASE_T, EXPOSED_CORNER_R).translate(
            (stop_x, stop_y, 0)
        )
        main = main.union(wall)

    # The plug pocket encloses the measured 6.50 mm projection.  Its outer end
    # is solid; the right-angle adapter turns through the broad rear slot so its
    # 0.6 mm pigtail can lie behind the tablet instead of exiting to the right.
    usb_pocket_x = USB_POCKET_INNER_X + USB_END_WALL_T
    usb_pocket_center_x = cavity_x / 2.0 + usb_pocket_x / 2.0
    cable_floor = rounded_plate(
        usb_pocket_x, USB_POCKET_Y, BASE_T, -BASE_T, EXPOSED_CORNER_R
    ).translate((usb_pocket_center_x, 0, 0))
    usb_end_wall = rounded_plate(
        USB_END_WALL_T,
        outer_y,
        wall_h,
        -BASE_T,
        EXPOSED_CORNER_R,
    ).translate((usb_end_wall_center_x, 0, 0))
    rear_turn_slot = (
        cq.Workplane("XY")
        .box(USB_REAR_TURN_SLOT_X, USB_REAR_TURN_SLOT_Y, BASE_T + 2.0)
        .translate(
            (
                cavity_x / 2.0
                + (USB_REAR_TURN_SLOT_OUTBOARD_X - USB_REAR_TURN_SLOT_INBOARD_X) / 2.0,
                0.0,
                -BASE_T / 2.0,
            )
        )
    )
    # Cut after unioning so the enlarged rectangle includes both the complete
    # original 8 mm outboard floor opening and the green-marked 4 mm inboard
    # relief.  The plug chamber above still reaches the unchanged outer wall.
    main = (
        main.union(cable_floor)
        .union(usb_end_wall)
        .cut(rear_turn_slot)
    )

    return main


def vertical_sleeve() -> cq.Workplane:
    sleeve = (
        cq.Workplane("XY")
        .workplane(offset=SLEEVE_BOTTOM_Z)
        .circle(SLEEVE_OD / 2.0)
        .circle(SLEEVE_ID / 2.0)
        .extrude(SLEEVE_TOP_Z - SLEEVE_BOTTOM_Z)
        .translate((0, SLEEVE_CENTER_Y, 0))
    )
    cap = (
        cq.Workplane("XY")
        .workplane(offset=SLEEVE_TOP_Z - SLEEVE_CAP_T)
        .circle(SLEEVE_OD / 2.0)
        .extrude(SLEEVE_CAP_T)
        .translate((0, SLEEVE_CENTER_Y, 0))
    )
    return sleeve.union(cap)


def vertical_sleeve_with_cable_channel() -> cq.Workplane:
    """Add a rear-facing snap channel without opening the tube bore."""
    channel_length = BRAIDED_CHANNEL_TOP_Z - BRAIDED_CHANNEL_BOTTOM_Z
    sleeve_back_y = SLEEVE_CENTER_Y + SLEEVE_OD / 2.0
    cavity_y = sleeve_back_y + BRAIDED_CHANNEL_ID / 2.0 - BRAIDED_CHANNEL_EMBED
    outer_center_y = sleeve_back_y + BRAIDED_CHANNEL_OUTER_Y / 2.0 - 0.5
    outer = cq.Workplane("XY").box(
        BRAIDED_CHANNEL_OUTER_X, BRAIDED_CHANNEL_OUTER_Y, channel_length
    ).translate((0, outer_center_y, (BRAIDED_CHANNEL_TOP_Z + BRAIDED_CHANNEL_BOTTOM_Z) / 2.0))
    cavity = (
        cq.Workplane("XY")
        .workplane(offset=BRAIDED_CHANNEL_BOTTOM_Z - 1.0)
        .center(0, cavity_y)
        .circle(BRAIDED_CHANNEL_ID / 2.0)
        .extrude(channel_length + 2.0)
    )
    opening_depth = BRAIDED_CHANNEL_OUTER_Y + 2.0
    opening = cq.Workplane("XY").box(
        BRAIDED_CHANNEL_SLOT, opening_depth, channel_length + 2.0
    ).translate(
        (
            0,
            cavity_y + opening_depth / 2.0,
            (BRAIDED_CHANNEL_TOP_Z + BRAIDED_CHANNEL_BOTTOM_Z) / 2.0,
        )
    )
    return vertical_sleeve().union(outer).cut(cavity).cut(opening)
