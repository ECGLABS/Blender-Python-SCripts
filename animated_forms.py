import bpy
import math
import random

# Delete all existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Object creation functions
def create_object(type, name, location):
    if type == "cube":
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    elif type == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=location)
    elif type == "cone":
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, depth=1, location=location)
    elif type == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=1, location=location)
    elif type == "torus":
        bpy.ops.mesh.primitive_torus_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

# Apply random color
def assign_material(obj, color):
    mat = bpy.data.materials.new(name="Material_" + obj.name)
    mat.diffuse_color = color
    mat.use_nodes = False
    obj.data.materials.append(mat)

# Animate rotation and bobbing
def animate_object(obj, frame_offset):
    for f in range(0, 250, 10):
        obj.location.z = 0.5 + 0.2 * math.sin((f + frame_offset) * 0.1)
        obj.keyframe_insert(data_path="location", frame=f)
        obj.rotation_euler[2] = math.radians((f + frame_offset) * 3)
        obj.keyframe_insert(data_path="rotation_euler", frame=f)

shapes = ["cube", "sphere", "cone", "cylinder", "torus"]
radius = 3
for i, shape in enumerate(shapes):
    angle = math.radians(i * (360 / len(shapes)))
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    obj = create_object(shape, shape.capitalize(), (x, y, 0.5))
    color = (random.random(), random.random(), random.random(), 1)
    assign_material(obj, color)
    animate_object(obj, i * 5)

# Set timeline and frame range
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 240
