import os
import shutil
import numpy as np

#You only need to use this script once per sample folder

#Point it to TartanAir's folder, it will list all folders, which should be individual samples of the TartanAir dataset.
#It will make a copy of the image files in the image_left folder, composing the new name using only the numbers of the original name.
#Then it will use those new names as the 'timestamp' field in (first column) the ground truth file 'pose_left.txt'
#Writes the result into a new file named 'pose_left_with_timestamps.txt' 


def process_folder(folder):
    image_folder = os.path.join(folder, "image_left")
    if not os.path.exists(image_folder):
        print("No images in " + folder)
        return
    else:
        print("Processing " + folder)

    #renamed_dir = os.path.join(folder, "image_left_renamed")
    #if not os.path.exists(renamed_dir):
    #    os.mkdir(renamed_dir)
    
    image_files = []
    for img_file in os.listdir(image_folder):
        filename, ext = os.path.splitext(img_file)
        if ext.lower() == ".png":
            #src = os.path.join(image_folder, img_file)
            #dst = os.path.join(renamed_dir, filename[:6] + ".png")
            #if not os.path.exists(dst):
            #    shutil.copy(src, dst)
            image_files.append(filename[:6]) #use only the number at the beginning
        
    image_files.sort()

    gt_traj = np.loadtxt(os.path.join(folder, "pose_left.txt"))

    #concatenate as columns
    output = np.c_[image_files, gt_traj]

    file = open(os.path.join(folder, "pose_left_with_timestamps.txt"), 'w')
    #Header
    file.write("# timestamp tx ty tz qx qy qz qw\n")
    for row in output:
        line = " ".join(row)
        file.write(line + "\n")


root = """D:\workspace\Hierarchical-Localization\datasets\TartanAir"""
for d_name in os.listdir(root):
    process_folder(os.path.join(root, d_name))


