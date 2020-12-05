import cv2
import sys
import time
import datetime
import zmq
import numpy as np

from camera import Camera, RealSense, RGBDCamera
from imageprocess import MotionDetect
from fcm_manager import FCMSender
from adb_manager import ADBSender
from config import *
from utils import *
from qt_widget import *

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


class SegmentationService(QtCore.QObject):
    seg_signal = QtCore.pyqtSignal(QtGui.QImage)
    
    client = zmq.Context().socket(zmq.SUB)
    client.bind("tcp://*:5556")
    client.setsockopt_string(zmq.SUBSCRIBE, str(''))

    def __init__(self, camera, parent=None):
        super(SegmentationService, self).__init__(parent)
        self.camera = camera

    @QtCore.pyqtSlot()
    def start(self):
        while True:
            msg = self.client.recv()

            src = rgba2rgb(np.frombuffer(msg, dtype=np.float32).reshape(480, 640, 4))

            qt_seg_image = QtGui.QImage(src.data, 640, 480, src.strides[0], QtGui.QImage.Format_RGB888)
            # qt_seg_image = qt_seg_image.scaled(640, 480, QtCore.Qt.KeepAspectRatio)

            self.seg_signal.emit(qt_seg_image)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(1, loop.quit)
            loop.exec_()


class Video(QtCore.QObject):
    rgb_signal = QtCore.pyqtSignal(QtGui.QImage)
    depth_signal = QtCore.pyqtSignal(QtGui.QImage)
    detect_signal = QtCore.pyqtSignal()
    
    def __init__(self, camera, parent=None):
        super(Video, self).__init__(parent)
        self.camera = camera

    @QtCore.pyqtSlot()
    def start(self):
        try:
            frame1, _ = self.camera.get_frames()
            frame2, _ = self.camera.get_frames()

            motion_detector = MotionDetect(frame1, frame2)

            prevTime = 0
            while True:
                color_image, depth_image = self.camera.get_frames()

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

                # detecting motion
                if motion_detector.distMap(color_image):
                    self.detect_signal.emit()
                    self._update_image_border(qt_rgb_image)  

                self.rgb_signal.emit(qt_rgb_image)

                # display depth image
                height, width, channel = depth_image.shape
                qt_depth_image = QtGui.QImage(depth_image.data,
                                        width,
                                        height,
                                        depth_image.strides[0],
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

    # FCM
    fcm_sender = FCMSender(api_key=FCM_API_KEY)
    fcm_sender.add_device(DEVICE_TOKEN)

    # ADB
    adb_sender = ADBSender()

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
    noti_button = QPushButton('Noti')

    vertical_layout = QVBoxLayout()
    vertical_layout.addLayout(grid_layout)
    vertical_layout.addWidget(table_viewer.table)
    vertical_layout.addWidget(start_button)
    vertical_layout.addWidget(seg_button)
    vertical_layout.addWidget(noti_button)
    vertical_layout.addWidget(clear_button)

    layout_widget = QWidget()
    layout_widget.setLayout(vertical_layout)

    # Button Event
    start_button.clicked.connect(video.start)
    seg_button.clicked.connect(segmentationService.start)
    clear_button.clicked.connect(table_viewer.clear)
    noti_button.clicked.connect(lambda: (
                                    fcm_sender.send(title="BeamMice", body="Detect Moving"),
                                    adb_sender.send("test contents"),
                                    table_viewer.addItem("Notify")))

    # Qt Event
    video.rgb_signal.connect(rgb_viewer.setImage)
    video.depth_signal.connect(depth_viewer.setImage)
    video.detect_signal.connect(lambda: table_viewer.addItem("Detect"))
    segmentationService.seg_signal.connect(inference_viewer.setImage)

    main_window = QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()

    sys.exit(app.exec_())
