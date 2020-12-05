# https://github.com/jmccormac/pySceneNetRGBD/blob/master/convert_instance2class.py

import numpy as np


# nyu classes 13
color_code = np.array([[0, 0, 0], #UNKNOWN
                       [0, 0, 1], #BED
                       [0.9137,0.3490,0.1882], #BOOKS
                       [0, 0.8549, 0], #CEILING
                       [0.5843,0,0.9412], #CHAIR
                       [0.8706,0.9451,0.0941], #FLOOR
                       [1.0000,0.8078,0.8078], #FURNITURE
                       [0,0.8784,0.8980], #OBJECTS
                       [0.4157,0.5333,0.8000], #PAINTING
                       [0.4588,0.1137,0.1608], #SOFA
                       [0.9412,0.1373,0.9216], #TABLE
                       [0,0.6549,0.6118], #TV
                       [0.9765,0.5451,0], #WALL
                       [0.8824,0.8980,0.7608]]) #WINDOW

# nyu classes 40 to 13
nyu_40_to_13_classes = [0, 12, 5, 6, 1, 4, 9, 10, 12, 13, 6, 8, 6, 13, 10, 6, 13, 6, 7, 7, 5, 7, 3, 2, 6, 11, 7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 7, 6, 7]


def class_from_instance(n):
    h, w = n.shape
    class_img_rgb = np.zeros((h,w,3),dtype=np.uint8)
    r = class_img_rgb[:,:,0]
    g = class_img_rgb[:,:,1]
    b = class_img_rgb[:,:,2]

    for instance_id in range(13):
        r[n==instance_id] = np.uint8(color_code[instance_id][0]*255)
        g[n==instance_id] = np.uint8(color_code[instance_id][1]*255)
        b[n==instance_id] = np.uint8(color_code[instance_id][2]*255)

    class_img_rgb[:,:,0] = r
    class_img_rgb[:,:,1] = g
    class_img_rgb[:,:,2] = b

    return class_img_rgb


def class_40_from_instance(n):
    h, w = n.shape
    class_img_rgb = np.zeros((h,w,3),dtype=np.uint8)
    r = class_img_rgb[:,:,0]
    g = class_img_rgb[:,:,1]
    b = class_img_rgb[:,:,2]

    for instance_id in range(len(nyu_40_to_13_classes)):
        color_id = nyu_40_to_13_classes[instance_id]
        r[n==instance_id] = np.uint8(color_code[color_id][0]*255)
        g[n==instance_id] = np.uint8(color_code[color_id][1]*255)
        b[n==instance_id] = np.uint8(color_code[color_id][2]*255)

    class_img_rgb[:,:,0] = r
    class_img_rgb[:,:,1] = g
    class_img_rgb[:,:,2] = b

    return class_img_rgb


def merge_class(to_class_index, from_class_index):
    color_code[from_class_index] = color_code[to_class_index]


# merge_class(12, 0)
# merge_class(7, 1)
# merge_class(7, 2)
# merge_class(7, 4)
# merge_class(7, 6)
# merge_class(12, 8)
# merge_class(7, 9)
# merge_class(7, 10)
# merge_class(7, 11)
# merge_class(12, 13)