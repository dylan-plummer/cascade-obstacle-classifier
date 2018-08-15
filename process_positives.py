import os
import bpy
import numpy as np
import cv2

print(os.path.dirname(os.path.realpath(__file__)))
frame_i = 1
frames_dir = 'img'
results = open("info.dat",'w')
keys = ['filename', 'height', 'width', 'xmax', 'xmin', 'ymax', 'ymin']
directory = os.fsencode(frames_dir)

def save_depth_frame(scene):
    global frame_i
    # get viewer pixels
    pixels = bpy.data.images['Viewer Node'].pixels
    # size is always width * height * 4 (rgba)
    pixels = np.array(pixels)[::4]
    print (pixels.shape)

    ix = scene.render.resolution_x
    iy = scene.render.resolution_y
    #depth = np.reshape(pixels, (iy,ix))
    #depth = np.flipud(depth)

    try:
        #np.save('C:\\Users\\jumpr_000\\Desktop\\Desktop\\Machine Learning\\Obstacle Detection\\test_data\\npy\\' + str(frame_i) + '.npy', depth)
        #cv2.imwrite('img/' + str(frame_i) + '.png', depth)
        img_name = "%04d" % (frame_i,) + '.png'
        img_path = 'C:/Users/jumpr_000/Desktop/cascade-obstacle-classifier/img/labels/' + img_name
        print(img_path)
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

bpy.app.handlers.frame_change_post.append(save_depth_frame)
