import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('/home/hp77/miniconda3/envs/tunex/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/hp77/miniconda3/envs/tunex/share/opencv4/haarcascades/haarcascade_eye.xml')
img=cv2.imread('test.jpg')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('test',gray)
cv2.waitKey(0)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

for (x,y,w,h) in faces:
    img = cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0),2)


cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
