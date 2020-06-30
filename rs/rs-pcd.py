import pyrealsense2 as rs
import numpy as np
import cv2
import time

from datetime import datetime
from os.path import expanduser

from pcd_app import PointCloudApp


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# camera intrinsics
profile = pipeline.get_active_profile()

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
align_to = rs.stream.color
align = rs.align(align_to)
colorizer = rs.colorizer()

prevTime = 0

pcd_app = PointCloudApp(profile)

cv2.namedWindow(pcd_app.state.WIN_NAME, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(pcd_app.state.WIN_NAME, pcd_app.mouse_cb)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        depth_frame = aligned_frames.get_depth_frame() 
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data())

        out = pcd_app.update(color_frame, depth_frame, color_image, depth_colormap)
        cv2.imshow(pcd_app.state.WIN_NAME, out)

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        curTime = time.time()
        fps = 1 / (curTime - prevTime)
        prevTime = curTime
        
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        #cv2.putText(images, str(fps), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:
    # Stop streaming
    pipeline.stop()

