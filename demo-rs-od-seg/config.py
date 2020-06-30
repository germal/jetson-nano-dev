import enum
import subprocess
import os


class CameraMode(enum.Enum):
    WEBCAM = 0
    REALSENSE = 1
    KVS = 2
    ZMQ = 3

camera_mode = CameraMode.REALSENSE

# segmentation
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

on_gpu_seg = True
eval_mode = True
running_model = SUN_RGB_SCENENET_PRETRAIN


# deep sort
on_gpu_tracking = True
config_detection = "tracking/configs/yolov3.yaml"
config_deepsort = "tracking/configs/deep_sort.yaml"
