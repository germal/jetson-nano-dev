# Realsense Camera

## Installation

```sh
sudo apt-get install git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
sudo apt-get install libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev

git clone git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
mkdir build
cd build
cmake ../ -DBUILD_EXAMPLES=true -DFORCE_LIBUVC=true -DBUILD_WITH_CUDA=true -DCMAKE_BUILD_TYPE=release -DBUILD_PYTHON_BINDINGS=bool:true
make -j{NUM_CPU}
sudo make install

echo "export PYTHONPATH=$PYTHONPATH:/usr/local/lib" >> ~/.bashrc

# copy udev rules so that camera can be from user space
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && udevadm trigger

./scripts/patch-realsense-ubuntu-lts.sh

sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE

sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo bionic main" -u

sudo apt-get install librealsense2-utils
sudo apt-get install librealsense2-dev
```