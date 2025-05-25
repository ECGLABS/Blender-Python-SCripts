import bpy
import math

# Clear existing objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='GPENCIL')
bpy.ops.object.delete()

# Create a new Grease Pencil object
bpy.ops.object.gpencil_add(location=(0, 0, 0))
gp_obj = bpy.context.active_object
gp_data = gp_obj.data

# Create a new grease pencil layer
gp_layer = gp_data.layers.new(name="Trail", set_active=True)
gp_frame = gp_layer.frames.new(0)

# Settings
frame_count = 100
points_per_stroke = 20
amplitude = 2
frequency = 0.2
trail_length = 10

# Animate strokes across frames
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
        stroke.material_index = 0

# Create glowing material
mat = bpy.data.materials.new(name="GlowMaterial")
mat.grease_pencil.color = (1.0, 0.2, 0.6, 1.0)  # Bright pink
mat.grease_pencil.fill_color = (1.0, 0.0, 0.2, 0.0)
mat.grease_pencil.show_fill = False
gp_data.materials.append(mat)

print("✨ Bouncing sine wave grease pencil animation created!")
