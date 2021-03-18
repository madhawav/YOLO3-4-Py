FROM ubuntu:18.04

## Python installation ##
RUN apt-get update && apt-get install -y python3.6 python3-pip git libgl1-mesa-glx wget && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir --upgrade pip

## Install opencv-python. This is used by the demo script. ##
RUN pip3 install --no-cache-dir opencv-python

## Download and compile YOLO3-4-Py ##
WORKDIR /
RUN git clone https://github.com/madhawav/YOLO3-4-Py.git
WORKDIR /YOLO3-4-Py/src
RUN pip3 install --no-cache-dir cython>=0.29 requests>=2.25 numpy>=1.19
RUN pip3 install .

## Run test ##
WORKDIR /YOLO3-4-Py/
RUN sh tools/download_models.sh
COPY ./docker_demo.py /YOLO3-4-Py/docker_demo.py
CMD ["python3", "docker_demo.py"]
