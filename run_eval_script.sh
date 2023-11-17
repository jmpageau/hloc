#!/bin/sh
tartanairfolder="D:/workspace/Hierarchical-Localization/datasets/TartanAir/endofworld_P001"
TartanAirColmapFolder="ColmapProjects"
TartanAirPoseFilename = "pose_left_with_timestamps.txt"


python3 eval_TUM_colmap.py --TartanAirFolder $tartanairfolder --TartanAirColmapFolder $TartanAirColmapFolder --TartanAirPoseFilename "pose_left_with_timestamps.txt"