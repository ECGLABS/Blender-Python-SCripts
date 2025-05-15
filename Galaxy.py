import bpy
import math
import random

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Parameters
num_arms = 5
stars_per_arm = 100
arm_spread = 0.5
galaxy_radius = 10
z_variation = 0.3
frame_count = 250

# Emission material generator
def create_emission_material(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    mat.node_tree.nodes.remove(bsdf)
    emission = mat.node_tree.nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = color
    emission.inputs['Strength'].default_value = strength
    output = mat.node_tree.nodes.get("Material Output")
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    return mat

# Create stars
for arm in range(num_arms):
    for i in range(stars_per_arm):
        ratio = i / stars_per_arm
        angle = ratio * 6.28 * 3 + (arm * 2 * math.pi / num_arms)
        distance = ratio * galaxy_radius
        offset = random.uniform(-arm_spread, arm_spread)
        x = math.cos(angle + offset) * distance
        y = math.sin(angle + offset) * distance
        z = random.uniform(-z_variation, z_variation)

        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(x, y, z))
        star = bpy.context.active_object
        star.name = f"Star_{arm}_{i}"

        # Random star color
        star_color = (random.uniform(0.8, 1.0), random.uniform(0.7, 1.0), random.uniform(0.4, 1.0), 1)
        star.data.materials.append(create_emission_material(f"StarMat_{arm}_{i}", star_color, 5))

        # Animate star orbit
        star.rotation_mode = 'XYZ'
        star.keyframe_insert(data_path="rotation_euler", frame=1)
        star.rotation_euler[2] = 6.28
        star.keyframe_insert(data_path="rotation_euler", frame=frame_count)

        fcurve = star.animation_data.action.fcurves.find('rotation_euler', index=2)
        if fcurve:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'

# Core glow
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=(0, 0, 0))
core = bpy.context.active_object
core.name = "GalacticCore"
core.data.materials.append(create_emission_material("CoreMat", (1.0, 0.8, 0.5, 1), 100))

# Camera
bpy.ops.object.camera_add(location=(0, -18, 8), rotation=(math.radians(75), 0, 0))
bpy.context.scene.camera = bpy.context.active_object

# Light
bpy.ops.object.light_add(type='AREA', location=(0, 0, 15))
light = bpy.context.active_object
light.data.energy = 3000
light.data.shape = 'DISK'
light.data.size = 5

# Set render settings
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = frame_count
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
