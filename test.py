import pydarknet
from pydarknet import Detector, Image
import cv2

if __name__ == "__main__":
    # net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))

    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0, bytes("cfg/coco.data",encoding="utf-8"))

    img = cv2.imread("/home/madhawa/Desktop/CV/darknet/data/dog.jpg")

    img2 = Image(img)

    img2.show_image(bytes("Preview", encoding="utf-8"))

    # r = net.classify(img2)
    r = net.detect(img2)
    print(r)
    # img2 = pydarknet.load_image(img)

    cv2.waitKey(0)