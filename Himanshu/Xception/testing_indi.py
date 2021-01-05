from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np

detect = 'haarcascade_files/haarcascade_frontalface_default.xml'

emo = 'xception/'

face_classi = cv2.CascadeClassifier(detect)
emo_classi = load_model(emo, compile=False)

EMOTIONS=['afraid', 'angry', 'disgust', 'happy', 'neutral', 'sad', 'surprised']

cv2.namedWindow('your_face')

camera = cv2.VideoCapture(1)

while True:
    frame = camera.read()[1]
    frame = imutils.resize(frame, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classi.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)
    colored = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR) #I added this to give model 3 channels
    canvas = np.zeros((250, 300, 3), dtype="uint8")
    frameClone = frame.copy()
    
    if len(faces)>0:
        faces = sorted(faces, reverse=True, key=lambda x:(x[2]-x[0])*(x[3]-x[1]))[0]
        (fX, fY, fW, fH) = faces

        roi = colored[fY:fY+fH, fX:fX+fW]
        roi = cv2.resize(roi, (180,180))
        roi = roi.astype("float")/255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        print("The shape of roi is {}".format(roi.shape))

        preds = emo_classi.predict(roi)[0]
        emo_prob = np.max(preds)
        label = EMOTIONS[preds.argmax()]

    else: continue

    for(i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):

        text = "{}: {:.2f}%".format(emotion, prob*100)

        w = int(prob*300)
        cv2.rectangle(canvas,(7, (i*35)+5), 
                (w, (i*35)+35), (0,0, 255), -1)
        cv2.putText(canvas, text, (10, (i*35)+23), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255), 2)
        cv2.putText(frameClone, label, (fX, fY-10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        cv2.rectangle(frameClone, (fX, fY), (fX+fW, fY+fH), (0, 0, 255), 2)


    cv2.imshow('your_face', frameClone)
    cv2.imshow("Probabilites", canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()






