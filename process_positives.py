import os
import bpy
import numpy as np
from mathutils import Euler
from mathutils import Vector
import random
import math
import cv2

print(os.path.dirname(os.path.realpath(__file__)))
frame_i = 1
frames_dir = 'img'
results = open("info.dat",'w')
keys = ['filename', 'height', 'width', 'xmax', 'xmin', 'ymax', 'ymin']
directory = os.fsencode(frames_dir)

def save_depth_frame(scene):
    global frame_i
    randomize_camera()
    try:
        img_name = "%04d" % (frame_i,) + '.png'
        img_path = 'C:/Users/jumpr_000/Desktop/cascade-obstacle-classifier/img/labels/' + img_name
        img = cv2.imread(img_path)
        print(img.shape)
        imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret,thresh = cv2.threshold(imgray,0,255,cv2.THRESH_BINARY)
        #begin contour detection
        image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        color = cv2.drawContours(img, contours, -1, (0,255,0), 1)
        bounding_box = ''
        for cntr in contours:
            x,y,obj_length,obj_height = cv2.boundingRect(cntr)
            print(x,y,obj_length,obj_height)
            rect = cv2.minAreaRect(cntr)
            cv2.rectangle(color,(x,y),(x+obj_length,y+obj_height),(0,255,0),2)
            bounding_box += ("{0} {1} {2} {3}   ".format(x, y, obj_length, obj_height))
        label = "img/" + img_name + "  " + str(len(contours)) + "  " + bounding_box + "\n"
        print(label)
        results.write(label)
        frame_i += 1
        print ("Saved...")
    except Exception as inst:
        print("There was an error we caught")
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly

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

bpy.app.handlers.frame_change_post.append(save_depth_frame)
