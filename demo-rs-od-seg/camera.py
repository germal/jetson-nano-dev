import cv2
import pyrealsense2 as rs
import numpy as np
import boto3
import imagezmq


class ICamera():
    def __init__(self):
        pass
    
    def get_frames(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class Camera(ICamera):
    def __init__(self, stream_name=None, video_index=0):
        self.camera = None
        self.frame = None
        
        if stream_name is None:
            self.camera = cv2.VideoCapture(video_index)
        else:
            kvs = boto3.client("kinesisvideo")
            endpoint = kvs.get_data_endpoint(
                APIName="GET_HLS_STREAMING_SESSION_URL",
                StreamName=stream_name
            )['DataEndpoint']

            print(endpoint)

            kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
            url = kvam.get_hls_streaming_session_url(
                StreamName=stream_name,
                PlaybackMode="LIVE"
            )['HLSStreamingSessionURL']

            self.camera = cv2.VideoCapture(url)
    
    def get_frames(self):
        try:
            _, self.frame = self.camera.read()
        finally:
            return self.frame, self.frame


class RealSense(ICamera):
    def __init__(self):
        self.pipeline = rs.pipeline()
        self.align = rs.align(rs.stream.color)

        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    
    def start(self):
        profile = self.pipeline.start(self.config)

        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()

    def stop(self):
        self.pipeline.stop()

    def get_frames(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        return color_image, depth_image, depth_colormap


class RGBDCamera(ICamera):
    def __init__(self, ip='localhost', port=5555):
        self.image_hub = imagezmq.ImageHub(open_port='tcp://' + ip + ':' + str(port), REQ_REP=False)
        self.color_image = self.depth_image = None

    def get_frames(self):
        name, jpg_buffer = self.image_hub.recv_jpg()
        image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype='uint8'), -1)

        if name =='rgb':
            self.color_image = image
        elif name == 'depth':
            self.depth_image = image

        return self.color_image, self.depth_image