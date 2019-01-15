from pydarknet import Detector, Image
import cv2
import os
import time

if __name__ == "__main__":
    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0, bytes("cfg/coco.data",encoding="utf-8"))

    input_files = os.listdir("input")
    for file_name in input_files:
        if not file_name.lower().endswith(".jpg"):
            continue

        print("File:", file_name)
        img = cv2.imread(os.path.join("input",file_name))
        img2 = Image(img)

        start_time = time.time()
        results = net.detect(img2)
        end_time = time.time()
        print(results)
        print("Elapsed Time:", end_time-start_time)

        for cat, score, bounds in results:
            x, y, w, h = bounds
            cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
            cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_DUPLEX,4,(0,0,255), thickness=2)

        cv2.imwrite(os.path.join("output",file_name), img)
        print()
