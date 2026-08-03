"""Shared direct CadQuery-to-Trimesh preview helpers for the active V2 model.

CadQuery/OpenCASCADE remains the source of truth. Each solid is tessellated in
memory and passed directly to Trimesh's depth-buffered viewer. STL and STEP
exports remain separate manufacturing deliverables, not preview inputs.
"""

from __future__ import annotations

import math
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image
import pyglet
import trimesh


# pyglet 1.5 on macOS otherwise exits the Python process while closing the
# temporary image-capture window used by Trimesh.
pyglet.app.event_loop.exit = lambda: None

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
