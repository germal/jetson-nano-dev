import cv2

from PyQt5 import QtCore
from PyQt5 import QtGui


class Video(QtCore.QObject):
    rgb_signal = QtCore.pyqtSignal(QtGui.QImage)
    depth_signal = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self, camera, parent=None):
        super(Video, self).__init__(parent)
        self.camera = camera

    @QtCore.pyqtSlot()
    def start(self):
        try:
            while True:
                color_image, depth_image, depth_colormap = self.camera.get_frames()

                # display rgb image
                color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                height, width, channel = color_image.shape

                qt_rgb_image = QtGui.QImage(color_image.data,
                                        width,
                                        height,
                                        color_image.strides[0],
                                        QtGui.QImage.Format_RGB888)

                self.rgb_signal.emit(qt_rgb_image)

                # display depth image
                height, width, channel = depth_colormap.shape
                qt_depth_image = QtGui.QImage(depth_colormap.data,
                                        width,
                                        height,
                                        depth_colormap.strides[0],
                                        QtGui.QImage.Format_RGB888)


                self.depth_signal.emit(qt_depth_image)

                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(1, loop.quit)
                loop.exec_()
        finally:
            self.camera.stop()

    def stop(self):
        self.realsense.stop()
    
    def _update_image_border(self, image):
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor("red"))
        
        painter = QtGui.QPainter()
        painter.begin(image)
        painter.setPen(pen)
        painter.drawRect(0, 0, image.width(), image.height())
        painter.end()
