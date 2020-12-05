#!/bin/bash

gst-launch-1.0 v4l2src device=/dev/video4 ! videoconvert ! video/x-raw,format=I420,width=640,height=480 ! x264enc bframes=0 key-int-max=45 bitrate=512 tune=zerolatency ! h264parse ! video/x-h264,stream-format=avc,alignment=au,profile=baseline ! kvssink stream-name="" storage-size=512 access-key="" secret-key="" aws-region="ap-northeast-2"
