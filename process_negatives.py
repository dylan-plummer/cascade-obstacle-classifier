import bpy
from mathutils import Euler
from mathutils import Vector
import random
import math

def randomize_camera():
    x_loc = random.uniform(-49,49)
    y_loc = random.uniform(-49,49)
    z_loc = random.uniform(0.5,3)
    x_rot = random.uniform(30,90) / 180 * math.pi
    y_rot = 0
    z_rot = random.uniform(0,360) / 180 * math.pi
    cam = bpy.data.objects['Camera']
    cam.rotation_euler = Euler((x_rot, y_rot, z_rot), 'XYZ')
    cam.location = Vector((x_loc, y_loc, z_loc))

bpy.app.handlers.frame_change_post.append(randomize_camera)
