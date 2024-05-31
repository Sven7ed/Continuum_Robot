import cv2

import time

import cvzone

from ultralytics import YOLO

from roboflow import Roboflow

rf = Roboflow(api_key="nbpM6kM1XQhfZCfHNNYZ")

project = rf.workspace("custom-dataset-or7cw").project("pipeline-investigation")

version = project.version(2)

dataset = version.download("yolov8")

model = YOLO("E:\textbackslash{}PycharmProjects\textbackslash{}pythonProject1\textbackslash{}yolov8n.pt")

my_file = open("E:\textbackslash{}PycharmProjects\textbackslash{}PycharmProjects\textbackslash{}pythonProject2\textbackslash{}README.dataset.txt","r")

print(my_file)

df = my_file.read()

classNames = df.split("\textbackslash{}n")

frame = cv2.VideoCapture(0)

prev_frame_time = 0

while True:

ret, cam = frame.read()

if not ret:

break

  59

result = model.predict(source=cam)

 for r in result:

boxes = r.boxes

for box in boxes:

x1, y1, x2, y2 = box.xyxy[0]

x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

w, h = x2 - x1, y2 - y1

cvzone.cornerRect(cam, (x1, y1, w, h), l=9, rt=5)

con = box.conf[0].item()

cls_names = int(box.cls[0].item())

current_class = classNames[cls_names]

cvzone.putTextRect(cam, f'Features: {current_class}', (max(0, x1), max(35, y1)),

scale=2, thickness=3, offset=10)

new_frame_time = time.time()

fps = 1 / (new_frame_time - prev_frame_time)

prev_frame_time = new_frame_time

print("FPS: ", int(fps))

cv2.imshow("Object Detection", cam)

key = cv2.waitKey(1)

if key == ord("q"):

break

frame.release()

cv2.destroyAllWindows()
