import cv2

from PyQt5 import QtCore
from PyQt5 import QtGui


class TrackingService(QtCore.QObject):
    tracking_signal = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self, camera, parent=None):
        super(TrackingService, self).__init__(parent)
        self.camera = camera

    @QtCore.pyqtSlot()
    def start(self):
        while True:
            rgb_frame, depth_frame, _ = self.camera.get_frames()

            
            qt_tracking_image = QtGui.QImage(seg_overlay.data, 640, 480, seg_overlay.strides[0], QtGui.QImage.Format_RGB888)
            
            self.tracking_signal.emit(qt_tracking_image)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(1, loop.quit)
            loop.exec_()
