# YOLO3-4-Py
A Python wrapper on [Darknet](https://github.com/pjreddie/darknet). Compatible with latest [YOLO V3](https://pjreddie.com/darknet/yolo).

![OutputImage](doc/output.jpg)
Image source: http://absfreepic.com/free-photos/download/crowded-cars-on-street-4032x2272_48736.html


* __Current Branch__: _direct-numpy-to-darknet-image-conversion._ Use master branch for stable code.
   - This branch removes dependency with Open CV.
   - No need to compile darknet with Open CV enabled.
   - This branch undertakes direct conversion from numpy array to darknet image. (Does not convert through OpenCV Matrix/Image classes). 
   - Currently, efficiency is less than indirect conversion (Direct conversion takes more time than the indirect conversion in master branch).

## Pre-requisites
1) Python 3.5
2) Numpy, cython and pkgconfig `pip3 install numpy cython pkgconfig`

## How to run in local machine?
1) Download [darknet](https://github.com/pjreddie/darknet) and compile.
2) Set environment variable DARKNET_HOME to download location of darknet.
3) Add DARKNET_HOME to LD_LIBRARY_PATH. `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DARKNET_HOME`
4) Run `python3 setup.py build_ext --inplace`
5) Download "yolov3" model file and config files using `sh download_models.sh`.
6) Run `python3 webcam_test.py` or `python3 test.py`

