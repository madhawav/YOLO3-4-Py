# PyYOLOV3
A Python wrapper on [Darknet](https://github.com/pjreddie/darknet). Compatible with latest [YOLO V3](https://pjreddie.com/darknet/yolo).

## Pre-requisites
1) Python 3.5
2) Numpy `pip3 install numpy`
3) OpenCV Python `pip3 install opencv-python`

## How to run?
1) Download and compile [darknet](https://github.com/pjreddie/darknet).
2) Set environment variable DARKNET_HOME to download location of darknet.
3) Add DARKNET_HOME to LD_LIBRARY_PATH. `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DARKNET_HOME`
4) Run `python3 setup.py build_ext --inplace`
5) Download "yolov3" model file and config files using `sh download_models.sh`.
6) Run `python3 webcam_test.py` or `python3 test.py`