import cv2
import sys
import time
import datetime
import zmq
import numpy as np

from camera import Camera, RealSense, RGBDCamera
from config import *
from utils import *
from qt_widget import *

from segmentation.convert_my_data import reshape_nyu_rgb, reshape_sun_depth
from segmentation.color_mapping import *
from segmentation.segmentation_model import SegmentationModel
from segmentation.npy_to_image import segmentation_overlay

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


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
            # qt_seg_image = qt_seg_image.scaled(640, 480, QtCore.Qt.KeepAspectRatio)

            self.seg_signal.emit(qt_seg_image)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(1, loop.quit)
            loop.exec_()


class Video(QtCore.QObject):
    rgb_signal = QtCore.pyqtSignal(QtGui.QImage)
    depth_signal = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self, camera, parent=None):
        super(Video, self).__init__(parent)
        self.camera = camera

    @QtCore.pyqtSlot()
    def start(self):
        try:
            prevTime = 0
            while True:
                color_image, depth_image, depth_colormap = self.camera.get_frames()

                # fps
                curTime = time.time()
                sec = curTime - prevTime
                prevTime = curTime
                # print(1/sec)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    if camera_mode == CameraMode.REALSENSE:
        camera = RealSense()
        camera.start()  
    elif camera_mode == CameraMode.WEBCAM:
        camera = Camera(video_index=0)
    elif camera_mode == CameraMode.KVS:
        camera = Camera(stream_name="beam-test-1")
    elif camera_mode == CameraMode.ZMQ:
        camera = RGBDCamera(ip="192.168.0.110")
    else:
        print("Camera Mode is not set")
        sys.exit(app.exec_())

    # Video thread
    video_thread = QtCore.QThread()
    video_thread.start()
    video = Video(camera)
    video.moveToThread(video_thread)

    # Segmentation service thread
    seg_inf_thread = QtCore.QThread()
    seg_inf_thread.start()
    segmentationService = SegmentationService(camera)
    segmentationService.moveToThread(seg_inf_thread)
    
    # Qt View
    rgb_viewer = ImageViewer()
    depth_viewer = ImageViewer()
    inference_viewer = ImageViewer()
    overlay_viewer = ImageViewer()
    table_viewer = TableViewer()

    grid_layout = QGridLayout()
    grid_layout.addWidget(rgb_viewer, 0, 0)
    grid_layout.addWidget(depth_viewer, 0, 1)
    grid_layout.addWidget(inference_viewer, 1, 0)
    grid_layout.addWidget(overlay_viewer, 1, 1)

    start_button = QPushButton('Start')
    seg_button = QPushButton('Segmentation')
    clear_button = QPushButton('Clear')

    vertical_layout = QVBoxLayout()
    vertical_layout.addLayout(grid_layout)
    vertical_layout.addWidget(table_viewer.table)
    vertical_layout.addWidget(start_button)
    vertical_layout.addWidget(seg_button)
    vertical_layout.addWidget(clear_button)

    layout_widget = QWidget()
    layout_widget.setLayout(vertical_layout)

    # Button Event
    start_button.clicked.connect(video.start)
    seg_button.clicked.connect(segmentationService.start)
    clear_button.clicked.connect(table_viewer.clear)

    # Qt Event
    video.rgb_signal.connect(rgb_viewer.setImage)
    video.depth_signal.connect(depth_viewer.setImage)
    segmentationService.seg_signal.connect(inference_viewer.setImage)

    main_window = QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()

    sys.exit(app.exec_())
