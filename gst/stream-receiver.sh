#!/bin/bash

#gst-launch-1.0 -v filesrc location=mjpeg.avi ! avidemux ! queue ! jpegdec ! videoconvert ! videoscale ! autovideosink

gst-launch-1.0 -v udpsrc port=5000 ! application/x-rtp,encoding-name=JPEG,payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink
