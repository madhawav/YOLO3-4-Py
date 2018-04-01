#!/usr/bin/env bash

echo "Downloading config files..."

mkdir cfg
wget -O cfg/coco.data https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/coco.data
wget -O cfg/yolov3.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg

mkdir data
wget -O data/coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names

echo "Downloading yolov3 weights"
mkdir weights
wget -O weights/yolov3.weights https://pjreddie.com/media/files/yolov3.weights