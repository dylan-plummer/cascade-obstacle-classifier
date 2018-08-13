import os

frames_dir = 'negatives'
results = open("bg.txt",'w')

directory = os.fsencode(frames_dir)
frame_i = 0

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        img_name = "%04d" % (frame_i,) + '.png'
        results.write(frames_dir + "/" + img_name + "\n")
        frame_i += 1

results.close()
