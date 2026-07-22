"""Validate the active tablet-stand geometry and generated manufacturing files."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import cadquery as cq
import trimesh


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cad import tablet_stand_v1 as model  # noqa: E402


BUILD = ROOT / "build" / "v1"
REQUIRED = (
    "model_parameters.json",
    "tablet_stand_main.stl",
    "tablet_stand_end_stop.stl",
    "tablet_stand_end_stop_installed.stl",
    "tablet_stand_v1.step",
)


def main() -> None:
    assert model.TILT_FROM_VERTICAL_DEG == 10.0
    assert model.SCREEN_ANGLE_FROM_HORIZONTAL_DEG == 80.0
    rise = model.TABLET_Y * math.sin(math.radians(model.SCREEN_ANGLE_FROM_HORIZONTAL_DEG))
    setback = model.TABLET_Y * math.cos(math.radians(model.SCREEN_ANGLE_FROM_HORIZONTAL_DEG))
    print(f"tablet edge rise={rise:.2f} mm; horizontal setback={setback:.2f} mm")

    main_holder, _ = model.installed_parts()
    shape = main_holder.val()
    tilted_holder = model.flat_main_holder().rotate(
        (0, 0, 0), (1, 0, 0), model.SCREEN_ANGLE_FROM_HORIZONTAL_DEG
    )
    actual_holder_bottom_z = tilted_holder.val().BoundingBox().zmin
    actual_sleeve_bottom_z = model.vertical_sleeve_with_cable_channel().val().BoundingBox().zmin
    assert abs(actual_holder_bottom_z - model.HOLDER_BOTTOM_Z) < 1e-6
    assert abs(actual_sleeve_bottom_z - actual_holder_bottom_z) < 1e-6
    print(f"holder and sleeve bottoms aligned at z={actual_holder_bottom_z:.2f} mm")

    tube_axis_z = model.SLEEVE_BOTTOM_Z + model.SLEEVE_ENGAGEMENT / 2.0
    tube_axis = cq.Vector(0, model.SLEEVE_CENTER_Y, tube_axis_z)
    cap_axis = cq.Vector(0, model.SLEEVE_CENTER_Y, model.SLEEVE_TOP_Z - model.SLEEVE_CAP_T / 2.0)
    assert not shape.isInside(tube_axis), "tube path is obstructed"
    assert shape.isInside(cap_axis), "seating cap is not solid"
    print("tube path clear; seating cap solid")

    missing = [name for name in REQUIRED if not (BUILD / name).is_file()]
    assert not missing, f"missing generated artifacts: {', '.join(missing)}"

    metadata = json.loads((BUILD / "model_parameters.json").read_text())
    assert metadata["tilt_degrees_from_vertical"] == 10.0
    assert metadata["screen_angle_degrees_above_horizontal"] == 80.0
    assert metadata["tube"]["sleeve_id"] == 32.2
    assert metadata["usb_c"]["plug_projection"] == 6.5
    assert metadata["usb_c"]["braided_cable_diameter"] == 3.45
    assert metadata["usb_c"]["braided_channel_id"] > metadata["usb_c"]["braided_cable_diameter"]

    # Check the right-side concept in its unrotated construction plane: the
    # outer end and full-depth screen-facing cap are continuous, its rear turn
    # slot is open, and the plug chamber plus supporting floor remain
    # clear/solid where expected.
    flat_holder = model.flat_main_holder().val()
    cavity_right_x = (model.TABLET_X + model.FIT_X) / 2.0
    end_wall_center_x = cavity_right_x + model.USB_POCKET_INNER_X + model.USB_END_WALL_T / 2.0
    assert flat_holder.isInside(cq.Vector(end_wall_center_x, 30.0, model.TABLET_Z / 2.0))
    assert flat_holder.isInside(cq.Vector(end_wall_center_x, 0.0, model.TABLET_Z / 2.0))
    right_cap_z = model.TABLET_Z + model.FIT_Z + model.USB_POCKET_CEILING_T / 2.0
    for cap_x in (cavity_right_x - model.LIP_OVERLAP / 2.0, cavity_right_x + 4.0, end_wall_center_x):
        for cap_y in (-50.0, 0.0, 50.0):
            assert flat_holder.isInside(cq.Vector(cap_x, cap_y, right_cap_z))
    assert not flat_holder.isInside(cq.Vector(cavity_right_x + 3.0, 0.0, model.TABLET_Z / 2.0))
    rear_turn_x = model.TABLET_X / 2.0 + model.USB_PLUG_PROJECTION
    assert not flat_holder.isInside(cq.Vector(rear_turn_x, 0.0, -model.BASE_T / 2.0))
    assert flat_holder.isInside(cq.Vector(rear_turn_x - 3.0, 0.0, -model.BASE_T / 2.0))
    clip_x = model.REAR_CLIP_X[-1]
    assert not flat_holder.isInside(cq.Vector(clip_x, 0.0, model.REAR_CLIP_CENTER_Z))
    assert flat_holder.isInside(cq.Vector(clip_x, 3.0, model.REAR_CLIP_CENTER_Z))
    print("right screen-facing cap and USB-C outer end continuous; rear route and clips clear")

    sleeve_back_y = model.SLEEVE_CENTER_Y + model.SLEEVE_OD / 2.0
    channel_y = sleeve_back_y + model.BRAIDED_CHANNEL_ID / 2.0 - model.BRAIDED_CHANNEL_EMBED
    remaining_sleeve_wall = (
        channel_y - model.BRAIDED_CHANNEL_ID / 2.0
    ) - (model.SLEEVE_CENTER_Y + model.SLEEVE_ID / 2.0)
    assert remaining_sleeve_wall >= 2.8 - 1e-6
    assert not shape.isInside(cq.Vector(0.0, channel_y, -25.0))
    assert shape.isInside(cq.Vector(3.0, channel_y + 0.5, -25.0))
    print(f"external sleeve cable channel clear; minimum sleeve wall={remaining_sleeve_wall:.2f} mm")

    for path in sorted(BUILD.glob("*.stl")):
        mesh = trimesh.load_mesh(path, force="mesh")
        components = len(mesh.split(only_watertight=False))
        assert mesh.is_watertight, f"{path.name} is not watertight"
        assert components == 1, f"{path.name} has {components} components"
        print(f"{path.name}: watertight, 1 component, extents={mesh.extents.round(2).tolist()}")

    print("validation passed")


if __name__ == "__main__":
    main()
