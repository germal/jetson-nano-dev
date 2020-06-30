import cv2

from PyQt5 import QtCore
from PyQt5 import QtGui

from tracking.tracking_model import TrackingModel
from config import *


class TrackingService(QtCore.QObject):
    tracking_signal = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self, camera, parent=None):
        super(TrackingService, self).__init__(parent)
        self.camera = camera
        self.model = TrackingModel(config_detection = config_detection,
                                    config_deepsort = config_deepsort,
                                    on_gpu=on_gpu_tracking)

    @QtCore.pyqtSlot()
    def start(self):
        while True:
            rgb_frame, _, _ = self.camera.get_frames()

            tracking_result = self.model.inference(rgb_frame)
            
            qt_tracking_image = QtGui.QImage(tracking_result.data, 
                                            640, 480, 
                                            tracking_result.strides[0], 
                                            QtGui.QImage.Format_RGB888)
            
            self.tracking_signal.emit(qt_tracking_image)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(1, loop.quit)
            loop.exec_()
