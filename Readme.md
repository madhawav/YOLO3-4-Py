# YOLO3-4-Py
[![PyPI Badge](https://img.shields.io/badge/PyPI-0.1.0rc10-blue.svg)](https://pypi.org/project/yolo34py)
[![PyPI Badge](https://img.shields.io/badge/PyPI-0.1.0rc10--gpu-blue.svg)](https://pypi.org/project/yolo34py-gpu)

A Python wrapper on [Darknet](https://github.com/pjreddie/darknet). Compatible with latest [YOLO V3](https://pjreddie.com/darknet/yolo).

![OutputImage](doc/output.jpg)
Image source: http://absfreepic.com/free-photos/download/crowded-cars-on-street-4032x2272_48736.html

## Pre-requisites
1) Python 3.5
2) Numpy, cython and pkgconfig `pip3 install numpy cython pkgconfig`
3) Optionally, OpenCV 3.x with Python bindings. (Tested on OpenCV 3.4.0)
    - You can use [this script](tools/install_opencv34.sh) to automate Open CV 3.4 installation (Tested on Ubuntu 16.04).
    - It is possible to compile YOLO3-4-Py without OpenCV. (Performance of this approach is less.)
```
NOTE: OpenCV 3.4.1 has a bug which causes Darknet to fail. Therefore this wrapper would not work with OpenCV 3.4.1.
More details are available at https://github.com/pjreddie/darknet/issues/502
```

```
NOTE: It is possible to build yolo3-4-py without OpenCV by setting the environment variable OPENCV=0.
```
## How to run using docker?
1) Navigate to [docker](/docker) directory.
2) Copy sample images into the `input` directory. Or else run [input/download_sample_images.sh](docker/input/download_sample_images.sh)
3) Run `sh run.sh`
4) Observe the outputs generated in `output` directory.


## How to run in local machine?
1) Download [darknet](https://github.com/pjreddie/darknet) and compile with OpenCV enabled.
    - Open Makefile of darknet and set OPENCV=1. Then run make.
2) Set environment variable DARKNET_HOME to download location of darknet.
3) Add DARKNET_HOME to LD_LIBRARY_PATH. `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DARKNET_HOME`
4) Run `python3 setup.py build_ext --inplace`
5) Download "yolov3" model file and config files using `sh download_models.sh`.
6) Run `python3 webcam_test.py` or `python3 test.py`

