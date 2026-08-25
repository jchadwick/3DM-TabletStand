"""Validate the V3 removable tongue/wedge cradle joint and exports."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import cadquery as cq
import numpy as np
import trimesh


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cad import tablet_stand_core as core  # noqa: E402
from cad import tablet_stand_v2 as v2  # noqa: E402
from cad import tablet_stand_v3 as model  # noqa: E402


BUILD = ROOT / "build" / "v3"
REQUIRED = (
    "model_parameters.json",
    "tablet_stand_v3.step",
    "tablet_stand_v3_cradle_left.stl",
    "tablet_stand_v3_cradle_right.stl",
    "tablet_stand_v3_rear_bracket.stl",
    "tablet_stand_v3_sleeve.stl",
    "tablet_stand_v3_alignment_key_print_1.stl",
    "tablet_stand_v3_locking_wedge.stl",
    "tablet_stand_v3_lock_coupon_left.stl",
    "tablet_stand_v3_lock_coupon_right.stl",
    "tablet_stand_v3_lock_coupon_wedge.stl",
    "tablet_stand_v3_lock_coupon_all3.stl",
)


def approximate_support_area(mesh: trimesh.Trimesh, threshold_degrees: float = 45.0) -> float:
    triangles = mesh.triangles
    normals = mesh.face_normals
    areas = mesh.area_faces
    zmin = mesh.bounds[0, 2]
    downward = normals[:, 2] < -math.cos(math.radians(threshold_degrees))
    on_bed = np.max(triangles[:, :, 2], axis=1) < zmin + 0.05
    return float(areas[downward & ~on_bed].sum())


def assert_open(shape: cq.Shape, point: tuple[float, float, float], message: str) -> None:
    assert not shape.isInside(cq.Vector(*point)), message


def assert_solid(shape: cq.Shape, point: tuple[float, float, float], message: str) -> None:
    assert shape.isInside(cq.Vector(*point)), message


def main() -> None:
    missing = [name for name in REQUIRED if not (BUILD / name).is_file()]
    assert not missing, f"missing generated artifacts: {', '.join(missing)}"

    metadata = json.loads((BUILD / "model_parameters.json").read_text())
    assert metadata["revision"] == "v3 removable tongue-and-wedge split cradle"
    assert metadata["cradle_split"]["total_clearance"] == model.CRADLE_SEAM_CLEARANCE
    assert metadata["cradle_split"]["rear_bracket_bridges_center_seam"] is True
    assert metadata["separate_left_cap"] is False
    assert metadata["cradle_split"]["adhesive_required"] is False
    assert metadata["removable_joint"]["tongue_count"] == 3
    assert metadata["removable_joint"]["root_clearance_total"] >= 0.4
    assert metadata["removable_joint"]["tip_clearance_total"] >= 0.8
    assert metadata["removable_joint"]["locking_channel"]["bridge"] <= 10.0
    assert metadata["lock_coupon"]["uses_exact_production_geometry"] is True
    assert metadata["structural_assembly"]["rear_bracket_bond"] == "fixed right cradle wing only"
    assert metadata["structural_assembly"]["left_wing_serviceable"] is True
    assert metadata["structural_assembly"]["alignment_key_quantity"] == 1
    assert metadata["finish"]["screen_opening_size"] == [
        model.FRONT_OPENING_X,
        model.FRONT_OPENING_Y,
    ]
    assert metadata["finish"]["screen_opening_corner_radius"] == model.FRONT_OPENING_CORNER_R
    assert metadata["finish"]["screen_opening_tablet_overlap"] == model.FRONT_CORNER_TABLET_OVERLAP
    assert metadata["finish"]["rail_wall_edge_fillet"] == model.V3_EXTERIOR_RAIL_WALL_EDGE_R
    assert metadata["finish"]["lip_edge_fillet"] == model.V3_EXTERIOR_LIP_CAP_EDGE_R
    assert metadata["finish"]["left_closure_edge_fillet"] == model.LEFT_CLOSURE_EDGE_R
    assert metadata["finish"]["continuous_exterior_edge_rounding"] is True
    assert metadata["usb_c"]["plug_chamber_depth"] == core.USB_POCKET_INNER_X
    assert metadata["usb_c"]["rear_turn_opening"] == {
        "x": core.USB_REAR_TURN_SLOT_X,
        "y": core.USB_REAR_TURN_SLOT_Y,
        "inboard_from_tablet_edge": core.USB_REAR_TURN_SLOT_INBOARD_X,
        "outboard_from_tablet_edge": core.USB_REAR_TURN_SLOT_OUTBOARD_X,
    }
    assert metadata["usb_c"]["outer_wall_thickness"] == core.USB_END_WALL_T

    source = model.split_cradle_source()
    left, right = model.cradle_halves()
    left_shape = left.val()
    right_shape = right.val()
    left_bb = left_shape.BoundingBox()
    right_bb = right_shape.BoundingBox()
    assert len(left.solids().vals()) == 1
    assert len(right.solids().vals()) == 1
    assert left.intersect(right).val().Volume() < 1e-6
    assert max(left_bb.xlen, right_bb.xlen) < 130.0
    assert max(left_bb.ylen, right_bb.ylen) < 145.0
    assert max(left_bb.xlen, left_bb.ylen, right_bb.xlen, right_bb.ylen) < 220.0
    assert abs(left_bb.zmin + core.BASE_T) < 1e-6
    assert abs(right_bb.zmin + core.BASE_T) < 1e-6
    print(
        "split cradle is interference-free and bed-friendly; "
        f"left={left_bb.xlen:.2f} x {left_bb.ylen:.2f} x {left_bb.zlen:.2f} mm, "
        f"right={right_bb.xlen:.2f} x {right_bb.ylen:.2f} x {right_bb.zlen:.2f} mm"
    )

    # Three bed-supported tongues enter open-ended sockets along +X.  Check
    # representative tongue material, socket voids, receiver roofs, and the
    # closed seating backs on the actual split solids.
    for center_y in (*model.OUTER_JOINT_CENTER_Y, 0.0):
        tongue_z = 0.0 if center_y else -1.5
        assert_solid(left_shape, (5.0, center_y, tongue_z), "joint tongue missing")
        assert_open(right_shape, (5.0, center_y, tongue_z), "joint socket obstructed")
        assert_solid(right_shape, (20.5, center_y, -1.5), "joint socket lacks seating back")
    for center_y in model.OUTER_JOINT_CENTER_Y:
        assert_solid(right_shape, (5.0, center_y, 4.5), "outer receiver roof missing")
        assert_open(right_shape, (5.0, center_y, -2.8), "outer receiver floor is not bed-open")

    assert model.OUTER_SOCKET_ROOT_Y - model.OUTER_TONGUE_ROOT_Y >= 0.4
    assert model.OUTER_SOCKET_TIP_Y - model.OUTER_TONGUE_TIP_Y >= 0.8
    assert model.CENTER_SOCKET_ROOT_Y - model.CENTER_TONGUE_ROOT_Y >= 0.4
    assert model.CENTER_SOCKET_TIP_Y - model.CENTER_TONGUE_TIP_Y >= 0.8
    for slide_offset_x in (-30.0, -24.0, -18.0, -12.0, -6.0, 0.0):
        overlap = left.translate((slide_offset_x, 0.0, 0.0)).intersect(right).val().Volume()
        assert overlap < 1e-6, (
            f"hard collision during left-wing insertion at X{slide_offset_x:.0f}: "
            f"{overlap:.3f} mm3"
        )
    print(
        "three integral tongues have collision-free +X insertion, closed seats, "
        f"{model.JOINT_ROOT_CLEARANCE_TOTAL:.2f} mm root clearance, and "
        f"{model.JOINT_TIP_CLEARANCE_TOTAL:.2f} mm lead clearance"
    )

    # The removable lower wedge passes through the aligned 4 mm channel.  Its
    # head remains outside the receiver, and the same channel clears an M3
    # shaft if metal hardware is needed after the coupon test.
    wedge = model.locking_wedge_installed()
    assert wedge.intersect(left).val().Volume() < 1e-6
    assert wedge.intersect(right).val().Volume() < 1e-6
    assert_open(left_shape, (model.LOCK_CENTER_X, model.LOCK_CENTER_Y, 0.0), "left lock channel missing")
    assert_open(right_shape, (model.LOCK_CENTER_X, model.LOCK_CENTER_Y, 0.0), "right lock channel missing")
    assert model.LOCK_CHANNEL_X >= model.M3_FALLBACK_DIAMETER + 0.5
    assert model.LOCK_CHANNEL_Z >= model.M3_FALLBACK_DIAMETER + 0.5
    for wedge_offset_y in (-12.0, -8.0, -4.0, 0.0):
        moving_wedge = wedge.translate((0.0, wedge_offset_y, 0.0))
        assert moving_wedge.intersect(left).val().Volume() < 1e-6
        assert moving_wedge.intersect(right).val().Volume() < 1e-6
    print("tapered lower cross-wedge is removable and the channel accepts an M3 fallback")

    coupon_left, coupon_right, coupon_wedge = model.lock_coupon_parts()
    assert len(coupon_left.solids().vals()) == 1
    assert len(coupon_right.solids().vals()) == 1
    assert len(coupon_wedge.solids().vals()) == 1
    assert coupon_left.intersect(coupon_right).val().Volume() < 1e-6
    coupon_plate_parts = model.lock_coupon_print_plate_parts()
    coupon_plate = model.lock_coupon_print_plate()
    assert len(coupon_plate.solids().vals()) == 3
    assert abs(coupon_plate.val().BoundingBox().zmin) < 1e-6
    assert coupon_plate.val().BoundingBox().xlen < 90.0
    assert coupon_plate.val().BoundingBox().ylen < 40.0
    assert math.isclose(
        sum(part.val().Volume() for part in coupon_plate_parts),
        sum(part.val().Volume() for part in (coupon_left, coupon_right, coupon_wedge)),
        rel_tol=0.0,
        abs_tol=1e-5,
    )
    print("three-piece lock coupon uses exact production tongue, receiver, and wedge geometry")

    # V3 retains the user-tested button and USB-C plug chamber while enlarging
    # the rear-floor opening by the green-marked 4 mm inboard area.
    assert_open(left_shape, (-80.0, 62.5, core.TABLET_Z / 2.0), "button channel obstructed")
    assert_solid(left_shape, (-80.0, 64.0, core.TABLET_Z / 2.0), "button outer wall missing")
    tablet_right_x = (core.TABLET_X + core.FIT_X) / 2.0
    rear_floor_z = -core.BASE_T / 2.0
    plug_chamber_z = core.TABLET_Z / 2.0
    assert math.isclose(core.USB_REAR_TURN_SLOT_X, 12.0, abs_tol=1e-9)
    assert math.isclose(core.USB_REAR_TURN_SLOT_Y, 16.0, abs_tol=1e-9)
    assert math.isclose(core.USB_REAR_TURN_SLOT_INBOARD_X, 4.0, abs_tol=1e-9)
    assert math.isclose(core.USB_REAR_TURN_SLOT_OUTBOARD_X, 8.0, abs_tol=1e-9)
    assert_open(
        right_shape,
        (tablet_right_x - 3.5, 0.0, rear_floor_z),
        "USB-C rear opening lacks the green-marked inboard relief",
    )
    assert_open(
        right_shape,
        (tablet_right_x + 7.5, 0.0, rear_floor_z),
        "USB-C rear opening does not retain the original 8 mm outboard span",
    )
    assert_solid(
        right_shape,
        (tablet_right_x + 8.5, 0.0, rear_floor_z),
        "USB-C rear opening extends into the solid outer wall",
    )
    assert_solid(
        right_shape,
        (tablet_right_x, core.USB_REAR_TURN_SLOT_Y / 2.0 + 1.0, rear_floor_z),
        "USB-C rear opening exceeds its retained 16 mm width",
    )
    for chamber_x in (tablet_right_x + 0.5, tablet_right_x + core.USB_PLUG_PROJECTION):
        assert_open(
            right_shape,
            (chamber_x, 0.0, plug_chamber_z),
            "USB-C plug chamber above the relocated floor opening was narrowed",
        )
    left_wall_x = -(
        core.TABLET_X + core.FIT_X + 2.0 * core.WALL_T
    ) / 2.0 - v2.ENDSTOP_OUTER_WALL_X / 2.0
    wall_edge_samples = (
        -model.V3_OUTER_Y / 2.0 + 2.0,
        0.0,
        model.V3_OUTER_Y / 2.0 - 2.0,
    )
    for y_pos in wall_edge_samples:
        assert_solid(
            left_shape,
            (left_wall_x, y_pos, 4.0),
            "integral left outer wall is not continuous",
        )
        assert_solid(
            left_shape,
            (-100.0, y_pos, core.TABLET_Z + core.FIT_Z + core.LIP_T / 2.0),
            "integral left screen-facing cap is not continuous",
        )
        right_wall_x = (
            core.TABLET_X + core.FIT_X
        ) / 2.0 + core.USB_POCKET_INNER_X + core.USB_END_WALL_T / 2.0
        assert_solid(
            right_shape,
            (right_wall_x, y_pos, 4.0),
            "integral right USB-C outer wall is not continuous",
        )
        assert_solid(
            right_shape,
            (core.TABLET_X / 2.0 + core.USB_PLUG_PROJECTION, y_pos, core.TABLET_Z + core.FIT_Z + core.LIP_T / 2.0),
            "integral right screen-facing cap is not continuous",
        )
    assert_open(left_shape, (-98.0, 0.0, 4.0), "integral left closure blocks tablet cavity")

    # The successful right-wing fit is preserved below the lip plane, while a
    # tablet-concentric 5.3 mm opening curve now covers the four nominal 7 mm
    # tablet-front corners.  The inner samples ensure this remains a narrow
    # corner treatment rather than an unnecessarily intrusive bezel.
    front_z = core.TABLET_Z + core.FIT_Z + core.LIP_T / 2.0
    for x_sign in (-1.0, 1.0):
        wing_shape = left_shape if x_sign < 0.0 else right_shape
        for y_sign in (-1.0, 1.0):
            assert_solid(
                wing_shape,
                (x_sign * 97.0, y_sign * 58.5, front_z),
                "rounded front-corner cover is missing",
            )
            assert_open(
                wing_shape,
                (x_sign * 96.5, y_sign * 58.0, front_z),
                "rounded front-corner cover intrudes beyond its 5.3 mm opening radius",
            )
    assert math.isclose(model.FRONT_CORNER_TABLET_OVERLAP, 1.70, abs_tol=1e-9)
    assert math.isclose(
        model.FRONT_CORNER_TABLET_OVERLAP,
        core.LIP_OVERLAP - core.FIT_X / 2.0,
        abs_tol=1e-9,
    )
    assert math.isclose(model.FRONT_OPENING_CORNER_R, 5.30, abs_tol=1e-9)
    assert left_bb.ylen >= model.V3_OUTER_Y
    assert right_bb.ylen >= model.V3_OUTER_Y

    # Change 3 is a cross-sectional exterior treatment, not another plan-corner
    # change.  Near-edge samples must be open while deeper points remain solid
    # along all four long-rail segments and both full-span short walls.  The
    # 0.40/0.20 mm central lands keep the 3.0/2.0 mm sections printable, and
    # flat rear-datum samples plus the sharp screen-opening transition confirm
    # that neither build orientation nor the approved overlap was sacrificed.
    assert math.isclose(model.V3_EXTERIOR_RAIL_WALL_EDGE_R, 1.30, abs_tol=1e-9)
    assert math.isclose(model.V3_EXTERIOR_LIP_CAP_EDGE_R, 0.90, abs_tol=1e-9)
    assert model.V3_EXTERIOR_RAIL_WALL_EDGE_R > core.EXPOSED_EDGE_R
    assert model.V3_EXTERIOR_LIP_CAP_EDGE_R > core.LIP_EDGE_R
    assert math.isclose(
        metadata["finish"]["rail_wall_edge_land"],
        core.WALL_T - 2.0 * model.V3_EXTERIOR_RAIL_WALL_EDGE_R,
        abs_tol=1e-9,
    )
    assert math.isclose(
        metadata["finish"]["lip_cap_edge_land"],
        core.LIP_T - 2.0 * model.V3_EXTERIOR_LIP_CAP_EDGE_R,
        abs_tol=1e-9,
    )
    assert metadata["finish"]["rail_wall_edge_land"] >= 0.39
    assert metadata["finish"]["lip_cap_edge_land"] >= 0.19

    rail_top = core.TABLET_Z + core.FIT_Z + core.LIP_T
    outer_y = model.V3_OUTER_Y / 2.0
    for wing_shape, x_pos in ((left_shape, -50.0), (right_shape, 50.0)):
        for y_sign in (-1.0, 1.0):
            assert_open(
                wing_shape,
                (x_pos, y_sign * (outer_y - 0.2), rail_top - 0.2),
                "pronounced long-rail exterior fillet is missing",
            )
            assert_solid(
                wing_shape,
                (x_pos, y_sign * (outer_y - 0.8), rail_top - 0.8),
                "long-rail exterior fillet breaks through its wall",
            )
            assert_solid(
                wing_shape,
                (x_pos, y_sign * (outer_y - 1.6), -core.BASE_T + 0.01),
                "rear-face-down print datum was rounded away",
            )
        opening_y = model.FRONT_OPENING_Y / 2.0
        assert_open(
            wing_shape,
            (x_pos, opening_y - 0.05, rail_top - 0.05),
            "screen opening was narrowed by the exterior fillet",
        )
        assert_solid(
            wing_shape,
            (x_pos, opening_y + 0.05, rail_top - 0.05),
            "screen-opening overlap was rounded away",
        )

    left_outer_x = -(
        core.TABLET_X + core.FIT_X + 2.0 * core.WALL_T
    ) / 2.0 - v2.ENDSTOP_OUTER_WALL_X
    right_outer_x = (
        core.TABLET_X + core.FIT_X
    ) / 2.0 + core.USB_POCKET_INNER_X + core.USB_END_WALL_T
    for wing_shape, outer_x, x_sign in (
        (left_shape, left_outer_x, -1.0),
        (right_shape, right_outer_x, 1.0),
    ):
        assert_open(
            wing_shape,
            (outer_x - x_sign * 0.2, 0.0, rail_top - 0.2),
            "pronounced short-wall exterior fillet is missing",
        )
        assert_solid(
            wing_shape,
            (outer_x - x_sign * 0.8, 0.0, rail_top - 0.8),
            "short-wall exterior fillet breaks through its wall",
        )
    print(
        "continuous V3 exterior uses 1.30 mm rail/wall and 0.90 mm lip/cap edge fillets "
        "with flat rear datums and unchanged screen-opening overlap"
    )

    print(
        "tested button, USB-C chamber, and tablet fit are preserved; the 16 x 12 mm "
        "rear opening adds 4 mm inboard to the original 8 mm outboard span, and "
        "5.30 mm screen-opening corners conceal the tablet's 7 mm front corners "
        "with 1.70 mm overlap"
    )

    # The bracket spans the seam geometrically but is bonded only to the fixed
    # right wing.  The left rear face stays ungrooved and removable.
    assert_solid(left_shape, (-20.0, v2.BRACKET_PLATE_CENTER_Y, -2.5), "left bond land missing")
    assert_solid(right_shape, (20.0, v2.BRACKET_PLATE_CENTER_Y, -2.5), "right bond land missing")
    bracket_xmin = -v2.BRACKET_PLATE_X / 2.0
    bracket_xmax = v2.BRACKET_PLATE_X / 2.0
    assert bracket_xmin < model.CRADLE_SEAM_X < bracket_xmax
    assert metadata["cradle_split"]["adhesive_required"] is False
    print("rear bracket spans the seam but bonds only to the fixed right wing")

    for part in model.print_parts():
        assert abs(part.val().BoundingBox().zmin) < 1e-6

    for path in sorted(BUILD.glob("*.stl")):
        mesh = trimesh.load_mesh(path, force="mesh")
        components = len(mesh.split(only_watertight=False))
        assert mesh.is_watertight, f"{path.name} is not watertight"
        expected_components = 3 if path.name == "tablet_stand_v3_lock_coupon_all3.stl" else 1
        assert components == expected_components, f"{path.name} has {components} components"
        print(
            f"{path.name}: watertight, extents={mesh.extents.round(2).tolist()}, "
            f"approx_overhang_area={approximate_support_area(mesh):.0f} mm2"
        )

    print("V3 split-cradle validation passed")


if __name__ == "__main__":
    main()
