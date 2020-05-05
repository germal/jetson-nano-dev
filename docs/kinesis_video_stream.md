# Kinesis Video Stream (KVS)

## Installation

```sh
git clone --recursive https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp.git
mkdir build
cd build
cmake .. -DBUILD_GSTREAMER_PLUGIN=ON -DBUILD_JNI=TRUE
make

export GST_PLUGIN_PATH={amazon-kinesis-video-streams-producer-sdk-cpp}/build
gst-inspect-1.0 kvssink
```

## Run

### Stream Video from an RTSP Camera

```sh
gst-launch-1.0 rtspsrc location="rtsp://YourCameraRtspUrl" short-header=TRUE ! rtph264depay ! video/x-h264, format=avc,alignment=au ! kvssink stream-name="YourStreamName" storage-size=512 access-key="YourAccessKey" secret-key="YourSecretKey" aws-region="YourAWSRegion"
```

### Encode and Stream Video from a USB Camera on Ubuntu

```sh
gst-launch-1.0 v4l2src do-timestamp=TRUE device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! x264enc  bframes=0 key-int-max=45 bitrate=500 ! video/x-h264,stream-format=avc,alignment=au,profile=baseline ! kvssink stream-name="YourStreamName" storage-size=512 access-key="YourAccessKey" secret-key="YourSecretKey" aws-region="YourAWSRegion"
```

## TroubleShooting

### Cmake step for libopenssl failed

When you encounter a `openssl_1_1_1 not found` error, you need to set the  `openssl` path.

```sh
which openssl # /usr/local/bin/openssl
echo "export LD_LIBRARY_PATH=/usr/local/bin/openssl" >> ~/.bashrc
```

# Reference

- [kinesis_video_streams_producer_github](https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp)
- [Kinesis Video Stremas: tips & tricks](https://www.alatortsev.com/2019/10/18/aws-kinesis-video-streams/)
- [Kinesis Video Streams Dev Document](https://docs.aws.amazon.com/ko_kr/kinesisvideostreams/latest/dg/kinesisvideo-dg.pdf)