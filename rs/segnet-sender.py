import pyrealsense2 as rs
import numpy as np
import cv2
import zmq, sys
import imagezmq
import jetson.inference
import jetson.utils
import argparse
import ctypes


ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
target_address = "tcp://192.168.0.186:5556"
sock.connect(target_address)

# parse the command line
parser = argparse.ArgumentParser(description="Segment a live camera stream using an semantic segmentation DNN.", 
						   formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.segNet.Usage())

parser.add_argument("--network", type=str, default="fcn-resnet18-sun", help="pre-trained model to load, see below for options")
parser.add_argument("--filter-mode", type=str, default="linear", choices=["point", "linear"], help="filtering mode used during visualization, options are:\n  'point' or 'linear' (default: 'linear')")
parser.add_argument("--ignore-class", type=str, default="void", help="optional name of class to ignore in the visualization results (default: 'void')")
parser.add_argument("--alpha", type=float, default=175.0, help="alpha blending value to use during overlay, between 0.0 and 255.0 (default: 175.0)")
parser.add_argument("--camera", type=str, default="/dev/video2", help="index of the MIPI CSI camera to use (e.g. CSI camera 0)\nor for VL42 cameras, the /dev/video device to use.\nby default, MIPI CSI camera 0 will be used.")
parser.add_argument("--width", type=int, default=640, help="desired width of camera stream (default is 1280 pixels)")
parser.add_argument("--height", type=int, default=480, help="desired height of camera stream (default is 720 pixels)")

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# load the segmentation network
net = jetson.inference.segNet(opt.network, sys.argv)

# set the alpha blending value
net.SetOverlayAlpha(opt.alpha)

# allocate the output images for the overlay & mask
img_overlay = jetson.utils.cudaAllocMapped(opt.width * opt.height * 4 * ctypes.sizeof(ctypes.c_float))
img_mask = jetson.utils.cudaAllocMapped(320 * 240 * 4 * ctypes.sizeof(ctypes.c_float))

# create the camera and display
#camera = jetson.utils.gstCamera(opt.width, opt.height, opt.camera)
#display = jetson.utils.glDisplay()

sender = imagezmq.ImageSender(connect_to='tcp://*:5555', REQ_REP=False)

# Create a pipeline
pipeline = rs.pipeline()

#Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()  
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

# Streaming loop
try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

#        img, width, height = camera.CaptureRGBA(zeroCopy=1)

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imwrite("/home/yoo/rgb.jpg", color_image)

        img, width, height = jetson.utils.loadImageRGBA("/home/yoo/rgb.jpg")
        net.Process(img, width, height, opt.ignore_class)
        net.Overlay(img_overlay, width, height, opt.filter_mode)
        net.Mask(img_mask, 320, 240, opt.filter_mode)

        np_mask = jetson.utils.cudaToNumpy(img_mask, 320, 240, 4)
        sock.send(np_mask)

        # Render images
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        ret_code1, jpg_buffer1 = cv2.imencode(".jpg", color_image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        ret_code2, jpg_buffer2 = cv2.imencode(".jpg", depth_colormap, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        sender.send_jpg("rgb", jpg_buffer1)
        sender.send_jpg("depth", jpg_buffer2)

        images = np.hstack((color_image, depth_colormap))

        cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Align Example', images)
        key = cv2.waitKey(1)

        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
