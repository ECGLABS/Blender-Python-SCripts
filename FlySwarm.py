import bpy
import random
import math

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a simple lowpoly character (capsule-like)
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 1))
bpy.ops.transform.resize(value=(0.5, 0.5, 1.2))
character = bpy.context.object
character.name = "LowpolyCharacter"

# Create a single fly object (a small icosphere)
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.05, location=(0, 0, 1.5))
fly_template = bpy.context.object
fly_template.name = "FlyTemplate"

# Create a swarm of flies
num_flies = 50
swarm = []

for i in range(num_flies):
    fly = fly_template.copy()
    fly.data = fly_template.data.copy()
    fly.location = (
        random.uniform(-1, 1),
        random.uniform(-1, 1),
        random.uniform(1.2, 2)
    )
    bpy.context.collection.objects.link(fly)
    swarm.append(fly)

# Delete the original template
bpy.data.objects.remove(fly_template, do_unlink=True)

# Animate swarm movement
frames = 100
for frame in range(frames):
    bpy.context.scene.frame_set(frame)
    for i, fly in enumerate(swarm):
        angle = math.radians(frame * 10 + i * 30)
        radius = 0.5 + 0.2 * math.sin(frame * 0.1 + i)
        fly.location.x = math.cos(angle) * radius
        fly.location.y = math.sin(angle) * radius
        fly.location.z = 1.5 + 0.2 * math.sin(frame * 0.2 + i)
        fly.keyframe_insert(data_path="location")

# Set frame range and play
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = frames
