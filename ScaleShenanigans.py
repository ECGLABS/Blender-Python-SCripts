import bpy
import math
import random

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Settings
shapes = ['cube', 'sphere', 'cone', 'cylinder', 'torus']
spacing = 2.2

# Create objects and animate them
for i, shape in enumerate(shapes):
    z = i * spacing
    loc = (0, 0, z)

    if shape == 'cube':
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    elif shape == 'sphere':
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=loc)
    elif shape == 'cone':
        bpy.ops.mesh.primitive_cone_add(radius1=0.6, depth=1.2, location=loc)
    elif shape == 'cylinder':
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1.5, location=loc)
    elif shape == 'torus':
        bpy.ops.mesh.primitive_torus_add(location=loc)

    obj = bpy.context.active_object
    obj.name = f"{shape.capitalize()}_{i}"

    # Random color
    mat = bpy.data.materials.new(name=f"Mat_{shape}_{i}")
    mat.diffuse_color = (random.random(), random.random(), random.random(), 1)
    mat.use_nodes = False
    obj.data.materials.append(mat)

    # Animate scaling like breathing
    for f in range(0, 200, 10):
        scale = 1 + 0.2 * math.sin((f + i * 10) * 0.1)
        obj.scale = (scale, scale, scale)
        obj.keyframe_insert(data_path="scale", frame=f)

# Add a light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 15))

# Add a camera
bpy.ops.object.camera_add(location=(8, -8, 8), rotation=(math.radians(60), 0, math.radians(45)))
bpy.context.scene.camera = bpy.context.active_object

# Frame range
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 200
