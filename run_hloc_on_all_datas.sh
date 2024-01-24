#!/bin/sh

start=`date +%s`

IMAGES_PATH="Hierarchical-Localization/datasets/13camLoftr/images"
COLMAP_OUTPUT_PATH="Hierarchical-Localization/outputs/13camLoftr"

#Derotate images (use exif 'Orientation' tag to orient, then rotate image then delete the exif)
#REQUIRES PACKAGE 'imagemagick'
#shopt -s nullglob
#for file in "$IMAGES_PATH"/*.{jpg,jpeg,png}
#do
#    orientation=$(identify -format "%[orientation]" $file)
#    if ! [[ "$orientation" == "Undefined" || "$orientation" == "TopLeft" ]]; then
#        echo "$file has orientation $orientation, reorienting it..."
#        convert "$file" -auto-orient "$file"
#    fi
#done


python3 Hierarchical-Localization/pipeline_SfM.py --images $IMAGES_PATH --output $COLMAP_OUTPUT_PATH --num_pairs 11

python3 colmap2nerf.py --colmap_db "$COLMAP_OUTPUT_PATH/sfm_loftr" --text "$COLMAP_OUTPUT_PATH/sfm_loftr" --images "$IMAGES_PATH" --aabb_scale 16 --out "$IMAGES_PATH/transforms.json"

end=`date +%s`
runtime=$((end-start))
echo "Runtime: $runtime"
