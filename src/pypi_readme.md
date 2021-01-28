A Python wrapper on [pjreddie's](https://pjreddie.com/) implementation (authors' implementation) of [YOLO V3 Object Detector](https://pjreddie.com/darknet/yolo) on [Darknet](https://github.com/pjreddie/darknet).
Also compatible with other Darknet Object Detection models.

![OutputImage](https://raw.githubusercontent.com/madhawav/YOLO3-4-Py/master/doc/output.jpg)
Image source: http://absfreepic.com/free-photos/download/crowded-cars-on-street-4032x2272_48736.html

# Prerequisites
* Python 3.5+
* Linux x86-64 Operating System
* nVidia CUDA SDK (for GPU version only. Make sure nvcc is available in PATH variable.)

# Sample Usage
Note: This sample code requires OpenCV with python bindings installed. (`pip3 install opencv-python==3.4.0`)

1) Create a directory to host sample code and navigate to it.
2) Download and execute [this script](https://github.com/madhawav/YOLO3-4-Py/blob/master/download_models.sh) to download model files.
3) Create sampleApp.py with following code. Specify SAMPLE_INPUT_IMAGE.
    ```python
    from pydarknet import Detector, Image
    import cv2
    
    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0, bytes("cfg/coco.data",encoding="utf-8"))
    
    img = cv2.imread('SAMPLE_INPUT_IMAGE')
    img_darknet = Image(img)
    
    results = net.detect(img_darknet)
        
    for cat, score, bounds in results:
        x, y, w, h = bounds
        cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
        cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
    
    cv2.imshow("output", img)
    cv2.waitKey(0)
    ```
4) Execute sampleApp.py `python sampleApp.py`.

# Installation
yolo34py comes in 2 variants, _CPU Only Version_ and _GPU Version_. Installation may take a while since it involves downloading and compiling of darknet.

## __CPU Only Version__
This version is configured on darknet compiled with flag GPU = 0.
```bash
pip3 install numpy
pip3 install yolo34py
```

## GPU Version:
This version is configured on darknet compiled with flag GPU = 1.
```bash
pip3 install numpy
pip3 install yolo34py-gpu
```


# More Information
* For more details on yolo34py (This python wrapper):
   - GitHub Repo: https://github.com/madhawav/YOLO3-4-Py
   - This is the place to discuss about issues of yolo34py. 
   - Your contributions are greatly appreciated. 
* For more details on YOLO V3:
   - Website from Authors: https://pjreddie.com/yolo
* For more details on Darknet, the base API wrapped by this library
   - Website: https://pjreddie.com/darknet/
   - GitHub: https://github.com/pjreddie/darknet
   

# License
* yolo34py (this wrapper) is under [Apache License 2.0](https://github.com/madhawav/YOLO3-4-Py/blob/master/LICENSE).
* The version of darknet wrapped by yolo34py is [public domain](https://github.com/madhawav/darknet/blob/master/LICENSE). 