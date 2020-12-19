import sys
import cv2
import numpy as np

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

capture = cv2.VideoCapture(0)

while capture.isOpened():

    check, image = capture.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face  = cascade.detectMultiScale(gray, 1.3, 8)

    for (x, y, w, h) in face:
        cv2.rectangle(image, (x, y), ((x + w), (y + h)), (110, 240, 4), 3)

    cv2.imshow('WebCam Face', image)

    if cv2.waitKey(1) in {27, 32, 13}:
        break

capture.release()
cv2.destroyAllWindows()
