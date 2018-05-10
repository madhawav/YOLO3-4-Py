from io import BytesIO

import PIL.Image
import numpy as np
import requests

from pydarknet import Detector, Image


def test_image():
    r = requests.get("https://raw.githubusercontent.com/madhawav/darknet/master/data/dog.jpg")
    assert r.status_code == 200
    img = PIL.Image.open(BytesIO(r.content))

    img = np.array(img)
    img = img[:,:,::-1] # RGB to BGR

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("cfg/coco.data", encoding="utf-8"))

    img2 = Image(img)

    results = net.detect(img2)

    results_labels = [x[0].decode("utf-8") for x in results]

    assert "bicycle" in results_labels
    assert "dog" in results_labels
    assert "truck" in results_labels
    assert len(results_labels) == 3