import sys
import cv2
import numpy as np
import tensorflow as tf

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
EMOTIONS = ["afraid","angry","disgust","happy","neutral","sad","surprised"]
emotion = {
    '0' : 'Afraid',
    '1' : 'Angry',
    '2' : 'Disgust',
    '3' : 'Happy',
    '4' : 'Neutral',
    '5' : 'Sad',
    '6' : 'Surprise'
}
def prepare(ima):
    IMG_SIZE = 48        # image size
    img_array = cv2.cvtColor(ima,cv2.COLOR_BGR2GRAY)
    img_array=img_array/255.0  
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing
    return new_array.reshape(-1,IMG_SIZE, IMG_SIZE,1)

model = tf.keras.models.load_model("6")
def det(directory):
    image = cv2.imread(directory)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face  = cascade.detectMultiScale(gray, 1.3, 8)
    for (x, y, w, h) in face:
        roi = image[y:y+h, x:x+w]
    prediction = (model.predict([prepare(roi)]))
    preds = prediction[0]
    cv2.imshow('Detected Face', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    print(preds)
    return preds

