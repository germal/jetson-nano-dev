# OpenCV

## Requirements

```sh
sudo apt install git cmake libatlas-base-dev gfortran libhdf5-serial-dev hdf5-tools python3-dev
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

# Reference

- [JetsonHacks](https://www.jetsonhacks.com/2019/11/22/opencv-4-cuda-on-jetson-nano/)