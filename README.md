#Image alignment pipeline
---

##Setup
Requires a Linux system due to the PyColmap dependency that does not (yet) exist on Windows

Requires Python >=3.7 and PyTorch >=1.1

First, use git to clone the repository at https://github.com/jmpageau/hloc
Don't forget to also pull the submodules, in a GUI client like tortoiseGit it is a checkbox, and on command-line it is:
```
git submodule update --init --recursive
```
Then install the python requirements with:
```
cd Hierarchical-Localization/
python -m pip install -e .
```
The imagemagick system package is also required for images pre-processing.
It can be installed with:
```
sudo apt install imagemagick
```

##Usage

We provide a convenience script named **run_hloc_on_all_datas.sh**
To use, open it and point the IMAGES_PATH variable near the top to the path of your image directory
COLMAP_OUTPUT_PATH should be set to the desired output location for the 3d model and cache files.

It then does 3 things:
1. Derotate the images (only required for InstantNerf compatibility)
2. Align all images
3. Convert the camera transforms to InstantNerf-compatible format

The step 2 can also be done in isolation if the Nerf visualisation is not needed.
It is done by calling the **Hierarchical-Localization/pipeline_SfM.py** script.

This script is the core of the method and can be adjusted with the following arguments:
| Argument | Effect | Default | Recommendation |
| -- | -- | -- | -- |
| images | folder of input images | - | - |
| output | folder for output files (cache files and generated colmap project) | - | - |
| loftr_max_kps | maximum number of keypoints to retain from LoFTR matching (top by confidence) | 8192 | 1000 - 16000, did tests at 4k and 8k, does not make much of a difference at these numbers |
| num_pairs | number of pairs to match for each input image | 10 | Can go as low as 3, found good results between 10-15, higher should be more robust. Computation time will increase as num_images * num_pairs. Can't exceed the number of input images |
| add_superpoint | concatenate superpoint features and superglue matches to the LoFTR ones | false | set to true to increase robustness in harder datasets |
| add_sift | concatenate SIFT features and nearest-neighbor-mutual matches to the LoFTR ones | false | set to true to increase robustness in harder datasets |


#Visualisation
---
##Transfer to InstantNerf
Follow the instructions here to setup InstantNerf: https://github.com/NVlabs/instant-ngp#installation

InstantNerf is technically compatible with Linux however my own setup (WSL) does not work with GUI apps, so I've setup InstantNerf on Windows and copy-paste the output of the pipeline to it for visualization.

When using the run_hloc_on_all_datas.sh script, the output folder will have the camera transforms along a copy of the images so that it can be easily copied as-is.

Then launch InstantNerf like this:
```
"instant-ngp/build/testbed.exe" --scene output/folder/from/pipeline --config instant-ngp/configs/nerf/base.json
```

Let it train for a minute or two, it might be useful (necessary for meshing) to define a tighter bounding box around the object of interest, to get rid of the background that is more noisy.

Then among other things, you can define a camera path, generate a full-resolution video, do the meshing (marching cubes algorithm) and export the result.

Also note that the NerfStudio (https://docs.nerf.studio/en/latest/quickstart/installation.html) project uses the same input format, and can be used as an alternative. The few tests we've done with it took longer to process but were higher quality.

