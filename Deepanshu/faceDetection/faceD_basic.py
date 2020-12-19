import sys
import cv2
import numpy as np

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

image = cv2.imread("deeps_2.jpeg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
face  = cascade.detectMultiScale(gray, 1.3, 8)

for (x, y, w, h) in face:
    cv2.rectangle(image, (x, y), ((x + w), (y + h)), (110, 240, 4), 5)

cv2.imshow('Detected Face', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
