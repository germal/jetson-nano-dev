#!/bin/bash

gst-launch-1.0 -v v4l2src device=/dev/video2 ! video/x-raw, width=640,height=480 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=15.165.181.111 port=5000
