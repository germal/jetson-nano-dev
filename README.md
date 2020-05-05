# Setting

## Env

```
OS : Ubuntu 18.04
JetPack 4.4
CUDA : 10.2.89
cuDNN : 8.0.0
```

## Installation

1. Download JetPack SDK

- Download the SD Card Image and NVIDIA SDK Manager. 
  [JetPack SDK](https://developer.nvidia.com/embedded/jetpack#install)
- Write Image to the microSD card and install Jetson software with SDK Manager [get-started-jetson-nano](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write)

```sh
# https://github.com/rbonghi/jetson_stats
sudo -H pip install -U jetson-stats

# status and information 
jetson_release

# system monitoring
jtop 
```

jetson-stats is a package to monitoring and control your NVIDIA Jetson. It is require to reboot.

2. CUDA path

```sh
echo "# Add CUDA bin & library paths:" >> ~/.bashrc
echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/cuda/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
source ~/.bashrc

nvcc -V
```

3. Python

```
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
rm get-pip.py
```

4. virtualenv

```sh
sudo -H pip install virtualenv virtualenvwrapper

echo "# virtualenv & virtualenvwrapper" >> ~/.bashrc
echo "export WORKON_HOME=$HOME/virtualenvs" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

mkvirtualenv {env_name} -p python3
```

## Power

- Mode 0

```sh
sudo nvpmodel -m0
```

Use 5V/4A Adapter. It is necessary to install `J48` jumper.

- Mode 1

```sh
sudo nvpmodel -m1
```

Use 5V/2A Micro USB. It have to remove `J48` jumper.

- Mode check

```sh
sudo nvpmodel -q
```

## 3rd party

### Camera

- [Open CV](./docs/opencv.md)
- [RPi Camera V2](./docs/rpi_camera_v2.md)
- [RealSense Camera](./docs/realsense_camera.md)

### Streaming

- [GStreamer](./docs/gstreamer.md)
- [AWS Kiinesis Video Stream](./docs/kinesis_video_stream.md)

### DeepLearning

- [TF_Pytorch](./docs/tf_torch.md)

# Notes

## v4l2-ctl

```sh
sudo apt install v4l-utils
```

Use `v4l2-ctl` for control when developing camera drivers.

```sh
v4l2-ctl -d /dev/video0 --list-formats-ext
```

Check supported image foramts and resolutions for specific devices.


# Reference

- [Get-started-jetson-nano-devkit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
