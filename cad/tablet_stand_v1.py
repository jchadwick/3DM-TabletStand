"""Parametric first concept for the 2024 onn. 8-inch tablet stand.

Coordinates:
    X: tablet left (-) to right / USB-C side (+)
    Y: viewer / bottom edge (-) to far / top edge (+)
    Z: up

The tablet plane is 10 degrees back from vertical (80 degrees above horizontal).
Its +Y / top edge is higher and farther from the user.  The support tube remains
vertical and is offset behind the screen plane.
All dimensions are millimeters.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import cadquery as cq


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "v1"

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
FRAME_OUTER_CORNER_R = 4.0
FRAME_INNER_CORNER_R = 3.0
EXPOSED_CORNER_R = 1.2
LIP_CORNER_R = 0.8
LIP_OVERLAP = 2.2
LIP_T = 2.0
RIGHT_STOP_SPAN = 25.0
CENTER_PLATE_X = 74.0
CENTER_PLATE_Y = 64.0
SPINE_W = 12.0
HOLDER_OUTER_Y = TABLET_Y + FIT_Y + 2.0 * WALL_T
HOLDER_BOTTOM_Z = (
    -HOLDER_OUTER_Y / 2.0 * math.sin(math.radians(SCREEN_ANGLE_FROM_HORIZONTAL_DEG))
    - BASE_T * math.cos(math.radians(SCREEN_ANGLE_FROM_HORIZONTAL_DEG))
)

# USB-C plug pocket and rear-hidden cable route.
USB_PLUG_PROJECTION = 6.50
USB_POCKET_X_CLEARANCE = 1.50
USB_POCKET_INNER_X = USB_PLUG_PROJECTION + USB_POCKET_X_CLEARANCE
USB_POCKET_Y = 30.0
USB_END_WALL_T = 3.0
USB_POCKET_CEILING_T = 2.0
USB_REAR_TURN_SLOT_X = 3.0
USB_REAR_TURN_SLOT_Y = 16.0
RIGHT_ANGLE_PIGTAIL_LENGTH = 51.4
RIGHT_ANGLE_FLAT_T = 0.6
DOWNSTREAM_CONNECTOR_BODY = 9.6

# Confirmed round braided cable and connector-passable routing holes. No
# cable-sized captive channels are used, and the sleeve bore remains untouched.
BRAIDED_CABLE_D = 3.45
CABLE_PASS_ID = 18.0
CABLE_EYELET_OD = 24.0
CABLE_EYELET_T = 6.0
HOLDER_EYELET_X = 34.0
HOLDER_EYELET_Z = -8.0

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
GUSSET_T = 4.0
SLEEVE_EYELET_X = SLEEVE_OD / 2.0 + CABLE_PASS_ID / 2.0 + 0.5
SLEEVE_EYELET_Z = (-25.0, -49.0)

# M3 removable end stop
M3_CLEARANCE = 3.4
M3_PILOT = 2.7
ENDSTOP_PAD_Y = 18.0
ENDSTOP_PAD_Z = 8.0


def rounded_plate(x: float, y: float, z: float, z0: float, radius: float) -> cq.Workplane:
    """Create a rectangular prism with rounded vertical corners."""
    result = cq.Workplane("XY").workplane(offset=z0).rect(x, y).extrude(z)
    if radius > 0:
        result = result.edges("|Z").fillet(radius)
    return result


def x_cylinder(diameter: float, length: float, origin: tuple[float, float, float]) -> cq.Workplane:
    """Create a cylinder whose axis points in +X."""
    return cq.Workplane("YZ", origin=origin).circle(diameter / 2.0).extrude(length)


def flat_main_holder() -> cq.Workplane:
    cavity_x = TABLET_X + FIT_X
    cavity_y = TABLET_Y + FIT_Y
    outer_x = cavity_x + 2.0 * WALL_T
    outer_y = HOLDER_OUTER_Y
    rail_top = TABLET_Z + FIT_Z + LIP_T

    # Open-backed perimeter with a central plate and four connecting spokes.
    outer = rounded_plate(outer_x, outer_y, BASE_T, -BASE_T, FRAME_OUTER_CORNER_R)
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

    # Long-edge U rails.  The left ends remain open so the tablet can slide in.
    # Their right ends reach the closed USB-C housing.
    wall_h = BASE_T + rail_top
    rail_left_x = -outer_x / 2.0
    usb_end_wall_inner_x = cavity_x / 2.0 + USB_POCKET_INNER_X
    usb_end_wall_center_x = usb_end_wall_inner_x + USB_END_WALL_T / 2.0
    usb_outer_x = usb_end_wall_inner_x + USB_END_WALL_T
    rail_x = usb_outer_x - rail_left_x
    rail_center_x = (usb_outer_x + rail_left_x) / 2.0
    for sign in (-1.0, 1.0):
        wall_y = sign * (cavity_y / 2.0 + WALL_T / 2.0)
        wall = rounded_plate(rail_x, WALL_T, wall_h, -BASE_T, EXPOSED_CORNER_R).translate(
            (rail_center_x, wall_y, 0)
        )
        lip_y = sign * (cavity_y / 2.0 - LIP_OVERLAP / 2.0)
        lip = rounded_plate(rail_x, LIP_OVERLAP, LIP_T, TABLET_Z + FIT_Z, LIP_CORNER_R).translate(
            (rail_center_x, lip_y, 0)
        )
        main = main.union(wall).union(lip)

    # Two internal corner stops locate the tablet at its right edge while the
    # central gap lets it slide onto a USB-C plug already resting in the case.
    stop_x = cavity_x / 2.0 + WALL_T / 2.0
    for sign in (-1.0, 1.0):
        stop_y = sign * (cavity_y / 2.0 - RIGHT_STOP_SPAN / 2.0)
        wall = rounded_plate(WALL_T, RIGHT_STOP_SPAN, wall_h, -BASE_T, EXPOSED_CORNER_R).translate(
            (stop_x, stop_y, 0)
        )
        lip = rounded_plate(
            LIP_OVERLAP, RIGHT_STOP_SPAN, LIP_T, TABLET_Z + FIT_Z, LIP_CORNER_R
        ).translate(
            (cavity_x / 2.0 - LIP_OVERLAP / 2.0, stop_y, 0)
        )
        main = main.union(wall).union(lip)

    # The plug pocket encloses the measured 6.50 mm projection.  Its outer end
    # is solid; the right-angle adapter turns through the broad rear slot so its
    # 0.6 mm pigtail can lie behind the tablet instead of exiting to the right.
    usb_pocket_x = USB_POCKET_INNER_X + USB_END_WALL_T
    usb_pocket_center_x = cavity_x / 2.0 + usb_pocket_x / 2.0
    cable_floor = rounded_plate(
        usb_pocket_x, USB_POCKET_Y, BASE_T, -BASE_T, EXPOSED_CORNER_R
    ).translate((usb_pocket_center_x, 0, 0))
    cable_ceiling = rounded_plate(
        usb_pocket_x,
        USB_POCKET_Y,
        USB_POCKET_CEILING_T,
        TABLET_Z + FIT_Z,
        EXPOSED_CORNER_R,
    ).translate((usb_pocket_center_x, 0, 0))
    usb_end_wall = rounded_plate(
        USB_END_WALL_T, outer_y, wall_h, -BASE_T, EXPOSED_CORNER_R
    ).translate((usb_end_wall_center_x, 0, 0))
    rear_turn_slot = (
        cq.Workplane("XY")
        .box(USB_REAR_TURN_SLOT_X, USB_REAR_TURN_SLOT_Y, BASE_T + 2.0)
        .translate((TABLET_X / 2.0 + USB_PLUG_PROJECTION, 0, -BASE_T / 2.0))
    )
    main = main.union(cable_floor.cut(rear_turn_slot)).union(cable_ceiling).union(usb_end_wall)

    # One wide rear eyelet accepts the complete connector, not just the wire.
    # Its 18 mm clear hole is deliberately generous around the photographed
    # 9.6 mm connector-body mark.
    eyelet_outer = x_cylinder(
        CABLE_EYELET_OD,
        CABLE_EYELET_T,
        (HOLDER_EYELET_X - CABLE_EYELET_T / 2.0, 0, HOLDER_EYELET_Z),
    )
    eyelet_hole = x_cylinder(
        CABLE_PASS_ID,
        CABLE_EYELET_T + 2.0,
        (HOLDER_EYELET_X - CABLE_EYELET_T / 2.0 - 1.0, 0, HOLDER_EYELET_Z),
    )
    main = main.union(eyelet_outer.cut(eyelet_hole))

    # Reinforced lug for the single M3 end-stop screw.  The printed pilot hole
    # is intentionally simple; it can be drilled to suit the actual screw.
    lug_x0 = -outer_x / 2.0 - 1.0
    lug_length = 28.0
    lug = cq.Workplane("XY").box(lug_length, ENDSTOP_PAD_Y, ENDSTOP_PAD_Z).translate(
        (lug_x0 + lug_length / 2.0, 0, -ENDSTOP_PAD_Z / 2.0)
    )
    pilot = x_cylinder(M3_PILOT, 24.0, (lug_x0 - 1.0, 0, -4.0))
    main = main.union(lug).cut(pilot)
    return main


def flat_end_stop() -> cq.Workplane:
    cavity_x = TABLET_X + FIT_X
    cavity_y = TABLET_Y + FIT_Y
    outer_y = cavity_y + 2.0 * WALL_T
    rail_top = TABLET_Z + FIT_Z + LIP_T
    wall_h = BASE_T + rail_top
    stop_x = -cavity_x / 2.0 - WALL_T / 2.0

    wall = rounded_plate(WALL_T, outer_y, wall_h, -BASE_T, EXPOSED_CORNER_R).translate(
        (stop_x, 0, 0)
    )
    lip = rounded_plate(LIP_OVERLAP, cavity_y, LIP_T, TABLET_Z + FIT_Z, LIP_CORNER_R).translate(
        (-cavity_x / 2.0 + LIP_OVERLAP / 2.0, 0, 0)
    )
    pad = cq.Workplane("XY").box(8.0, ENDSTOP_PAD_Y, ENDSTOP_PAD_Z).translate(
        (-cavity_x / 2.0 - 4.0, 0, -ENDSTOP_PAD_Z / 2.0)
    )
    clearance = x_cylinder(M3_CLEARANCE, 12.0, (-cavity_x / 2.0 - 10.0, 0, -4.0))
    return wall.union(lip).union(pad).cut(clearance)


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


def vertical_sleeve_with_cable_eyelets() -> cq.Workplane:
    """Add two wide connector-pass holes beside, never through, the sleeve."""
    result = vertical_sleeve()
    for center_z in SLEEVE_EYELET_Z:
        eyelet = (
            cq.Workplane("XY")
            .workplane(offset=center_z - CABLE_EYELET_T / 2.0)
            .center(SLEEVE_EYELET_X, SLEEVE_CENTER_Y)
            .circle(CABLE_EYELET_OD / 2.0)
            .circle(CABLE_PASS_ID / 2.0)
            .extrude(CABLE_EYELET_T)
        )
        result = result.union(eyelet)
    return result


def gussets() -> cq.Workplane:
    # Two triangular ribs connect the nearly vertical backplate to the sleeve,
    # which is offset behind the tablet so it cannot intrude into the cavity.
    # Points are (Y, Z) in the installed coordinate system.
    sleeve_drop = SLEEVE_BOTTOM_Z + SLEEVE_LENGTH
    rib_profile = [
        (-2.5, -31.0),
        (8.5, 31.0),
        (22.0, 4.0 + sleeve_drop),
        (22.0, -22.0 + sleeve_drop),
    ]
    ribs = None
    for x in (-13.0, 13.0):
        rib = (
            cq.Workplane("YZ", origin=(x - GUSSET_T / 2.0, 0, 0))
            .polyline(rib_profile)
            .close()
            .extrude(GUSSET_T)
        )
        ribs = rib if ribs is None else ribs.union(rib)
    assert ribs is not None
    return ribs


def installed_parts() -> tuple[cq.Workplane, cq.Workplane]:
    main_tilted = flat_main_holder().rotate(
        (0, 0, 0), (1, 0, 0), SCREEN_ANGLE_FROM_HORIZONTAL_DEG
    )
    stop_tilted = flat_end_stop().rotate(
        (0, 0, 0), (1, 0, 0), SCREEN_ANGLE_FROM_HORIZONTAL_DEG
    )
    main_installed = main_tilted.union(vertical_sleeve_with_cable_eyelets()).union(gussets())
    # Re-bore after unioning the gussets so no hidden rib material intrudes into
    # the tested 32.2 mm tube path.  A deliberate 3 mm seating cap remains.
    bore = (
        cq.Workplane("XY")
        .workplane(offset=SLEEVE_BOTTOM_Z)
        .circle(SLEEVE_ID / 2.0)
        .extrude(SLEEVE_ENGAGEMENT)
        .translate((0, SLEEVE_CENTER_Y, 0))
    )
    main_installed = main_installed.cut(bore)
    return main_installed, stop_tilted


def export() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    main, stop_installed = installed_parts()
    stop_print = flat_end_stop()

    cq.exporters.export(main, str(OUT / "tablet_stand_main.stl"), tolerance=0.08, angularTolerance=0.15)
    cq.exporters.export(stop_print, str(OUT / "tablet_stand_end_stop.stl"), tolerance=0.08, angularTolerance=0.15)
    cq.exporters.export(stop_installed, str(OUT / "tablet_stand_end_stop_installed.stl"), tolerance=0.08, angularTolerance=0.15)

    assembly = cq.Assembly(name="tablet_stand_v1")
    assembly.add(main, name="main_holder", color=cq.Color(0.12, 0.14, 0.17))
    assembly.add(stop_installed, name="m3_end_stop", color=cq.Color(0.10, 0.32, 0.55))
    assembly.save(str(OUT / "tablet_stand_v1.step"))

    metadata = {
        "units": "mm",
        "tablet": {"x": TABLET_X, "y": TABLET_Y, "z": TABLET_Z},
        "fit_allowance_total": {"x": FIT_X, "y": FIT_Y, "z": FIT_Z},
        "tilt_degrees_from_vertical": TILT_FROM_VERTICAL_DEG,
        "screen_angle_degrees_above_horizontal": SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
        "orientation": "top edge higher and farther from user; bottom edge lower and nearer",
        "tube": {
            "od": 32.0,
            "sleeve_id": SLEEVE_ID,
            "sleeve_od": SLEEVE_OD,
            "body_length": SLEEVE_LENGTH,
            "engagement": SLEEVE_ENGAGEMENT,
            "seating_cap_thickness": SLEEVE_CAP_T,
            "center_offset_behind_screen_plane_y": SLEEVE_CENTER_Y,
            "bottom_z": SLEEVE_BOTTOM_Z,
            "holder_bottom_z": HOLDER_BOTTOM_Z,
            "bottom_alignment": "sleeve bottom level with holder lower long edge",
        },
        "retention": "left slide-in; one M3 screw end stop",
        "usb_c": {
            "side": "right",
            "position": "center",
            "plug_projection": USB_PLUG_PROJECTION,
            "pocket_clearance_x": USB_POCKET_X_CLEARANCE,
            "right_angle_pigtail_length": RIGHT_ANGLE_PIGTAIL_LENGTH,
            "flat_cable_thickness": RIGHT_ANGLE_FLAT_T,
            "downstream_connector_body_marked_dimension": DOWNSTREAM_CONNECTOR_BODY,
            "braided_cable_diameter": BRAIDED_CABLE_D,
            "connector_pass_hole_id": CABLE_PASS_ID,
            "routing": "right-angle pigtail turns behind tablet; complete cable passes through 18 mm eyelets beside the sleeve",
        },
    }
    (OUT / "model_parameters.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Exported tablet stand v1 to {OUT}")


if __name__ == "__main__":
    export()
