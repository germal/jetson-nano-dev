import torch
import torchfile
import numpy as np
from . import unet as un

from config import *


class SegmentationModel():
    def __init__(self, model=running_model, on_gpu=on_gpu_seg, eval_mode=eval_mode):
        self.on_gpu = on_gpu
        self.eval_mode = eval_mode

        self.model = self.get_network(model)
    
    def get_network(self, model_path):
        if model_path == (SUN_RGB_SCENENET_PRETRAIN or NYU_RGB_SCENENET_PRETRAIN):
            unet = un.UNet(14)
        elif model_path == (SUN_RGBD_SCENENET_PRETRAIN or NYU_RGBD_SCENENET_PRETRAIN):
            unet = un.UNetRGBD(14)

        unet.load_state_dict(torch.load(model_path + '.pth'))

        if self.on_gpu:
            unet.cuda()
        
        if self.eval_mode:
            unet.eval()

        return unet

    def inference(self, rgb_data, depth_data):
        if self.model.__class__ == un.UNet:
            return self.inference_rgb(rgb_data)
        elif self.model.__class__ == un.UNetRGBD:
            return self.inference_rgbd(rgb_data, depth_data)
        return None

    def inference_rgb(self, rgb_data):
        scaled_rgb = np.expand_dims(rgb_data,0)
        torch_rgb = torch.tensor(scaled_rgb,dtype=torch.float32)
        
        if self.on_gpu:
            pred = self.model.forward(torch_rgb.cuda())
            pred_numpy = pred.cpu().detach().numpy()
        else:
            pred = self.model.forward(torch_rgb)
            pred_numpy = pred.detach().numpy()

        new_pred = np.argmax(pred_numpy[0],axis=0)

        return new_pred

    def inference_rgbd(self, rgb_data, depth_data):
        scaled_rgb = np.expand_dims(rgb_data,0)
        scaled_depth = np.expand_dims(depth_data,0)

        torch_rgb = torch.tensor(scaled_rgb,dtype=torch.float32)
        torch_depth = torch.tensor(scaled_depth,dtype=torch.float32)

        if self.on_gpu:
            pred = self.model.forward((torch_rgb.cuda(),torch_depth.cuda()))
            pred_numpy = pred.cpu().detach().numpy()
        else:
            pred = self.model.forward((torch_rgb,torch_depth))
            pred_numpy = pred.detach().numpy()

        new_pred = np.argmax(pred_numpy[0],axis=0)

        return new_pred
