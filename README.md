# Setting

## Installation

1. Write Image to the microSD Card
   [Reference Link](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write)

```sh
sudo -H pip install jetson-stats
jetson_release
```

2. CUDA path

```sh
echo "# Add CUDA bin & library paths:" >> ~/.bashrc
echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/cuda/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
source ~/.bashrc
```

3. Install tensorflow

```sh
sudo apt-get install python3-pip
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev
pip3 install -U pip
pip3 install -U numpy grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast h5py astor termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta

# TF-2.x
$ sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow==2.1.0+nv20.3

# TF-1.15
$ sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow==1.15.2+nv20.3
```
- [Reference Link](https://forums.developer.nvidia.com/t/official-tensorflow-for-jetson-nano/71770)

4. Install Pytorch

- torch

```sh
wget https://nvidia.box.com/shared/static/ncgzus5o23uck9i5oth2n8n06k340l6k.whl -O torch-1.4.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base
pip3 install Cython
pip3 install numpy torch-1.4.0-cp36-cp36m-linux_aarch64.whl
```

- torchvision

```
sudo apt-get install libjpeg-dev zlib1g-dev
git clone --branch v0.5.0 https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
cd torchvision
sudo python setup.py install
cd ../  # attempting to load torchvision from build dir will result in import error
```

- [Reference Link](https://forums.developer.nvidia.com/t/pytorch-for-jetson-nano-version-1-4-0-now-available/72048)

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

# OpenCV

## Requirements

```sh
sudo apt istall cmake
```

## Install & Build

```sh
git clone https://github.com/opencv/opencv
git clone https://github.com/opencv/opencv_contrib

cd opencv
mkdir build
cd build
cmake -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules -DWITH_CUDA=ON -DCUDA_FAST_MATH=1 -DBUILD_EXAMPLES=ON  -DBUILD_opencv_python3=ON -DPYTHON3_INCLUDE_DIR2=/usr/include/python3.6m -DPYTHON3_NUMPY_INCLUDE_DIRS=/usr/lib/python3/dist-packages/numpy/core/include -DCUDA_ARCH_BIN="5.3" -DCUDA_ARCH_PTX=""  -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DBUILD_EXAMPLES=OFF ..
make -j{NUM_CORE}
sudo make install
```

## Check

```sh
opencv_version
```

## Link

- [JetsonHacks](https://www.jetsonhacks.com/2019/11/22/opencv-4-cuda-on-jetson-nano/)

# RPi Camera

Jetson 제품군은 보통 MIPI-CSI 카메라를 지원한다.
`MIPI(Mobile Industry Processor Interface)`
`CSI(Camera Serial Interface)`

> MIPI
> : 모바일 기기의 내부 인터페이스. 프로세서와 주변 장치들 사이의 HW와 SW를 연결하는 Serial Interface 규격
> - 고속의 디지털 Serial Interface로, 아날로그 Interface에 비해 적용하기 쉽다.
> - 배터리 소모량을 줄이고 높은 대역폭을 통해 고속의 신호 전송이 가능

> CSI
> : Camera를 Control 하는 Device는 I2C 버스를 사용해 카메라를 컨트롤하고, 카메라에서 촬영한 이미지는 S-LVDS를 통해 전달 받는다. 

> MIPI CSI-2는 현재 스마트폰 카메라 Interface를 위해 주로 사용하는 방식으로, Protocol Layer로 CSI-2를 사용하고 Physical Layer로는 D-PHY를 사용한다. 이 프로토콜은 Camera와 Host 장치 간의 고속 전송을 위한 것이다. 프로세서에 직접 연결되기 때문에 USB 연결보다 적은 오버헤드를 갖는다. 

Jetson Nano에는 RPi 카메라 호환 Connector가 있고, IMX 219의 장치 드라이버가 설치되어 있어서 카메라만 연결하면 사용 가능하다.
V1 RPi 카메라 모듈은 호환되지 않고 V2 RPi 카메라 모듈만 가능하다.

(이미지 첨부)

`J13` Camera Connector를 오픈하고 리본 케이블을 삽입한 후 Connector를 닫는다.
파란색 면티 바깥쪽을 향해 있어야 한다.

- Check camera connection

```sh
ls -al /dev/video0
```

```sh
crw-rw----+ 1 root video 81, 0  4월 18 13:43 /dev/video0
```

장치가 연결 됐는지 확인 할 수 있다. 나의 경우에는 연결 후 바로 인식이 되진 않고 5분 정도 기다린 후에야 인식이 됐다.

- GStreamer Test

```sh
gst-launch-1.0 nvarguscamerasrc ! nvoverlaysink
```

```sh
Setting pipeline to PAUSED ...
Pipeline is live and does not need PREROLL ...
Setting pipeline to PLAYING ...
New clock: GstSystemClock
GST_ARGUS: Creating output stream
CONSUMER: Waiting until producer is connected...
GST_ARGUS: Available Sensor modes :
GST_ARGUS: 3264 x 2464 FR = 21.000000 fps Duration = 47619048 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: 3264 x 1848 FR = 28.000001 fps Duration = 35714284 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: 1920 x 1080 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: 1280 x 720 FR = 59.999999 fps Duration = 16666667 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: 1280 x 720 FR = 120.000005 fps Duration = 8333333 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: Running with following settings:
   Camera index = 0 
   Camera mode  = 2 
   Output Stream W = 1920 H = 1080 
   seconds to Run    = 0 
   Frame Rate = 29.999999 
GST_ARGUS: PowerService: requested_clock_Hz=13608000
GST_ARGUS: Setup Complete, Starting captures for 0 seconds
GST_ARGUS: Starting repeat capture requests.
CONSUMER: Producer has connected; continuing.
^Chandling interrupt.
Interrupt: Stopping pipeline ...
Execution ended after 0:00:23.747806781
Setting pipeline to PAUSED ...
Setting pipeline to READY ...
GST_ARGUS: Cleaning up
CONSUMER: Done Success
GST_ARGUS: Done Success
Setting pipeline to NULL ...
Freeing pipeline ...
GST_ARGUS: 
PowerServiceHwVic::cleanupResources
```

Camera와 Interface 하는데에 GStreamer가 사용된다. 위의 명령어를 실행하면 창에 카메라 이미지가 출력되는 것을 확인할 수 있다.

```sh
gst-launch-1.0 nvarguscamerasrc ! 'video/x-raw(memory:NVMM),width=3820, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=616' ! nvvidconv ! nvegltransform ! nveglglessink -e
```

# RealSense Camera

## Installation

# Notes

## v4l2-ctl

```sh
sudo apt install v4l-utils
```

카메라 드라이버 개발할 때 간단한 제어를 하고 싶을 때 `v4l2-ctl` 사용. 

```sh
v4l2-ctl -d /dev/video0 --list-formats-ext
```

특정 디바이스에 대한 지원 이미지 포맷과 해상도를 확인할 수 있다

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

- [Get-started-jetson-nano-devkit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
- [Kinesis Video Stremas: tips & tricks](https://www.alatortsev.com/2019/10/18/aws-kinesis-video-streams/)
- [Kinesis Video Streams Dev Document](https://docs.aws.amazon.com/ko_kr/kinesisvideostreams/latest/dg/kinesisvideo-dg.pdf)