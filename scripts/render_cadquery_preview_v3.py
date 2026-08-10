"""Render V3 installed, split-joint, and print-layout previews from CadQuery."""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
import trimesh


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cad import tablet_stand_core as core  # noqa: E402
from cad import tablet_stand_v3 as model  # noqa: E402
from scripts.render_cadquery_helpers import (  # noqa: E402
    BACKGROUND,
    cq_mesh,
    render_view,
    rotation_x,
    translation,
)


BUILD = ROOT / "build" / "v3"
ANGLE_RAD = math.radians(core.SCREEN_ANGLE_FROM_HORIZONTAL_DEG)
LEFT_COLOR = (38, 88, 138, 255)
RIGHT_COLOR = (42, 126, 186, 255)
KEY_COLOR = (232, 132, 28, 255)


def installed_objects() -> list[tuple[trimesh.Trimesh, tuple[int, int, int, int]]]:
    left, right, bracket, sleeve = model.installed_parts()
    objects = [
        (cq_mesh(left), LEFT_COLOR),
        (cq_mesh(right), RIGHT_COLOR),
        (cq_mesh(bracket), (48, 104, 156, 255)),
        (cq_mesh(sleeve), (42, 62, 88, 255)),
    ]
    objects.append((cq_mesh(model.installed_locking_wedge()), KEY_COLOR))

    tablet = trimesh.load_mesh(ROOT / "reference" / "tablet" / "tinker.obj", force="mesh")
    tablet.apply_transform(
        translation(0, 0, 0.45) @ rotation_x(ANGLE_RAD) @ translation(-7.0, 10.5, 0.0)
    )
    objects.append((tablet, (116, 124, 136, 190)))

    screen = trimesh.creation.box(extents=(184.0, 107.0, 0.22))
    screen.apply_transform(
        translation(0, 0, 0.45) @ rotation_x(ANGLE_RAD) @ translation(0, 0, 8.97)
    )
    objects.append((screen, (5, 9, 15, 255)))

    tube = trimesh.creation.cylinder(radius=16.0, height=100.0, sections=72)
    tube_top_z = core.SLEEVE_TOP_Z - core.SLEEVE_CAP_T
    tube.apply_translation((0.0, core.SLEEVE_CENTER_Y, tube_top_z - 50.0))
    objects.append((tube, (118, 127, 140, 255)))
    return objects


def rear_joint_objects() -> list[tuple[trimesh.Trimesh, tuple[int, int, int, int]]]:
    left, right = model.cradle_halves()
    left_mesh = cq_mesh(left)
    left_mesh.apply_translation((-24.0, 0.0, 0.0))
    wedge_mesh = cq_mesh(model.locking_wedge_installed())
    wedge_mesh.apply_translation((0.0, -10.0, 0.0))
    return [
        (left_mesh, LEFT_COLOR),
        (cq_mesh(right), RIGHT_COLOR),
        (wedge_mesh, KEY_COLOR),
    ]


def print_layout_objects() -> list[tuple[trimesh.Trimesh, tuple[int, int, int, int]]]:
    left, right, _, _, _, wedge = model.print_parts()
    placed: list[tuple[trimesh.Trimesh, tuple[int, int, int, int], tuple[float, float, float]]] = [
        (cq_mesh(left), LEFT_COLOR, (-68.0, 0.0, 0.0)),
        (cq_mesh(right), RIGHT_COLOR, (68.0, 0.0, 0.0)),
        (cq_mesh(wedge), KEY_COLOR, (0.0, 0.0, 0.0)),
    ]
    objects = []
    for mesh, color, offset in placed:
        mesh.apply_translation(offset)
        objects.append((mesh, color))
    return objects


def coupon_plate_objects() -> list[tuple[trimesh.Trimesh, tuple[int, int, int, int]]]:
    colors = (LEFT_COLOR, RIGHT_COLOR, KEY_COLOR)
    return [
        (cq_mesh(part), color)
        for part, color in zip(model.lock_coupon_print_plate_parts(), colors)
    ]


def contact_sheet(installed: Path, left_edge: Path, joint: Path, layout: Path, output: Path) -> None:
    installed_image = Image.open(installed).convert("RGB")
    left_edge_image = Image.open(left_edge).convert("RGB")
    joint_image = Image.open(joint).convert("RGB")
    layout_image = Image.open(layout).convert("RGB")
    canvas = Image.new("RGB", (1400, 3230), BACKGROUND[:3])
    canvas.paste(installed_image, (0, 45))
    canvas.paste(left_edge_image, (0, 1070))
    canvas.paste(joint_image, (0, 1800))
    canvas.paste(layout_image, (0, 2530))
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 14), "V3 INSTALLED — TWO-PIECE CRADLE", fill=(225, 232, 240))
    draw.text((24, 1039), "INTEGRAL LEFT WING — CONTINUOUS ENCLOSED EDGE", fill=(225, 232, 240))
    draw.text((24, 1769), "REMOVABLE JOINT — THREE TONGUES + LOWER CROSS-WEDGE", fill=(225, 232, 240))
    draw.text((24, 2499), "PRINT LAYOUT — TWO WINGS + ONE LOCKING WEDGE", fill=(225, 232, 240))
    canvas.save(output)


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    installed = BUILD / "tablet_stand_v3_preview.png"
    left_edge = BUILD / "tablet_stand_v3_left_edge.png"
    joint = BUILD / "tablet_stand_v3_rear_joint.png"
    layout = BUILD / "tablet_stand_v3_print_layout.png"
    coupon_plate = BUILD / "tablet_stand_v3_lock_coupon_plate.png"

    if len(sys.argv) == 3 and sys.argv[1] == "--render-one":
        if sys.argv[2] == "installed":
            render_view(
                installed_objects(),
                installed,
                (1400, 1000),
                eye=(280.0, -340.0, 115.0),
                target=(0.0, 8.0, -5.0),
            )
        elif sys.argv[2] == "left-edge":
            render_view(
                installed_objects(),
                left_edge,
                (1400, 700),
                eye=(-330.0, -190.0, 80.0),
                target=(-98.0, 0.0, 2.0),
            )
        elif sys.argv[2] == "joint":
            render_view(
                rear_joint_objects(),
                joint,
                (1400, 700),
                eye=(170.0, -230.0, -175.0),
                target=(0.0, -18.0, -0.5),
            )
        elif sys.argv[2] == "layout":
            render_view(
                print_layout_objects(),
                layout,
                (1400, 700),
                eye=(0.0, -5.0, 430.0),
                target=(0.0, 0.0, 0.0),
            )
        elif sys.argv[2] == "coupon":
            render_view(
                coupon_plate_objects(),
                coupon_plate,
                (1400, 700),
                eye=(65.0, -95.0, 105.0),
                target=(0.0, 5.0, 1.5),
            )
        else:
            raise ValueError(f"unknown V3 preview view: {sys.argv[2]}")
        return

    processes = [
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--render-one", view]
        )
        for view in ("installed", "left-edge", "joint", "layout", "coupon")
    ]
    for process in processes:
        if process.wait() != 0:
            raise subprocess.CalledProcessError(process.returncode, process.args)
    contact_sheet(installed, left_edge, joint, layout, BUILD / "tablet_stand_v3_multiview.png")
    print("Rendered V3 CadQuery solids directly with a depth-buffered renderer (no STL import).")


if __name__ == "__main__":
    main()
