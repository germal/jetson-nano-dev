# tensorflow

```sh
sudo apt-get install python3-pip
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev
pip3 install -U pip
pip3 install -U numpy grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast h5py astor termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta

# TF-2.x
sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow==2.1.0+nv20.3

# TF-1.15
sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow==1.15.2+nv20.3
```

## Reference
- [nvidia_tensorflow](https://forums.developer.nvidia.com/t/official-tensorflow-for-jetson-nano/71770)

# Pytorch

- torch

```sh
wget https://nvidia.box.com/shared/static/3ibazbiwtkl181n95n9em3wtrca7tdzp.whl -O torch-1.5.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base
pip3 install Cython
pip3 install numpy torch-1.4.0-cp36-cp36m-linux_aarch64.whl
```

```python
import torch
print(torch.__version__)
print('CUDA available: ' + str(torch.cuda.is_available()))
print('cuDNN version: ' + str(torch.backends.cudnn.version()))
```

- torchvision

```
sudo apt-get install libjpeg-dev zlib1g-dev
git clone --branch v0.6.0 https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
cd torchvision
sudo python setup.py install
cd ../  # attempting to load torchvision from build dir will result in import error
```

## Refernece

- [nvidia_pytorch](https://forums.developer.nvidia.com/t/pytorch-for-jetson-nano-version-1-4-0-now-available/72048)
