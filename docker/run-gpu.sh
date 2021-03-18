#!/usr/bin/env bash
# We assume the input images are at the ./input directory.

# Make output directory
mkdir output

# Build the docker image
docker build -t yolo34py-gpu -f Dockerfile-gpu .

# Run the docker image.
nvidia-docker run --rm -it --name yolo34py-gpu -v `pwd`/input:/YOLO3-4-Py/input -v `pwd`/output:/YOLO3-4-Py/output yolo34py-gpu
