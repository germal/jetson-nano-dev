import enum
import subprocess
import os

# model .pth path
NYU_RGB_NO_PRETRAIN = "segmentation/models/nyu_rgb_no_pretrain"
NYU_RGB_IMAGENET_PRETRAIN = "segmentation/models/nyu_rgb_imagenet_pretrain"
NYU_RGB_SCENENET_PRETRAIN = "segmentation/models/nyu_rgb_scenenet_pretrain"
NYU_RGBD_NO_PRETRAIN = "segmentation/models/nyu_rgbd_no_pretrain"
NYU_RGBD_SCENENET_PRETRAIN = "segmentation/models/nyu_rgbd_scenenet_pretrain"

SUN_RGB_NO_PRETRAIN = "segmentation/models/sun_rgb_no_pretrain"
SUN_RGB_IMAGENET_PRETRAIN = "segmentation/models/sun_rgb_imagenet_pretrain"
SUN_RGB_SCENENET_PRETRAIN = "segmentation/models/sun_rgb_scenenet_pretrain"
SUN_RGBD_NO_PRETRAIN = "segmentation/models/sun_rgbd_no_pretrain"
SUN_RGBD_SCENENET_PRETRAIN = "segmentation/models/sun_rgbd_scenenet_pretrain"

on_gpu = True
eval_mode = True
running_model = SUN_RGB_SCENENET_PRETRAIN

class CameraMode(enum.Enum):
    WEBCAM = 0
    REALSENSE = 1
    KVS = 2
    ZMQ = 3

camera_mode = CameraMode.REALSENSE
