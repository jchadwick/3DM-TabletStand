"""Optional polished presentation preview of the v1 stand using Blender.

Routine previews use render_cadquery_preview.py and direct in-memory CadQuery
tessellation. This script intentionally uses the generated STL only when a
Blender-specific presentation scene is desired.

Run with:
    blender --background --python scripts/render_preview.py
"""

from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "v1"
TILT = math.radians(80.0)
SLEEVE_CENTER_Y = 24.0


def material(name: str, color: tuple[float, float, float, float], metallic: float = 0.0, roughness: float = 0.45):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def import_stl(path: Path, name: str, mat):
    bpy.ops.wm.stl_import(filepath=str(path))
    obj = bpy.context.selected_objects[0]
    obj.name = name
    obj.data.materials.append(mat)
    for poly in obj.data.polygons:
        poly.use_smooth = False
    return obj


def look_at(obj, target: tuple[float, float, float]):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def main():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    holder_mat = material("Charcoal PETG", (0.16, 0.20, 0.25, 1.0), roughness=0.33)
    stop_mat = material("End stop", (0.07, 0.34, 0.68, 1.0), roughness=0.30)
    tablet_mat = material("Tablet body", (0.42, 0.45, 0.49, 1.0), metallic=0.25, roughness=0.28)
    screen_mat = material("Screen", (0.008, 0.014, 0.022, 1.0), metallic=0.05, roughness=0.12)
    tube_mat = material("Support tube", (0.40, 0.43, 0.46, 1.0), metallic=0.65, roughness=0.27)
    cable_mat = material("USB-C cable", (0.025, 0.025, 0.028, 1.0), roughness=0.50)

    import_stl(BUILD / "tablet_stand_main.stl", "Main holder", holder_mat)
    import_stl(BUILD / "tablet_stand_end_stop_installed.stl", "M3 end stop", stop_mat)

    # Use the supplied tablet mesh, centered in the documented 200 x 123 mm envelope.
    bpy.ops.wm.obj_import(filepath=str(ROOT / "reference" / "tablet" / "tinker.obj"))
    tablet = bpy.context.selected_objects[0]
    tablet.name = "Supplied tablet reference"
    tablet.data.materials.clear()
    tablet.data.materials.append(tablet_mat)
    tablet.matrix_world = (
        Matrix.Translation((0.0, 0.0, 0.45))
        @ Matrix.Rotation(TILT, 4, "X")
        @ Matrix.Translation((-7.0, 10.5, 0.0))
    )

    # A dark inset communicates screen orientation without altering the source OBJ.
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    screen = bpy.context.object
    screen.name = "Screen indication"
    screen.dimensions = (184.0, 107.0, 0.22)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    local_center = Vector((0.0, 0.0, 8.97))
    screen.location = Matrix.Rotation(TILT, 4, "X") @ local_center + Vector((0.0, 0.0, 0.45))
    screen.rotation_euler[0] = TILT
    screen.data.materials.append(screen_mat)

    # Existing 32 mm OD pedestal tube, shown extending into the sleeve.
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=96, radius=16.0, depth=95.0, location=(0, SLEEVE_CENTER_Y, -50.5)
    )
    tube = bpy.context.object
    tube.name = "Existing 32 mm tube"
    tube.data.materials.append(tube_mat)

    # Represent the slim cable leaving the open center of the right edge and curving down.
    curve_data = bpy.data.curves.new("USB-C cable path", type="CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = 1.7
    curve_data.bevel_resolution = 5
    spline = curve_data.splines.new("BEZIER")
    spline.bezier_points.add(3)
    local_exit = Matrix.Rotation(TILT, 4, "X") @ Vector((106.0, 0.0, 4.2)) + Vector((0, 0, 0.45))
    points = [
        local_exit,
        local_exit + Vector((12.0, 0.0, 0.0)),
        local_exit + Vector((23.0, 7.0, -7.0)),
        local_exit + Vector((18.0, 19.0, -25.0)),
    ]
    for bp, co in zip(spline.bezier_points, points):
        bp.co = co
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    cable = bpy.data.objects.new("USB-C routing indication", curve_data)
    bpy.context.collection.objects.link(cable)
    cable.data.materials.append(cable_mat)

    # Ground plane and studio lighting.
    bpy.ops.mesh.primitive_plane_add(size=700, location=(0, 0, -124.0))
    floor = bpy.context.object
    floor.data.materials.append(material("Floor", (0.10, 0.12, 0.15, 1.0), roughness=0.75))

    bpy.ops.object.light_add(type="AREA", location=(-170, -190, 270))
    # The CAD is modeled in millimeters while Blender treats scene units as
    # meters, so studio lights need intentionally high power at this scale.
    bpy.context.object.data.energy = 180000
    bpy.context.object.data.shape = "DISK"
    bpy.context.object.data.size = 150
    look_at(bpy.context.object, (0, 0, -10))

    bpy.ops.object.light_add(type="AREA", location=(210, 40, 180))
    bpy.context.object.data.energy = 130000
    bpy.context.object.data.size = 120
    look_at(bpy.context.object, (0, 0, -10))

    bpy.ops.object.light_add(type="AREA", location=(-60, 190, 100))
    bpy.context.object.data.energy = 90000
    bpy.context.object.data.size = 100
    look_at(bpy.context.object, (0, 20, 0))

    bpy.ops.object.camera_add(location=(285, -330, 245))
    camera = bpy.context.object
    look_at(camera, (0, 0, -24))
    camera.data.lens = 56
    bpy.context.scene.camera = camera

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(BUILD / "tablet_stand_v1_preview.png")
    scene.render.film_transparent = False
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.035, 0.045, 0.065, 1.0)
    background.inputs["Strength"].default_value = 0.55
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = 1.0
    bpy.ops.wm.save_as_mainfile(filepath=str(BUILD / "tablet_stand_v1_preview.blend"))
    bpy.ops.render.render(write_still=True)

    # Edge-on view makes the accepted 10-degree-back-from-vertical angle clear.
    camera.location = (335.0, -15.0, 88.0)
    look_at(camera, (0.0, 0.0, -13.0))
    camera.data.lens = 62
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 700
    scene.render.filepath = str(BUILD / "tablet_stand_v1_side.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
