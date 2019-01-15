#!/usr/bin/env bash
# Make output directory
mkdir output

docker build -t yolo34py-gpu -f Dockerfile-gpu .

nvidia-docker run --rm -it --name yolo34py-gpu -v `pwd`/input:/YOLO3-4-Py/input -v `pwd`/output:/YOLO3-4-Py/output yolo34py-gpu
