import numpy as np
import cv2 as cv
import argparse
from PIL import Image, ImageEnhance, ImageDraw 
import matplotlib.pyplot as plt
import os

def ROI(frame):
    #enhancer = ImageEnhance.Contrast(frame)
    #img = enhancer.enhance(0.7)
    face_classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv.cvtColor(np.array(frame), cv.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.1, 5)
    try:
        x, y, w, h = faces[0]
        #print(faces)
    except:
        x,y,w,h = (0,0,0,0)
    return x,y,w,h

def using_cam():
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        x,y,w,h = ROI(frame)
        cv.rectangle(frame, (x,y), (x+w, y+h), (127, 0, 255), 2)
        cv.imshow('ROI', frame)
        if(cv.waitKey(2) == 13 & 0xFF):
            break

    cap.release()
    cv.destroyAllWindows()

def KDEF_data():
    base_dir = 'data/'
    dirs = ['train', 'test', 'validation']

    data_dir = 'cropped/'

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    
    count = 1

    for sub in dirs:
        curr_dir = base_dir + sub
        for i, j, k in os.walk(curr_dir):
            
            for name in k:
                img = Image.open(i+"/"+name)
                x,y,w,h = ROI(img)
                img_2 = np.array(img)
                croped = img_2[y:y+h, x:x+w]
                #resize = cv.resize(Image.fromarray(croped), (500, 500), interpolation=cv.INTER_CUBIC)
                #resize = Image.fromarray(resize)
                #croped = Image.fromarray(croped)
                #croped.save(data_dir+str(count)+'.jpeg','JPEG')
                if croped.shape[0]>0:
                    croped = Image.fromarray(croped)
                    croped.save(data_dir+str(count)+'.jpeg','JPEG')
                count+=1

if __name__ == '__main__':
    #using_cam()
    KDEF_data()