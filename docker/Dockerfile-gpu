FROM nvidia/cuda:9.0-cudnn7-devel

## Pyton installation ##
RUN apt-get update && apt-get install -y python3.5 python3-pip git

## OpenCV 3.4 Installation ##
RUN apt-get install -y build-essential cmake
RUN apt-get install -y qt5-default libvtk6-dev
RUN apt-get install -y zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libjasper-dev libopenexr-dev libgdal-dev
RUN apt-get install -y libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev
RUN apt-get install -y python-dev python-tk python-numpy python3-dev python3-tk python3-numpy
RUN apt-get install -y unzip wget
RUN wget https://github.com/opencv/opencv/archive/3.4.0.zip
RUN unzip 3.4.0.zip
RUN rm 3.4.0.zip
WORKDIR /opencv-3.4.0
RUN mkdir build
WORKDIR /opencv-3.4.0/build
RUN cmake -DBUILD_EXAMPLES=OFF ..
RUN make -j4
RUN make install
RUN ldconfig


## Downloading and compiling darknet ##
WORKDIR /
RUN apt-get install -y git
RUN git clone https://github.com/pjreddie/darknet.git
WORKDIR /darknet
RUN sed -i '/GPU=0/c\GPU=1' Makefile
RUN sed -i '/OPENCV=0/c\OPENCV=1' Makefile
RUN make
ENV DARKNET_HOME /darknet
ENV LD_LIBRARY_PATH /darknet

## Download and compile YOLO3-4-Py ##
WORKDIR /
RUN git clone https://github.com/madhawav/YOLO3-4-Py.git
WORKDIR /YOLO3-4-Py
RUN apt-get install -y pkg-config
RUN pip3 install pkgconfig cython numpy
ENV GPU 1
ENV OPENCV 1
RUN python3 setup.py build_ext --inplace

## Download Models ##
ADD ./download_models.sh /YOLO3-4-Py/download_models.sh
RUN sh download_models.sh

## Run test ##
ADD ./docker_demo.py /YOLO3-4-Py/docker_demo.py
CMD ["python3", "docker_demo.py"]