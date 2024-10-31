#!/bin/bash +x

sudo apt install nvidia-cuda-toolkit
nvcc --version
lspci | grep -i nvidia # suporte a cuda

sudo apt install nvidia-driver-440
nvidia-container-toolkit --version

wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-6

nvidia-smi

## inicia nvidia dentro do container
docker run --rm --gpus all ubuntu nvidia-smi

docker run --isolation process --device class/5B45201D-F2F2-4F3B-85BB-30FF1F953599 mcr.microsoft.com/windows:1809