import os
import cv2
import time
import argparse
import torch
import warnings
import numpy as np

from .detector import build_detector
from .deep_sort import build_tracker
from .utils.draw import draw_boxes
from .utils.parser import get_config
from .utils.io import write_results


class TrackingModel(object):
    def __init__(self, config_detection="./configs/yolov3.yaml", config_deepsort="./configs/deep_sort.yaml", on_gpu=True):
        self.cfg = get_config()
        self.cfg.merge_from_file(config_detection)
        self.cfg.merge_from_file(config_deepsort)

        use_cuda = on_gpu and torch.cuda.is_available()
        
        self.detector = build_detector(self.cfg, use_cuda=use_cuda)
        self.deepsort = build_tracker(self.cfg, use_cuda=use_cuda)
        class_name = self.detector.class_names

    def inference(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # detection
        bbox_xywh, cls_conf, cls_ids = self.detector(img)

        # select person class
        # cat: 16
        mask = cls_ids == 0

        bbox_xywh = bbox_xywh[mask]
        bbox_xywh[:, 3:] *= 1.2
        cls_conf = cls_conf[mask]

        # tracking
        outputs = self.deepsort.update(bbox_xywh, cls_conf, img)
        
        # draw bbox
        if len(outputs) > 0:
            bbox_tlwh = []
            bbox_xyxy = outputs[:, :4]
            identities = outputs[:, -1]
            result_img = draw_boxes(frame, bbox_xyxy, identities)

            for bb_xyxy in bbox_xyxy:
                bbox_tlwh.append(self.deepsort._xyxy_to_tlwh(bb_xyxy))
            
            return result_img

        else:
            return frame
