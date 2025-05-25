import bpy
import math

# Delete existing Grease Pencil objects
for obj in bpy.data.objects:
    if obj.type == 'GPENCIL':
        bpy.data.objects.remove(obj, do_unlink=True)

# Create a new Grease Pencil object
bpy.ops.object.gpencil_add(location=(0, 0, 0))
gp_obj = bpy.context.active_object
gp_data = gp_obj.data

# Create a new Grease Pencil material
material = bpy.data.materials.new(name="TrailMaterial")
material.use_nodes = False
material.diffuse_color = (1.0, 0.2, 0.6, 1.0)  # Bright pink with alpha
material.grease_pencil.show_fill = False  # Optional: hide fill

# Append the material to the GP object
gp_data.materials.append(material)

# Create a new layer
gp_layer = gp_data.layers.new(name="Trail", set_active=True)

# Settings
frame_count = 100
points_per_stroke = 20
amplitude = 2
frequency = 0.2

# Draw animation over frames
for frame_num in range(frame_count):
    gp_frame = gp_layer.frames.new(frame_num)
    for i in range(points_per_stroke):
        x = (i + frame_num * 0.5) * 0.2
        y = amplitude * math.sin(frequency * x + frame_num * 0.2)

        stroke = gp_frame.strokes.new()
        stroke.display_mode = '3DSPACE'
        stroke.points.add(count=1)
        stroke.points[0].co = (x, y, 0)
        stroke.line_width = int(30 * (1 - i / points_per_stroke))
        stroke.material_index = 0  # Use the first material

print("✅ Done! Grease Pencil trail animation successfully created.")
