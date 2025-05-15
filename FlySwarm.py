import bpy
import random
import math

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a simple lowpoly character
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 1))
bpy.ops.transform.resize(value=(0.5, 0.5, 1.2))
character = bpy.context.object
character.name = "LowpolyCharacter"

# Create a base fly (icosphere)
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.05, location=(0, 0, 1.5))
fly_template = bpy.context.object
fly_template.name = "FlyTemplate"

# Create swarm with unique animation parameters
num_flies = 50
frames = 150
swarm = []

for i in range(num_flies):
    fly = fly_template.copy()
    fly.data = fly_template.data.copy()
    fly.name = f"Fly_{i}"
    bpy.context.collection.objects.link(fly)

    # Store animation parameters as custom properties
    fly["amp_x"] = random.uniform(0.2, 0.5)
    fly["amp_y"] = random.uniform(0.2, 0.5)
    fly["amp_z"] = random.uniform(0.1, 0.3)
    fly["freq"] = random.uniform(0.05, 0.15)
    fly["phase"] = random.uniform(0, 2 * math.pi)
    fly["offset_x"] = random.uniform(-0.5, 0.5)
    fly["offset_y"] = random.uniform(-0.5, 0.5)
    swarm.append(fly)

# Delete the template
bpy.data.objects.remove(fly_template, do_unlink=True)

# Animate chaotic swarming
for frame in range(frames):
    bpy.context.scene.frame_set(frame)
    for fly in swarm:
        freq = fly["freq"]
        phase = fly["phase"]
        amp_x = fly["amp_x"]
        amp_y = fly["amp_y"]
        amp_z = fly["amp_z"]
        offset_x = fly["offset_x"]
        offset_y = fly["offset_y"]

        t = frame
        fly.location.x = offset_x + math.sin(freq * t + phase) * amp_x
        fly.location.y = offset_y + math.cos(freq * t + phase) * amp_y
        fly.location.z = 1.5 + math.sin(freq * t * 1.5 + phase) * amp_z
        fly.keyframe_insert(data_path="location")

# Set scene frame range
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = frames
