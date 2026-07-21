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
    tube_axis = cq.Vector(0, model.SLEEVE_CENTER_Y, 0.0)
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

    for path in sorted(BUILD.glob("*.stl")):
        mesh = trimesh.load_mesh(path, force="mesh")
        components = len(mesh.split(only_watertight=False))
        assert mesh.is_watertight, f"{path.name} is not watertight"
        assert components == 1, f"{path.name} has {components} components"
        print(f"{path.name}: watertight, 1 component, extents={mesh.extents.round(2).tolist()}")

    print("validation passed")


if __name__ == "__main__":
    main()
