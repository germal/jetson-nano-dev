import cv2

from PyQt5 import QtCore
from PyQt5 import QtGui


class PointCloudService(QtCore.QObject):
    pcd_signal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, camera, parent=None):
        super(PointCloudService, self).__init__(parent)
        self.camera = camera

    @QtCore.pyqtSlot()
    def start(self):
        try:
            while True:
                out = self.camera.get_pointcloud()
                
                out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
                height, width, channel = out.shape

                qt_pcd_image = QtGui.QImage(out.data,
                                        width,
                                        height,
                                        out.strides[0],
                                        QtGui.QImage.Format_RGB888)

                self.pcd_signal.emit(qt_pcd_image)

                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(1, loop.quit)
                loop.exec_()
        finally:
            self.camera.stop()
