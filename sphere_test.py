import cadquery as cq

# ============================================================
# PARAMETERS - Edit these to customize the model
# ============================================================
sphere_radius = 20.0  # mm

# ============================================================
# MODEL
# ============================================================
# A sphere is an intentionally simple closed solid used to verify the
# CadQuery → STL → preview pipeline. It is centered at the origin.
result = cq.Workplane("XY").sphere(sphere_radius)

# ============================================================
# EXPORT
# ============================================================
cq.exporters.export(
    result,
    "sphere_test.stl",
    tolerance=0.01,
    angularTolerance=0.1,
)
print(f"Exported sphere: radius={sphere_radius} mm, diameter={2 * sphere_radius} mm")
