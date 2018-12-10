# *monica* - MinION Open Nucleotide Identifier for Continuous Analysis 
[![Build Status](https://travis-ci.com/bioinformagic/monica.svg?branch=master)](https://travis-ci.com/bioinformagic/monica)

an open source pathogen identifier for real-time analysis on MinION output







Edit the `build.sh` to choose between CPU or GPU

```
# Build the Docker image
docker-compose build

# Set env variables for TensoFlow CPU 
export PYTHON_VERSION=3.6
export TF_VERSION_GIT_TAG=v1.9.0
export USE_GPU=0

# Set env variables for TensoFlow GPU
export PYTHON_VERSION=3.6
export TF_VERSION_GIT_TAG=v1.9.0
export USE_GPU=1
export CUDA_VERSION=9.1
export CUDNN_VERSION=7.1

# Start container
docker-compose run tf

# You can also do:
# docker-compose run tf bash
# bash build.sh
```

Note: The CPU works well when tested. Subprocess + others have too be added though. The GPU has to be tested.

---

