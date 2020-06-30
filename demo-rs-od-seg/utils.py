import cv2
import time
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtGui


def get_current_time():
    return time.strftime("%m-%d %H:%M:%S", time.gmtime())


def createImageWithOverlay(baseImage, overlayImage):
    imageWithOverlay = QtGui.QImage(baseImage.size(), QtGui.QImage.Format_ARGB32_Premultiplied)
    painter = QtGui.QPainter(imageWithOverlay)

    painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
    painter.fillRect(imageWithOverlay.rect(), QtCore.Qt.transparent)

    painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
    painter.drawImage(0, 0, baseImage)

    painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
    painter.drawImage(0, 0, overlayImage)

    painter.end()
    
    return imageWithOverlay


def rgba2rgb( rgba, background=(255,255,255) ):
    row, col, ch = rgba.shape

    if ch == 3:
        return rgba

    assert ch == 4, 'RGBA image has 4 channels.'

    rgb = np.zeros( (row, col, 3), dtype='float32' )
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]

    a = np.asarray( a, dtype='float32' ) / 255.0

    R, G, B = background

    rgb[:,:,0] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,2] = b * a + (1.0 - a) * B

    return np.asarray( rgb, dtype='uint8' )


def update_overlay(baseImage):
    painter = QtGui.QPainter(baseImage)

    rec = QtGui.QPen(QtCore.Qt.red)
    painter.setPen(rec)

    painter.drawRect(10, 10, 20, 20)

    return qimage

