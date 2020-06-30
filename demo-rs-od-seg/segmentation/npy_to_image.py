import argparse
from PIL import Image
import numpy as np
import cv2
import os
import matplotlib.image as mpimg
from utils import *
from .color_mapping import *


rgbd_path = "data/"
segmentation_path = "result/"


def rgbd_npy_to_image(rgbd_path, alpha=0.7):
    # ids
    img_ids = list()
    for filename in os.listdir(rgbd_path):
        if filename.endswith('.npy'):
            img_ids.append(filename.split('.')[0].split('_')[0])
    img_ids = list(set(img_ids))

    for filename in img_ids:
       np_rgb = np.load(rgbd_path + filename + "_RGB.npy")
       img_rgb = Image.fromarray(np_rgb)
       mpimg.imsave(rgbd_path + filename + "_RGB.jpg", np_rgb)

       # depth
       np_depth = np.load(rgbd_path + filename + "_DEPTH.npy")
       norm_depth = cv2.normalize(np_depth, None, 0, 255, cv2.NORM_MINMAX)
       cvt_depth = cv2.cvtColor(norm_depth, cv2.COLOR_GRAY2BGR)
       np_depth = cvt_depth.astype(np.uint8)
       mpimg.imsave(rgbd_path + filename + "_DEPTH.jpg", np_depth)

       # rgb + depth
       merge = cv2.addWeighted(np_rgb, alpha, np_depth, 1 - alpha, 0)
       mpimg.imsave(rgbd_path + filename + "_SUM.jpg", merge)


# segmentation class
def segmentation_color_mapping(rgbd_path, segmentation_path, alpha=0.8):
    for filename in os.listdir(segmentation_path):
        if filename.endswith('.npy'):
            n = np.load(segmentation_path + filename)
            np_seg = class_from_instance(n)
            np_seg = cv2.resize(np_seg, dsize=(640, 480), interpolation=cv2.INTER_CUBIC)
            
            if alpha==0:
                mpimg.imsave(sagmentation_path + filename + ".jpg", np_seg)
        
            else:
                np_rgb = cv2.imread(rgbd_path + filename.split('_')[0] + "_RGB.jpg")
                merge = cv2.addWeighted(np_rgb, alpha, np_seg, 1 - alpha, 0)
                mpimg.imsave(segmentation_path + filename + ".jpg", merge)


def segmentation_overlay(np_rgb, np_seg, alpha=0.8):
    np_seg = class_from_instance(np_seg)
    np_seg = cv2.resize(np_seg, dsize=(640, 480), interpolation=cv2.INTER_CUBIC)
    merge = cv2.addWeighted(np_rgb, alpha, np_seg, 1 - alpha, 0)
    return merge


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="save rgbd image & segmentation color mapping")

    parser.add_argument('--rgbd_path', help='rgbd np folder path', default=rgbd_path)
    parser.add_argument('--seg_path', help='segmentation np folder path', default='')
    parser.add_argument('--rgbd_alpha', help='rgb + depth image weight (0~1)', default=0.7)
    parser.add_argument('--seg_alpha', help='rgb + segmentation image weight (0~1)', default=0.8)
    args = parser.parse_args()

    rgbd_npy_to_image(args.rgbd_path, args.rgbd_alpha)
    if not args.seg_path:    
        segmentation_color_mapping(args.rgbd_path, args.segmentation_path, args.seg_alpha)
    
    
