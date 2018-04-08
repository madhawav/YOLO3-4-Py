#!/usr/bin/env bash
# Make output directory
mkdir output

# Build the docker image
docker build -t yolo3-4-py .

# Run the docker image
docker run --rm -it --name yolo3-4-py -v `pwd`/input:/YOLO3-4-Py/input -v `pwd`/output:/YOLO3-4-Py/output yolo3-4-py