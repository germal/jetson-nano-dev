#!/bin/bash

gst-launch-1.0 -v v4l2src device=/dev/video2 ! video/x-raw, width=640,height=480 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=127.0.0.1 port=5000
