#!/usr/bin/env bash
# Make output directory
mkdir output

docker build -t yolo34py-gpu -f Dockerfile-gpu .

# nvidia-docker run --rm -it --name yolo34py-gpu -v `pwd`/input:/YOLO3-4-Py/input -v `pwd`/output:/YOLO3-4-Py/output yolo34py-gpu
docker run --runtime=nvidia -it --name yolo34py-gpu \
    --privileged -e DISPLAY="$DISPLAY" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$(pwd)"/input:/YOLO3-4-Py/input -v "$(pwd)"/output:/YOLO3-4-Py/output yolo34py-gpu
