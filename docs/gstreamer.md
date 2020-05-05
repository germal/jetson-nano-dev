# Gstreamer

## Install

```
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

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