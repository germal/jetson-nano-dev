import numpy as np
import cv2
import os
import matplotlib.image as mpimg
from PIL import Image
from utils import *

source_path = "data"
output_path = "data2"


def reshape_nyu_rgb(n):
    img = Image.fromarray(n)
    img = img.resize(size=(320, 240), resample=Image.NEAREST)
    resized = np.array(img, dtype='float32')
    reshaped = np.transpose(resized, (2, 0, 1)) / 255.0
    return reshaped

def reshape_nyu_depth(n):
    img = Image.fromarray(n)
    img = img.resize(size=(320, 240), resample=Image.NEAREST)
    resized = np.array(img, dtype='float32')
    reshaped = resized.reshape(1, 240, 320) / 1000.0
    return reshaped

def reshape_sun_depth(n):
    img = Image.fromarray(n)
    img = img.resize(size=(320, 240), resample=Image.NEAREST)
    resized = np.array(img, dtype='float32')
    reshaped = resized.reshape(1, 240, 320) / 10000.0
    return reshaped


if __name__ == "__main__":
    os.makedirs(output_path, exist_ok=True)

    for filename in os.listdir(source_path):
        if filename.endswith('RGB.npy'):
            # np
            img = reshape_nyu_rgb(np.load(source_path + "/" + filename))
            n = np.array(img, dtype='float32')
            np.save(output_path + "/" + filename, n)

            # img
            #np_img = reshape_img_rgb(n)
            #save_np_to_image(output_path + "/" + filename.split('.')[0] + ".jpg", np_img)
        elif filename.endswith('DEPTH.npy'):
            # np
            img = reshape_sun_depth(np.load(source_path + "/" + filename))
            n = np.array(img, dtype='float32')
            np.save(output_path + "/" + filename, n)

            # img
            #np_img = reshape_img_depth(n)
            #save_np_to_image(output_path + "/" + filename.split('.')[0] + ".jpg", np_img)


