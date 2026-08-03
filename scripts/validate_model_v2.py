"""Validate V2 geometry, glue-key alignment, print layouts, and artifacts."""

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
from cad import tablet_stand_v2 as model  # noqa: E402


BUILD = ROOT / "build" / "v2"
REQUIRED = (
    "model_parameters.json",
    "tablet_stand_v2.step",
    "tablet_stand_v2_cradle.stl",
    "tablet_stand_v2_rear_bracket.stl",
    "tablet_stand_v2_sleeve.stl",
    "tablet_stand_v2_end_stop.stl",
    "tablet_stand_v2_alignment_key_print_2.stl",
    "tablet_stand_v2_right_fit_coupon.stl",
    "tablet_stand_v2_button_fit_coupon.stl",
    "tablet_stand_v2_left_slide_coupon_cradle.stl",
    "tablet_stand_v2_left_slide_coupon_stop.stl",
    "tablet_stand_v2_left_slide_coupon_plate.stl",
)


def approximate_support_area(mesh: trimesh.Trimesh, threshold_degrees: float = 45.0) -> float:
    """Return downward face area beyond threshold, excluding bed-contact faces."""
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
    assert core.TILT_FROM_VERTICAL_DEG == 10.0
    assert core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG == 80.0
    assert core.SLEEVE_ID == 32.2
    assert core.SLEEVE_ENGAGEMENT == 51.0

    missing = [name for name in REQUIRED if not (BUILD / name).is_file()]
    assert not missing, f"missing generated artifacts: {', '.join(missing)}"

    metadata = json.loads((BUILD / "model_parameters.json").read_text())
    assert metadata["tube"]["sleeve_id"] == 32.2
    assert metadata["tube"]["engagement"] == 51.0
    assert metadata["fit_allowance_total"] == {"x": 1.0, "y": 1.0, "z": 0.8}
    assert metadata["alignment_key"]["quantity"] == 2
    assert metadata["alignment_key"]["total_clearance_width"] >= 1.0
    assert metadata["alignment_key"]["total_clearance_thickness"] >= 0.4
    assert metadata["joints"]["cradle_to_bracket"]["method"] == "adhesive bond"
    assert metadata["joints"]["bracket_to_sleeve"]["method"] == "adhesive bond"
    assert metadata["right_fit_coupon"]["uses_exact_cradle_geometry"] is True
    assert metadata["button_fit_coupon"]["uses_exact_cradle_geometry"] is True
    assert metadata["left_slide_coupon"]["uses_exact_cradle_geometry"] is True
    assert metadata["cable"]["usb_rear_turn_open_rectangle"] == {"x": 8.0, "y": 16.0}
    assert metadata["buttons"]["group_start_from_top_left"] == 20.0
    assert metadata["buttons"]["group_end_from_top_left"] == 60.0
    assert metadata["buttons"]["width_across_tablet_thickness"] == 2.0
    assert metadata["buttons"]["protrusion_from_tablet_edge"] == 1.0
    assert metadata["buttons"]["channel_height"] == 2.0
    assert metadata["buttons"]["channel_depth_into_inner_wall"] == 1.2
    assert metadata["buttons"]["remaining_outer_wall"] == 1.8
    assert metadata["buttons"]["channel_open_to_slide_in_end"] is True
    assert metadata["buttons"]["channel_open_through_outer_wall"] is False
    assert metadata["joints"]["end_stop"]["mechanical_fasteners"] == 0
    assert metadata["joints"]["end_stop"]["detent_count"] == 2
    assert metadata["joints"]["end_stop"]["nominal_rib_interference_x"] > 0.0

    cradle_flat = model.flat_cradle().val()
    bracket_local = model.rear_bracket_local_plate().val()
    bracket_installed = model.rear_bracket_installed().val()
    sleeve_installed = model.pedestal_sleeve_installed().val()
    stop_flat = model.flat_end_stop().val()
    installed_parts = model.installed_parts()

    # The complete cradle, including its new lower-left landing, retains the
    # broad rear print datum and fits the configured 220 mm bed.
    assert abs(cradle_flat.BoundingBox().zmin + core.BASE_T) < 1e-6
    assert cradle_flat.BoundingBox().xlen <= 217.1
    assert abs(cradle_flat.BoundingBox().ylen - 135.0) < 1e-5
    print(
        "cradle rear datum clear; "
        f"flat envelope={cradle_flat.BoundingBox().xlen:.2f} x "
        f"{cradle_flat.BoundingBox().ylen:.2f} x "
        f"{cradle_flat.BoundingBox().zlen:.2f} mm"
    )

    # The glue grooves remove material only from the intended mating faces.
    assert_open(cradle_flat, (0.0, model.BRACKET_PLATE_CENTER_Y, -2.5), "cradle groove missing")
    assert_solid(cradle_flat, (20.0, model.BRACKET_PLATE_CENTER_Y, -2.5), "cradle bond face missing")
    assert_open(
        bracket_local,
        (0.0, model.BRACKET_PLATE_CENTER_Y, -3.5),
        "bracket plate groove missing",
    )
    assert_solid(
        bracket_local,
        (20.0, model.BRACKET_PLATE_CENTER_Y, -3.5),
        "bracket plate bond face missing",
    )
    assert_open(
        bracket_installed,
        (0.0, model.BRACKET_FOOT_CENTER_Y, model.BRACKET_FOOT_BOTTOM_Z + 0.5),
        "bracket foot groove missing",
    )
    assert_solid(
        bracket_installed,
        (20.0, model.BRACKET_FOOT_CENTER_Y, model.BRACKET_FOOT_BOTTOM_Z + 0.5),
        "bracket foot bond face missing",
    )
    assert_open(
        sleeve_installed,
        (0.0, model.BRACKET_FOOT_CENTER_Y, model.SLEEVE_FLANGE_TOP_Z - 0.5),
        "sleeve flange groove missing",
    )
    assert_solid(
        sleeve_installed,
        (20.0, model.BRACKET_FOOT_CENTER_Y, model.SLEEVE_FLANGE_TOP_Z - 0.5),
        "sleeve flange bond face missing",
    )
    print("both adhesive joints have matching cross-key grooves and broad surrounding faces")

    key = model.alignment_key_print().val()
    key_bb = key.BoundingBox()
    assert abs(key_bb.xlen - model.ALIGNMENT_KEY_LONG) < 1e-6
    assert abs(key_bb.ylen - model.ALIGNMENT_KEY_SHORT) < 1e-6
    assert abs(key_bb.zlen - model.ALIGNMENT_KEY_T) < 1e-6
    assert 2.0 * model.ALIGNMENT_GROOVE_DEPTH > model.ALIGNMENT_KEY_T
    planar_clearances = (
        model.ALIGNMENT_GROOVE_LONG - model.ALIGNMENT_KEY_LONG,
        model.ALIGNMENT_GROOVE_SHORT - model.ALIGNMENT_KEY_SHORT,
        model.ALIGNMENT_GROOVE_WIDTH - model.ALIGNMENT_KEY_WIDTH,
    )
    assert min(planar_clearances) >= 1.0
    thickness_clearance = 2.0 * model.ALIGNMENT_GROOVE_DEPTH - model.ALIGNMENT_KEY_T
    assert thickness_clearance >= 0.4
    print(
        f"alignment key={key_bb.xlen:.1f} x {key_bb.ylen:.1f} x {key_bb.zlen:.1f} mm; "
        f"minimum planar clearance={min(planar_clearances):.2f} mm; "
        f"thickness clearance={thickness_clearance:.2f} mm; "
        f"print quantity={model.ALIGNMENT_KEY_QUANTITY}"
    )

    # Split parts and their keys may touch at designed faces but must never
    # occupy the same volume.
    names = ("cradle", "rear bracket", "sleeve", "end stop")
    for first in range(len(installed_parts)):
        for second in range(first + 1, len(installed_parts)):
            overlap = installed_parts[first].intersect(installed_parts[second]).val().Volume()
            assert overlap < 1e-6, f"{names[first]} overlaps {names[second]} by {overlap:.3f} mm3"
    cradle_key = model.cross_key(
        0.0,
        model.BRACKET_PLATE_CENTER_Y,
        -core.BASE_T - model.ALIGNMENT_KEY_T / 2.0,
        model.ALIGNMENT_KEY_T,
    ).rotate(
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG,
    )
    sleeve_key = model.cross_key(
        0.0,
        model.BRACKET_FOOT_CENTER_Y,
        model.SLEEVE_FLANGE_TOP_Z - model.ALIGNMENT_KEY_T / 2.0,
        model.ALIGNMENT_KEY_T,
    )
    key_checks = (
        ("cradle key/cradle", cradle_key, installed_parts[0]),
        ("cradle key/bracket", cradle_key, installed_parts[1]),
        ("sleeve key/bracket", sleeve_key, installed_parts[1]),
        ("sleeve key/sleeve", sleeve_key, installed_parts[2]),
    )
    for label, alignment_key, mating_part in key_checks:
        overlap = alignment_key.intersect(mating_part).val().Volume()
        assert overlap < 1e-6, f"{label} interference={overlap:.3f} mm3"
    print("installed modules and both alignment keys are interference-free")

    # The screw-free stop slides down the left short edge. Its narrow ribs rub
    # over the base edge, settle into matching grooves, and the lower cradle
    # projection provides a hard seating ledge. Rear hooks remain below the
    # cradle datum and prevent lateral release.
    cradle_left_x = -(
        core.TABLET_X + core.FIT_X + 2.0 * core.WALL_T
    ) / 2.0
    assert_solid(
        cradle_flat,
        (-104.5, -67.0, -1.5),
        "lower-left stop landing missing",
    )
    for detent_y in model.ENDSTOP_DETENT_Y:
        assert_open(
            cradle_flat,
            (cradle_left_x + 0.1, detent_y, model.ENDSTOP_DETENT_CENTER_Z),
            "left-stop detent groove missing",
        )
        assert_solid(
            stop_flat,
            (
                cradle_left_x - model.ENDSTOP_SLIDE_CLEARANCE_X + 0.2,
                detent_y,
                model.ENDSTOP_DETENT_CENTER_Z,
            ),
            "left-stop friction rib missing",
        )
    assert_solid(stop_flat, (-101.0, -52.0, -4.2), "lower rear guide hook missing")
    assert_solid(stop_flat, (-101.0, 52.0, -4.2), "upper rear guide hook missing")
    assert_open(stop_flat, (-101.0, -52.0, -3.1), "rear hook consumes cradle clearance")
    assert_solid(stop_flat, (-100.75, -42.0, 4.0), "tablet edge locator missing")
    assert core.LEFT_RAIL_ENTRY_RELIEF_X >= 4.0

    insertion_overlaps = []
    for slide_offset_y in (90.0, 70.0, 50.0, 30.0, 10.0):
        overlap = model.flat_cradle().intersect(
            model.flat_end_stop().translate((0.0, slide_offset_y, 0.0))
        ).val().Volume()
        insertion_overlaps.append(overlap)
        assert overlap < 1.0, (
            f"hard collision during left-stop insertion at Y+{slide_offset_y:.0f}: "
            f"{overlap:.3f} mm3"
        )
    assert model.flat_cradle().intersect(model.flat_end_stop()).val().Volume() < 1e-6
    print(
        "screw-free left stop has two friction detents, rear capture hooks, "
        f"a lower landing, and collision-free slide travel apart from <= "
        f"{max(insertion_overlaps):.2f} mm3 intentional rib interference"
    )

    # The right-side coupon is a literal crop of the production cradle. It
    # retains both long-edge rails, the full right cap, the plug pocket, and
    # the open rear-turn slot while omitting the center glue joint.
    coupon = model.right_fit_coupon().val()
    coupon_bb = coupon.BoundingBox()
    assert abs(coupon_bb.xmin - model.RIGHT_FIT_COUPON_X_MIN) < 1e-6
    assert abs(coupon_bb.xmax - model.RIGHT_FIT_COUPON_X_MAX) < 1e-6
    assert abs(coupon_bb.ylen - core.HOLDER_OUTER_Y) < 1e-6
    assert_open(coupon, (90.0, 0.0, 4.0), "coupon tablet cavity obstructed")
    assert_open(coupon, (104.0, 0.0, 4.0), "coupon USB-C pocket obstructed")
    assert_solid(coupon, (110.0, 0.0, 4.0), "coupon outer USB-C wall missing")
    assert_open(
        coupon,
        (core.TABLET_X / 2.0 + core.USB_PLUG_PROJECTION, 0.0, -1.5),
        "coupon rear-turn slot missing",
    )
    rectangle_entry_x = (core.TABLET_X + core.FIT_X) / 2.0 + 0.5
    assert_open(
        coupon,
        (rectangle_entry_x, 0.0, -1.5),
        "coupon cable rectangle is not open to tablet cavity",
    )
    assert_solid(
        coupon,
        (rectangle_entry_x, core.USB_REAR_TURN_SLOT_Y / 2.0 + 1.0, -1.5),
        "coupon cable rectangle removes excess pocket floor",
    )
    print(
        "right fit coupon is an exact cradle crop; "
        f"envelope={coupon_bb.xlen:.2f} x {coupon_bb.ylen:.2f} x "
        f"{coupon_bb.zlen:.2f} mm; open cable rectangle="
        f"{core.USB_REAR_TURN_SLOT_Y:.1f} x {core.USB_REAR_TURN_SLOT_X:.1f} mm"
    )

    # The top-left coupon is a literal crop of the production rail. Its slot
    # remains open at the slide-in end, clears the entire measured seated
    # button group, and ends in intact wall after the 5 mm overrun.
    button_coupon = model.button_fit_coupon().val()
    button_coupon_bb = button_coupon.BoundingBox()
    assert abs(button_coupon_bb.xmin - model.BUTTON_FIT_COUPON_X_MIN) < 1e-6
    assert abs(button_coupon_bb.xmax - model.BUTTON_FIT_COUPON_X_MAX) < 1e-6
    assert abs(button_coupon_bb.ymin - model.BUTTON_FIT_COUPON_Y_MIN) < 1e-6
    top_wall_inner_y = (
        (core.TABLET_Y + core.FIT_Y) / 2.0 + core.BUTTON_CHANNEL_DEPTH_Y / 2.0
    )
    top_wall_outer_y = (
        (core.TABLET_Y + core.FIT_Y) / 2.0
        + core.BUTTON_CHANNEL_DEPTH_Y
        + core.BUTTON_CHANNEL_REMAINING_OUTER_WALL / 2.0
    )
    button_center_z = core.TABLET_Z / 2.0
    seated_button_start_x = -core.TABLET_X / 2.0 + core.BUTTON_GROUP_START_FROM_LEFT
    seated_button_end_x = -core.TABLET_X / 2.0 + core.BUTTON_GROUP_END_FROM_LEFT
    assert_open(
        button_coupon,
        (model.BUTTON_FIT_COUPON_X_MIN + 0.5, top_wall_inner_y, button_center_z),
        "internal button groove is not open at the slide-in end",
    )
    for button_x in (seated_button_start_x, seated_button_end_x):
        assert_open(
            button_coupon,
            (button_x, top_wall_inner_y, button_center_z),
            "internal button groove obstructs the measured seated button group",
        )
        assert_solid(
            button_coupon,
            (button_x, top_wall_outer_y, button_center_z),
            "button groove breaks through the exterior rail wall",
        )
    assert_solid(
        button_coupon,
        (core.BUTTON_CHANNEL_FINAL_X + 1.0, top_wall_inner_y, button_center_z),
        "button coupon does not retain wall beyond the relief",
    )
    assert_solid(
        button_coupon,
        (seated_button_start_x, top_wall_inner_y, core.BUTTON_CHANNEL_Z0 - 0.5),
        "button channel removes the lower rail wall",
    )
    print(
        "button fit coupon is an exact top-rail crop; "
        f"envelope={button_coupon_bb.xlen:.2f} x {button_coupon_bb.ylen:.2f} x "
        f"{button_coupon_bb.zlen:.2f} mm; internal channel="
        f"{core.BUTTON_CHANNEL_Z:.1f} mm high x {core.BUTTON_CHANNEL_DEPTH_Y:.1f} mm deep; "
        f"outer wall={core.BUTTON_CHANNEL_REMAINING_OUTER_WALL:.1f} mm"
    )

    left_coupon_cradle, left_coupon_stop = model.left_slide_coupon_parts()
    assert len(left_coupon_cradle.solids().vals()) == 1
    assert len(left_coupon_stop.solids().vals()) == 1
    assert_solid(
        left_coupon_cradle.val(),
        (-104.5, -67.0, -1.5),
        "slide coupon omits the lower landing",
    )
    assert_solid(
        left_coupon_stop.val(),
        (-101.0, -52.0, -4.2),
        "slide coupon omits the rear hook",
    )
    print("left-slide coupon pair is an exact production crop of the landing, hook, and detent")

    # Preserve the user-tested tube path and seating cap.
    tube_axis_z = core.SLEEVE_BOTTOM_Z + core.SLEEVE_ENGAGEMENT / 2.0
    cap_axis_z = core.SLEEVE_TOP_Z - core.SLEEVE_CAP_T / 2.0
    assert_open(
        sleeve_installed,
        (0.0, core.SLEEVE_CENTER_Y, tube_axis_z),
        "tube bore obstructed",
    )
    assert_solid(
        sleeve_installed,
        (0.0, core.SLEEVE_CENTER_Y, cap_axis_z),
        "seating cap missing",
    )
    assert abs(sleeve_installed.BoundingBox().zmin - core.HOLDER_BOTTOM_Z) < 1e-6
    print("32.2 mm bore clear; 51 mm engagement and 3 mm seating cap preserved")

    print_parts = model.print_parts()
    for part in print_parts:
        assert abs(part.val().BoundingBox().zmin) < 1e-6

    for path in sorted(BUILD.glob("*.stl")):
        mesh = trimesh.load_mesh(path, force="mesh")
        components = len(mesh.split(only_watertight=False))
        assert mesh.is_watertight, f"{path.name} is not watertight"
        expected_components = 2 if path.name == "tablet_stand_v2_left_slide_coupon_plate.stl" else 1
        assert components == expected_components, (
            f"{path.name} has {components} components; expected {expected_components}"
        )
        support_area = approximate_support_area(mesh)
        print(
            f"{path.name}: watertight, {components} component(s), "
            f"extents={mesh.extents.round(2).tolist()}, "
            f"approx_overhang_area={support_area:.0f} mm2"
        )

    print("V2 validation passed")


if __name__ == "__main__":
    main()
