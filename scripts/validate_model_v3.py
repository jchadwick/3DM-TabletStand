"""Validate the V3 split cradle, splice keys, print layouts, and exports."""

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
    "tablet_stand_v3_alignment_key_print_2.stl",
    "tablet_stand_v3_cradle_splice_key_print_3.stl",
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
    assert metadata["revision"] == "v3 split-cradle concept"
    assert metadata["cradle_split"]["total_clearance"] == model.CRADLE_SEAM_CLEARANCE
    assert metadata["cradle_split"]["rear_bracket_bridges_center_seam"] is True
    assert metadata["separate_left_cap"] is False
    assert metadata["splice_key"]["quantity"] == 3
    assert metadata["splice_key"]["length_clearance_total"] >= 1.0
    assert metadata["splice_key"]["width_clearance_total"] >= 1.0
    assert metadata["splice_key"]["depth_clearance"] >= 0.2

    source = model.split_cradle_source()
    left, right = model.cradle_halves()
    left_shape = left.val()
    right_shape = right.val()
    left_bb = left_shape.BoundingBox()
    right_bb = right_shape.BoundingBox()
    assert len(left.solids().vals()) == 1
    assert len(right.solids().vals()) == 1
    assert left.intersect(right).val().Volume() < 1e-6
    assert max(left_bb.xlen, right_bb.xlen) < 120.0
    assert max(left_bb.ylen, right_bb.ylen) < 140.0
    assert max(left_bb.xlen, left_bb.ylen, right_bb.xlen, right_bb.ylen) < 220.0
    assert abs(left_bb.zmin + core.BASE_T) < 1e-6
    assert abs(right_bb.zmin + core.BASE_T) < 1e-6
    assert left_shape.Volume() + right_shape.Volume() < source.val().Volume()
    print(
        "split cradle is interference-free and bed-friendly; "
        f"left={left_bb.xlen:.2f} x {left_bb.ylen:.2f} x {left_bb.zlen:.2f} mm, "
        f"right={right_bb.xlen:.2f} x {right_bb.ylen:.2f} x {right_bb.zlen:.2f} mm"
    )

    # The center dogleg and the outer seam legs are separated by the specified
    # glue clearance; the shoulders provide plan-view Y indexing.
    half_gap = model.CRADLE_SEAM_CLEARANCE / 2.0
    assert_open(
        left_shape,
        (model.CRADLE_SEAM_CENTER_X, 5.0, -1.5),
        "left center seam did not preserve clearance",
    )
    assert_open(
        right_shape,
        (model.CRADLE_SEAM_OUTER_X, 56.0, -1.5),
        "right outer seam did not preserve clearance",
    )
    assert_solid(
        left_shape,
        (model.CRADLE_SEAM_CENTER_X - half_gap - 0.3, 5.0, -1.5),
        "left center tongue missing",
    )
    assert_solid(
        right_shape,
        (model.CRADLE_SEAM_OUTER_X + half_gap + 0.3, 56.0, -1.5),
        "right outer tongue missing",
    )
    print(
        f"stepped seam has {model.CRADLE_SEAM_CLEARANCE:.2f} mm total glue clearance "
        f"and a {model.CRADLE_SEAM_CENTER_X - model.CRADLE_SEAM_OUTER_X:.1f} mm dogleg"
    )

    # All three loose keys fit inside their rear recesses without touching the
    # cradle, remain recessed below the bracket bond plane, and bridge no more
    # than the validated support-free groove width during printing.
    assert model.CRADLE_SPLICE_GROOVE_WIDTH <= 10.0
    assert model.CRADLE_SPLICE_KEY_QUANTITY == len(model.cradle_splice_keys_installed())
    for index, key in enumerate(model.cradle_splice_keys_installed(), start=1):
        assert key.intersect(left).val().Volume() < 1e-6
        assert key.intersect(right).val().Volume() < 1e-6
        key_bb = key.val().BoundingBox()
        assert key_bb.zmin > -core.BASE_T
        assert key_bb.zmax < -core.BASE_T + model.CRADLE_SPLICE_GROOVE_DEPTH
        print(
            f"splice key {index}: recessed {model.CRADLE_SPLICE_KEY_RECESS:.2f} mm, "
            "clear of both cradle wings"
        )

    # V3 deliberately retains the user-tested button and USB-C geometry while
    # replacing the separate cap with a continuous integral left closure.
    assert_open(left_shape, (-80.0, 62.5, core.TABLET_Z / 2.0), "button channel obstructed")
    assert_solid(left_shape, (-80.0, 64.0, core.TABLET_Z / 2.0), "button outer wall missing")
    assert_open(right_shape, (104.0, 0.0, 4.0), "USB-C pocket obstructed")
    assert_open(
        right_shape,
        (core.TABLET_X / 2.0 + core.USB_PLUG_PROJECTION, 0.0, -1.5),
        "USB-C rear rectangle obstructed",
    )
    left_wall_x = -(
        core.TABLET_X + core.FIT_X + 2.0 * core.WALL_T
    ) / 2.0 - v2.ENDSTOP_OUTER_WALL_X / 2.0
    for y_pos in (-60.0, 0.0, 60.0):
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
    assert_open(left_shape, (-98.0, 0.0, 4.0), "integral left closure blocks tablet cavity")
    assert abs(left_bb.ylen - core.HOLDER_OUTER_Y) < 1e-5
    print("tested button and USB-C interfaces are preserved; left wing is fully enclosed")

    # The bracket spans the center seam and sees solid bond land on each wing.
    assert_solid(left_shape, (-20.0, v2.BRACKET_PLATE_CENTER_Y, -2.5), "left bond land missing")
    assert_solid(right_shape, (20.0, v2.BRACKET_PLATE_CENTER_Y, -2.5), "right bond land missing")
    bracket_xmin = -v2.BRACKET_PLATE_X / 2.0
    bracket_xmax = v2.BRACKET_PLATE_X / 2.0
    assert bracket_xmin < model.CRADLE_SEAM_CENTER_X < bracket_xmax
    print("74 x 36 mm rear bracket spans the center seam and bonds to both wings")

    for part in model.print_parts():
        assert abs(part.val().BoundingBox().zmin) < 1e-6

    for path in sorted(BUILD.glob("*.stl")):
        mesh = trimesh.load_mesh(path, force="mesh")
        components = len(mesh.split(only_watertight=False))
        assert mesh.is_watertight, f"{path.name} is not watertight"
        assert components == 1, f"{path.name} has {components} components"
        print(
            f"{path.name}: watertight, extents={mesh.extents.round(2).tolist()}, "
            f"approx_overhang_area={approximate_support_area(mesh):.0f} mm2"
        )

    print("V3 split-cradle validation passed")


if __name__ == "__main__":
    main()
