import cv2

from PyQt5 import QtCore
from PyQt5 import QtGui

from segmentation.convert_my_data import reshape_nyu_rgb, reshape_sun_depth
from segmentation.color_mapping import *
from segmentation.segmentation_model import SegmentationModel
from segmentation.npy_to_image import segmentation_overlay
from config import *


class SegmentationService(QtCore.QObject):
    seg_signal = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self, camera, parent=None):
        super(SegmentationService, self).__init__(parent)
        self.camera = camera
        self.seg_model = SegmentationModel(running_model, on_gpu, eval_mode)

    @QtCore.pyqtSlot()
    def start(self):
        while True:
            rgb_frame, depth_frame, _ = self.camera.get_frames()

            rgb_data = reshape_nyu_rgb(rgb_frame)
            depth_data = reshape_sun_depth(depth_frame)
            
            np_seg = self.seg_model.inference(rgb_data, depth_data)
            seg_result = cv2.resize(class_from_instance(np_seg), dsize=(640, 480), interpolation=cv2.INTER_CUBIC)
            seg_overlay = segmentation_overlay(rgb_frame, np_seg, 0.5)
            
            qt_seg_image = QtGui.QImage(seg_overlay.data, 640, 480, seg_overlay.strides[0], QtGui.QImage.Format_RGB888)
            
            self.seg_signal.emit(qt_seg_image)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(1, loop.quit)
            loop.exec_()
