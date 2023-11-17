#!/usr/bin/env python
# coding: utf-8
import argparse
from pathlib import Path
from hloc import extract_features, match_features, reconstruction, visualization, pairs_from_retrieval, match_dense


def main(args):

    images = args.images
    output_path = args.output
    loftr_max_kps = args.loftr_max_kps
    num_pairs = args.num_pairs
    add_superpoint = args.add_superpoint
    add_sift = args.add_sift

    images = Path(images)
    outputs = Path(output_path)
    sfm_pairs = outputs / 'pairs-netvlad-loftr.txt'
    sfm_dir = outputs / 'sfm_loftr'

    retrieval_conf = extract_features.confs['netvlad']
    dense_conf = match_dense.confs['loftr']

    #Choose the most similar image pairs
    retrieval_path = extract_features.main(retrieval_conf, images, outputs)
    pairs_from_retrieval.main(retrieval_path, sfm_pairs, num_matched=num_pairs)
    
    all_features = []
    all_matches = []
    
    #Extract features and matches with LoFTR
    features, matches = match_dense.main(dense_conf, sfm_pairs, images, export_dir=outputs, max_kps=loftr_max_kps)
    all_features.append(features)
    all_matches.append(matches)
    
    if add_superpoint:
        #Concatenate Superpoint/Superglue features and matches
        superpoint_conf = extract_features.confs['superpoint_aachen']
        superglue_conf = match_features.confs['superglue']
        superpoint_features = extract_features.main(superpoint_conf, images, outputs)
        superglue_matches = match_features.main(superglue_conf, sfm_pairs, superpoint_conf['output'], outputs)
        all_features.append(superpoint_features)
        all_matches.append(superglue_matches)
    
    if add_sift:
        #Concatenate SIFT features and matches
        sift_conf = extract_features.confs['sift']
        sift_nn_conf = match_features.confs['NN-mutual']
        sift_features = extract_features.main(sift_conf, images, outputs)
        sift_matches = match_features.main(sift_nn_conf, sfm_pairs, sift_conf['output'], outputs)
        all_features.append(sift_features)
        all_matches.append(sift_matches)
    
    #Reconstruct the sparse model using all possible features and matches
    model = reconstruction.main(sfm_dir, images, sfm_pairs, all_features, all_matches)
    if model:
        model.write_text(str(sfm_dir))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--loftr_max_kps', type=int, required=False, default=8192)
    parser.add_argument('--num_pairs', type=int, required=False, default=10)
    parser.add_argument('--add_superpoint', action='store_true', required=False, default=False)
    parser.add_argument('--add_sift', action='store_true', required=False, default=False)
    args = parser.parse_args()
    main(args)
