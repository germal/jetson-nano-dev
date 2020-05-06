# Gstreamer

## Install

```sh
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

## Run

To play webcam using gstreamer, you need to use `v4l2` driver input.

```sh
gst-launch-1.0 v4l2src ! xvimagesink
gst-launch-1.0 autovideosrc ! xvimagesink
```

`autovideosrc` automatically detect available camera sources.

```sh
gst-launch-1.0 -v v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1,width=640,height=480 ! xvimagesink
```

You can change properties of device input, raw format, width, height, framerate and so on.


## TroubleShooting

### no element "*"

```sh
gst-inspect-1.0 {whatelse}

No such element or plguin 'autovideosink'
No such element or plguin 'udpsrc'
```

If the same error occurs even after installing `gstreamer1.0-plugins-good`, it is a path problem.

```sh
export GST_PLUGIN_SYSTEM_PATH_1_0=$GST_PLUGIN_SYSTEM_PATH_1_0:/usr/lib/x86_64-linux-gnu/gstreamer-1.0
echo $GST_PLUGIN_SYSTEM_PATH_1_0
```