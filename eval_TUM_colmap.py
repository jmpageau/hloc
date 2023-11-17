import argparse
import os
import csv
import sys
import math
from pathlib import Path

TartanAir_folder = """Hierarchical-Localization/datasets/TartanAir/hospital_P000/"""
TartanAir_colmap_folder = "ColmapProjectsLoftr15"
TartanAir_pose_filename = "pose_left_with_timestamps.txt"

TUM_folder = """Hierarchical-Localization/datasets/Tum/"""
TUM_colmap_folder = "rgbd_dataset_freiburg1_xyz"
TUM_pose_filename = "groundtruth_xyz.txt"


def compute_tum_scales(filepath):
    coord_min = [sys.float_info.max,sys.float_info.max,sys.float_info.max]
    coord_max = [sys.float_info.min,sys.float_info.min,sys.float_info.min]

    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ') 
        for line in reader:
            if line[0] == "#":
                continue #Skip header
            # timestamp tx ty tz qx qy qz qw
            # 1305031449.7996 1.2334 -0.0113 1.6941 0.7907 0.4393 -0.1770 -0.3879
            coord_min[0] = min(coord_min[0], float(line[1]))
            coord_min[1] = min(coord_min[1], float(line[2]))
            coord_min[2] = min(coord_min[2], float(line[3]))
            coord_max[0] = max(coord_max[0], float(line[1]))
            coord_max[1] = max(coord_max[1], float(line[2]))
            coord_max[2] = max(coord_max[2], float(line[3]))
    
    return (coord_max[0] - coord_min[0],
            coord_max[1] - coord_min[1],
            coord_max[2] - coord_min[2])


def get_colmap_scales(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            #max - min for each of 3 coords
            return (float(line[3]) - float(line[0]),
                    float(line[4]) - float(line[1]),
                    float(line[5]) - float(line[2]))


def process_folder(root_folder, colmap_project_folder, pose_filename):
    folder = os.path.join(root_folder, colmap_project_folder)
    for d_name in os.listdir(folder):
        d = os.path.join(folder, d_name)
        print(os.path.isdir(d))
        if os.path.isdir(d):
            print("Processing " + d)
            colmap_cams_file = os.path.join(d, "images.txt")
            tum_cams_file = os.path.join(d, "cameras_tum.txt")
            if os.path.exists(colmap_cams_file):
                #Convert colmap text output to TUM format
                os.system(" ".join(["python3", "colmap_text_to_TUM_trajectory.py", colmap_cams_file, tum_cams_file]))
                
                #Compute the scale factor by comparing the bounding boxes sizes (distance between the 2 corners)
                colmap_scales = get_colmap_scales(os.path.join(d, "tum_trajectory_scale.txt"))
                tum_scales = compute_tum_scales(os.path.join(root_folder, d_name, pose_filename))
                colmap_size = math.sqrt(colmap_scales[0] ** 2 + colmap_scales[1] ** 2 + colmap_scales[2] ** 2)
                tum_size = math.sqrt(tum_scales[0] ** 2 + tum_scales[1] ** 2 + tum_scales[2] ** 2)
                avg_scale = tum_size / colmap_size
                avg_scale = str(avg_scale)
                print("Scale " + avg_scale)
                
                #Evaluate the trajectory, the script does a translation/rotation alignement, it just needs the correct scale
                print(TUM_folder)
                os.system(" ".join(["python3", os.path.join(TUM_folder, "scripts/evaluate_ate.py"), os.path.join(root_folder, d_name, pose_filename), os.path.join(d, "cameras_tum.txt"), "--scale", avg_scale, "--plot", d_name + "_trajectory.png", "--verbose"]))
                print("Finish")
            else:
                print("Colmap has not run (or has failed) for " + d_name)

#if __name__=="__main__":
#    # parse command line
#    parser = argparse.ArgumentParser(description='''
#    Eval Tartanair ol tum datadas with groudtruth
#    ''')
#    parser.add_argument('TartanAirFolder',type=Path, help='Path to folder where tartanair datas are')
#    parser.add_argument('TartanAirColmapFolder',type=Path, help='name of the folder with colmap project')
#    parser.add_argument('TartanAirPoseFilename',type=Path, help='tartan air grountruth previously get')
#    args = parser.parse_args()
#    
#    print(args.TartanAirFolder)
#    print(args.TartanAirColmapFolder)
#    print(args.TartanAirPoseFilename)
process_folder(TartanAir_folder, TartanAir_colmap_folder, TartanAir_pose_filename)
#process_folder(TUM_folder, TUM_colmap_folder, TUM_pose_filename)
