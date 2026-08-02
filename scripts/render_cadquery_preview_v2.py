"""Render V2 installed, rear-detail, and print-layout previews from CadQuery."""

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

from cad import tablet_stand_v1 as v1  # noqa: E402
from cad import tablet_stand_v2 as model  # noqa: E402
from scripts.render_cadquery_preview import (  # noqa: E402
    BACKGROUND,
    cable_mesh,
    cq_mesh,
    render_view,
    rotation_x,
    translation,
)


BUILD = ROOT / "build" / "v2"
ANGLE_RAD = math.radians(v1.SCREEN_ANGLE_FROM_HORIZONTAL_DEG)


def installed_objects() -> list[tuple[trimesh.Trimesh, tuple[int, int, int, int]]]:
    cradle, bracket, sleeve, stop = model.installed_parts()
    objects = [
        (cq_mesh(cradle), (48, 72, 104, 255)),
        (cq_mesh(bracket), (48, 104, 156, 255)),
        (cq_mesh(sleeve), (42, 62, 88, 255)),
        (cq_mesh(stop), (16, 112, 220, 255)),
    ]

    tablet = trimesh.load_mesh(ROOT / "reference" / "tablet" / "tinker.obj", force="mesh")
    tablet.apply_transform(
        translation(0, 0, 0.45) @ rotation_x(ANGLE_RAD) @ translation(-7.0, 10.5, 0.0)
    )
    objects.append((tablet, (116, 124, 136, 210)))

    screen = trimesh.creation.box(extents=(184.0, 107.0, 0.22))
    screen.apply_transform(
        translation(0, 0, 0.45) @ rotation_x(ANGLE_RAD) @ translation(0, 0, 8.97)
    )
    objects.append((screen, (5, 9, 15, 255)))

    tube = trimesh.creation.cylinder(radius=16.0, height=100.0, sections=72)
    tube_top_z = v1.SLEEVE_TOP_Z - v1.SLEEVE_CAP_T
    tube.apply_translation((0.0, v1.SLEEVE_CENTER_Y, tube_top_z - 50.0))
    objects.append((tube, (118, 127, 140, 255)))

    # Schematic V2 cable route through the clips now carried by the rear bracket.
    tablet_transform = translation(0, 0, 0.45) @ rotation_x(ANGLE_RAD)
    flat_end_x = (
        v1.TABLET_X / 2.0 + v1.USB_PLUG_PROJECTION - v1.RIGHT_ANGLE_PIGTAIL_LENGTH
    )
    connector_exit = (
        tablet_transform @ np.array([flat_end_x - 12.0, 0.0, v1.REAR_CLIP_CENTER_Z, 1.0])
    )[:3]
    clip_center_z = (
        model.BRACKET_PLATE_Z0 - v1.REAR_CLIP_OUTER_Z / 2.0 + 0.05
    )
    bracket_transform = rotation_x(ANGLE_RAD)
    clip_far = (
        bracket_transform
        @ np.array(
            [
                model.BRACKET_CLIP_X[-1],
                model.BRACKET_CLIP_LOCAL_Y,
                clip_center_z,
                1.0,
            ]
        )
    )[:3]
    clip_near = (
        bracket_transform
        @ np.array(
            [
                model.BRACKET_CLIP_X[0],
                model.BRACKET_CLIP_LOCAL_Y,
                clip_center_z,
                1.0,
            ]
        )
    )[:3]
    clip_release = (
        bracket_transform
        @ np.array(
            [
                model.BRACKET_CLIP_X[0],
                model.BRACKET_CLIP_LOCAL_Y,
                clip_center_z - v1.REAR_CLIP_OUTER_Z / 2.0 - 1.0,
                1.0,
            ]
        )
    )[:3]
    sleeve_back_y = v1.SLEEVE_CENTER_Y + v1.SLEEVE_OD / 2.0
    channel_y = sleeve_back_y + v1.BRAIDED_CHANNEL_ID / 2.0 - v1.BRAIDED_CHANNEL_EMBED
    outside_x = v1.SLEEVE_OD / 2.0 + v1.BRAIDED_CABLE_D / 2.0 + 1.0
    rear_clear_y = (
        sleeve_back_y
        + v1.BRAIDED_CHANNEL_OUTER_Y
        + v1.BRAIDED_CABLE_D / 2.0
        + 1.0
    )
    transition_z = -36.0
    cable_points = [
        connector_exit,
        clip_far,
        clip_near,
        clip_release,
        np.array([outside_x, clip_release[1], transition_z]),
        np.array([outside_x, rear_clear_y, transition_z]),
        np.array([0.0, rear_clear_y, transition_z]),
        np.array([0.0, channel_y, transition_z]),
        np.array([0.0, channel_y, v1.BRAIDED_CHANNEL_BOTTOM_Z]),
    ]
    objects.append(
        (cable_mesh(cable_points, radius=v1.BRAIDED_CABLE_D / 2.0), (7, 7, 8, 255))
    )
    return objects


def print_layout_objects() -> list[tuple[trimesh.Trimesh, tuple[int, int, int, int]]]:
    cradle, bracket, sleeve, stop, key = model.print_parts()
    stop_mesh = cq_mesh(stop)
    second_key_mesh = cq_mesh(key)
    stop_mesh.apply_transform(
        trimesh.transformations.rotation_matrix(math.radians(90.0), [0.0, 0.0, 1.0])
    )
    placed = [
        (cq_mesh(cradle), (48, 72, 104, 255), (0.0, -55.0, 0.0)),
        (cq_mesh(bracket), (48, 104, 156, 255), (-80.0, 70.0, 0.0)),
        (cq_mesh(sleeve), (42, 62, 88, 255), (0.0, 70.0, 0.0)),
        (stop_mesh, (16, 112, 220, 255), (80.0, 110.0, 0.0)),
        (cq_mesh(key), (230, 128, 30, 255), (56.0, 61.0, 0.0)),
        (second_key_mesh, (230, 128, 30, 255), (64.0, 82.0, 0.0)),
    ]
    objects = []
    for mesh, color, offset in placed:
        mesh.apply_translation(offset)
        objects.append((mesh, color))
    return objects


def coupon_objects() -> list[tuple[trimesh.Trimesh, tuple[int, int, int, int]]]:
    """Direct in-memory tessellation of the right-side production-geometry crop."""
    return [(cq_mesh(model.right_fit_coupon_print()), (38, 104, 174, 255))]


def coupon_contact_sheet(paths: list[Path], output: Path) -> None:
    labels = ("TABLET ENTRY / RAILS", "USB-C OUTER END", "OPEN CABLE NOTCH")
    canvas = Image.new("RGB", (2100, 745), BACKGROUND[:3])
    draw = ImageDraw.Draw(canvas)
    for index, (path, label) in enumerate(zip(paths, labels, strict=True)):
        panel = Image.open(path).convert("RGB")
        canvas.paste(panel, (index * 700, 45))
        draw.text((index * 700 + 22, 14), label, fill=(225, 232, 240))
    canvas.save(output)


def contact_sheet(installed_path: Path, rear_path: Path, layout_path: Path, output: Path) -> None:
    installed = Image.open(installed_path).convert("RGB")
    rear = Image.open(rear_path).convert("RGB")
    layout = Image.open(layout_path).convert("RGB")
    canvas = Image.new("RGB", (1400, 2500), BACKGROUND[:3])
    canvas.paste(installed, (0, 45))
    canvas.paste(rear, (0, 1070))
    canvas.paste(layout, (0, 1800))
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 14), "V2 INSTALLED - FOUR PRINTABLE MODULES", fill=(225, 232, 240))
    draw.text((24, 1039), "REAR DETAIL - BRACKET JOINTS AND CABLE ROUTE", fill=(225, 232, 240))
    draw.text((24, 1769), "INTENDED PRINT ORIENTATIONS - BROAD DATUM FACES DOWN", fill=(225, 232, 240))
    canvas.save(output)


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    installed = BUILD / "tablet_stand_v2_preview.png"
    rear = BUILD / "tablet_stand_v2_rear_detail.png"
    layout = BUILD / "tablet_stand_v2_print_layout.png"
    coupon_views = [
        BUILD / "tablet_stand_v2_right_fit_coupon_entry.png",
        BUILD / "tablet_stand_v2_right_fit_coupon_outer.png",
        BUILD / "tablet_stand_v2_right_fit_coupon_rear.png",
    ]

    # One clean child process per camera avoids repeated pyglet capture failures
    # on macOS while keeping every mesh directly tessellated from CadQuery.
    if len(sys.argv) == 3 and sys.argv[1] == "--render-one":
        if sys.argv[2] == "installed":
            render_view(
                installed_objects(),
                installed,
                (1400, 1000),
                eye=(280.0, -340.0, 115.0),
                target=(0.0, 8.0, -5.0),
            )
        elif sys.argv[2] == "rear":
            render_view(
                installed_objects(),
                rear,
                (1400, 700),
                eye=(230.0, 240.0, 80.0),
                target=(20.0, 18.0, -2.0),
            )
        elif sys.argv[2] == "layout":
            render_view(
                print_layout_objects(),
                layout,
                (1400, 700),
                eye=(0.0, -15.0, 450.0),
                target=(10.0, 0.0, 0.0),
            )
        elif sys.argv[2] == "coupon-entry":
            render_view(
                coupon_objects(),
                coupon_views[0],
                (700, 700),
                eye=(-85.0, -180.0, 95.0),
                target=(96.0, 0.0, 4.0),
            )
        elif sys.argv[2] == "coupon-outer":
            render_view(
                coupon_objects(),
                coupon_views[1],
                (700, 700),
                eye=(260.0, -150.0, 85.0),
                target=(99.0, 0.0, 3.0),
            )
        elif sys.argv[2] == "coupon-rear":
            render_view(
                coupon_objects(),
                coupon_views[2],
                (700, 700),
                eye=(190.0, 170.0, -85.0),
                target=(101.0, 0.0, 3.0),
            )
        else:
            raise ValueError(f"unknown preview view: {sys.argv[2]}")
        return

    subprocess.run([sys.executable, str(Path(__file__).resolve()), "--render-one", "installed"], check=True)
    subprocess.run([sys.executable, str(Path(__file__).resolve()), "--render-one", "rear"], check=True)
    subprocess.run([sys.executable, str(Path(__file__).resolve()), "--render-one", "layout"], check=True)
    for view in ("coupon-entry", "coupon-outer", "coupon-rear"):
        subprocess.run([sys.executable, str(Path(__file__).resolve()), "--render-one", view], check=True)
    contact_sheet(installed, rear, layout, BUILD / "tablet_stand_v2_multiview.png")
    coupon_contact_sheet(
        coupon_views,
        BUILD / "tablet_stand_v2_right_fit_coupon_multiview.png",
    )
    print("Rendered V2 CadQuery solids directly with Trimesh (no STL import).")


if __name__ == "__main__":
    main()
