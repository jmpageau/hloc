import argparse
import numpy
import os
import sys
import re

class ColmapToTUM:

    def parse_colmap_images_txt(filepath):
        file = open(filepath)
        data = file.read()
        lines = data.replace(","," ").replace("\t"," ").split("\n")
        lines_list = [[v.strip() for v in line.split(" ") if v.strip()!=""] for line in lines if len(line)>0 and line[0]!="#"]
        images = {}
        for i in range(0, len(lines_list), 2):
            l = lines_list[i]
            images[l[0]] = {
                "IMAGE_ID": l[0],
                "QW": l[1],
                "QX": l[2],
                "QY": l[3],
                "QZ": l[4],
                "TX": l[5],
                "TY": l[6],
                "TZ": l[7],
                "CAMERA_ID": l[8],
                "NAME": l[9]
            }
        return images


    def write_tum_trajectory(images, output_path, write_timestamps="True"):
        file = open(output_path, 'w')
        #Header
        file.write("# timestamp tx ty tz qx qy qz qw\n")
        
        coord_min = [sys.float_info.max,sys.float_info.max,sys.float_info.max]
        coord_max = [sys.float_info.min,sys.float_info.min,sys.float_info.min]
        for v in images.values():
            #file name is the timestamp
            timestamp = os.path.splitext(v["NAME"])[0]
            tokens = []
            if write_timestamps.lower() == "true":
                match = re.search("[0-9.]*", timestamp)
                tokens.append(match.group(0))
            
            tokens.append(v["TX"][:7])
            tokens.append(v["TY"][:7])
            tokens.append(v["TZ"][:7])
            tokens.append(v["QX"][:7])
            tokens.append(v["QY"][:7])
            tokens.append(v["QZ"][:7])
            tokens.append(v["QW"][:7])
            line = " ".join(tokens) + "\n"
            
            file.write(line)
            
            coord_min[0] = min(coord_min[0], float(v["TX"]))
            coord_min[1] = min(coord_min[1], float(v["TY"]))
            coord_min[2] = min(coord_min[2], float(v["TZ"]))
            coord_max[0] = max(coord_max[0], float(v["TX"]))
            coord_max[1] = max(coord_max[1], float(v["TY"]))
            coord_max[2] = max(coord_max[2], float(v["TZ"]))
        
        path_split = os.path.splitext(output_path)
        file2 = open(path_split[0] + "_scale" + path_split[1], 'w')
        
        coords = [str(c) for c in coord_min+coord_max]
        file2.write(",".join(coords))
    
    
    def convert_file(colmap_file, output_file):
        images = ColmapToTUM.parse_colmap_images_txt(colmap_file)
        ColmapToTUM.write_tum_trajectory(images, output_file)


if __name__=="__main__":
    # parse command line
    parser = argparse.ArgumentParser(description='''
    Converts from Colmap 'text' export images.txt file to TUM-RGBD compatible trajectory, for analysis with evaluate_ate.py script
    ''')
    parser.add_argument('colmap_file', help='Colmap text export images.txt')
    parser.add_argument('output_file', help='Output text file')
    parser.add_argument('--write_timestamps', default="True", help='TUM needs timestamps, TartanAir needs to not have them')
    args = parser.parse_args()
    
    ColmapToTUM.convert_file(args.colmap_file, args.output_file)
    
