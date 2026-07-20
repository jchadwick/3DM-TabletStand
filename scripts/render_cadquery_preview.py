"""Render v1 directly from CadQuery solids without an intermediate STL.

CadQuery/OpenCASCADE remains the source of truth. Each solid is tessellated in
memory and passed directly to Trimesh's depth-buffered viewer. STL and STEP
exports remain separate manufacturing deliverables, not preview inputs.
"""

from __future__ import annotations

import math
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
import pyglet
import trimesh


# pyglet 1.5 on macOS otherwise exits the Python process while closing the
# temporary image-capture window used by Trimesh.
pyglet.app.event_loop.exit = lambda: None

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cad import tablet_stand_v1 as model  # noqa: E402


BUILD = ROOT / "build" / "v1"
ANGLE_RAD = math.radians(model.SCREEN_ANGLE_FROM_HORIZONTAL_DEG)
BACKGROUND = (9, 12, 18, 255)


def cq_mesh(workplane) -> trimesh.Trimesh:
    """Tessellate one CadQuery solid directly into an in-memory Trimesh."""
    vertices, triangles = workplane.val().tessellate(0.08, 0.15)
    vertex_array = np.array([[v.x, v.y, v.z] for v in vertices], dtype=float)
    face_array = np.array(triangles, dtype=np.int64)
    return trimesh.Trimesh(vertices=vertex_array, faces=face_array, process=False)


def translation(x: float, y: float, z: float) -> np.ndarray:
    matrix = np.eye(4)
    matrix[:3, 3] = (x, y, z)
    return matrix


def rotation_x(angle: float) -> np.ndarray:
    c, s = math.cos(angle), math.sin(angle)
    return np.array(
        [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]],
        dtype=float,
    )


def cable_mesh(points: list[np.ndarray], radius: float = 1.7) -> trimesh.Trimesh:
    pieces = []
    for start, end in zip(points, points[1:]):
        vector = end - start
        length = float(np.linalg.norm(vector))
        cylinder = trimesh.creation.cylinder(radius=radius, height=length, sections=20)
        align = trimesh.geometry.align_vectors([0, 0, 1], vector / length)
        align[:3, 3] = (start + end) / 2.0
        cylinder.apply_transform(align)
        pieces.append(cylinder)
    return trimesh.util.concatenate(pieces)


def build_objects() -> list[tuple[trimesh.Trimesh, tuple[int, int, int, int]]]:
    main_holder, end_stop = model.installed_parts()
    objects = [
        (cq_mesh(main_holder), (48, 72, 104, 255)),
        (cq_mesh(end_stop), (16, 112, 220, 255)),
    ]

    # Supplied tablet reference, centered from its documented OBJ bounds.
    tablet = trimesh.load_mesh(ROOT / "reference" / "tablet" / "tinker.obj", force="mesh")
    tablet.apply_transform(
        translation(0, 0, 0.45) @ rotation_x(ANGLE_RAD) @ translation(-7.0, 10.5, 0.0)
    )
    objects.append((tablet, (116, 124, 136, 255)))

    # Dark inset indicating the screen without modifying the supplied OBJ.
    screen = trimesh.creation.box(extents=(184.0, 107.0, 0.22))
    screen.apply_transform(
        translation(0, 0, 0.45) @ rotation_x(ANGLE_RAD) @ translation(0, 0, 8.97)
    )
    objects.append((screen, (5, 9, 15, 255)))

    # Existing 32 mm tube, aligned to the rear-offset sleeve and seating cap.
    tube = trimesh.creation.cylinder(radius=16.0, height=100.0, sections=72)
    tube.apply_translation((0.0, model.SLEEVE_CENTER_Y, -49.0))
    objects.append((tube, (118, 127, 140, 255)))

    # Schematic cable path exiting the right-edge midpoint and bending behind.
    local_exit = np.array([106.0, 0.0, model.TABLET_Z / 2.0, 1.0])
    exit_point = (translation(0, 0, 0.45) @ rotation_x(ANGLE_RAD) @ local_exit)[:3]
    cable_points = [
        exit_point,
        exit_point + np.array([12.0, 0.0, 0.0]),
        exit_point + np.array([23.0, 7.0, -7.0]),
        exit_point + np.array([18.0, 19.0, -25.0]),
    ]
    objects.append((cable_mesh(cable_points), (7, 7, 8, 255)))
    return objects


def camera_pose(eye, target, up=(0.0, 0.0, 1.0)) -> np.ndarray:
    """Build a Trimesh camera pose whose -Z axis points at target."""
    eye = np.asarray(eye, dtype=float)
    target = np.asarray(target, dtype=float)
    up = np.asarray(up, dtype=float)
    z_axis = eye - target
    z_axis /= np.linalg.norm(z_axis)
    x_axis = np.cross(up, z_axis)
    x_axis /= np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)
    pose = np.eye(4)
    pose[:3, 0] = x_axis
    pose[:3, 1] = y_axis
    pose[:3, 2] = z_axis
    pose[:3, 3] = eye
    return pose


def render_view(objects, output: Path, size: tuple[int, int], eye, target):
    """Render all in-memory tessellations with a real depth buffer."""
    scene = trimesh.Scene()
    for index, (mesh, rgba) in enumerate(objects):
        rendered = mesh.copy()
        rendered.visual.face_colors = np.tile(np.asarray(rgba, dtype=np.uint8), (len(mesh.faces), 1))
        scene.add_geometry(rendered, geom_name=f"part_{index}", node_name=f"part_{index}")

    scene.camera.resolution = size
    scene.camera.fov = (45.0, 40.0)
    scene.camera_transform = camera_pose(eye, target)
    png = scene.save_image(
        resolution=size,
        visible=True,
        background=BACKGROUND,
        smooth=False,
        flags={"axis": False, "grid": False},
    )

    # Retina displays return a 2x capture; normalize the committed artifact.
    image = Image.open(BytesIO(png)).convert("RGB")
    if image.size != size:
        image = image.resize(size, Image.Resampling.LANCZOS)
    image.save(output)


def contact_sheet(hero_path: Path, side_path: Path, output: Path):
    hero = Image.open(hero_path).convert("RGB")
    side = Image.open(side_path).convert("RGB")
    canvas = Image.new("RGB", (1400, 1740), BACKGROUND[:3])
    canvas.paste(hero, (0, 45))
    canvas.paste(side, (0, 1040))
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 14), "V1 KIOSK ORIENTATION - THREE-QUARTER", fill=(225, 232, 240))
    draw.text((24, 1009), "SIDE VIEW - 10 DEG BACK FROM VERTICAL", fill=(225, 232, 240))
    canvas.save(output)


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    objects = build_objects()
    hero = BUILD / "tablet_stand_v1_preview.png"
    side = BUILD / "tablet_stand_v1_side.png"
    render_view(objects, hero, (1400, 1000), eye=(280.0, -340.0, 115.0), target=(0.0, 8.0, -5.0))
    render_view(objects, side, (1400, 700), eye=(330.0, 15.0, 30.0), target=(0.0, 15.0, -8.0))
    contact_sheet(hero, side, BUILD / "tablet_stand_v1_multiview.png")
    print("Rendered CadQuery solids directly with Trimesh (no STL import).")


if __name__ == "__main__":
    main()

