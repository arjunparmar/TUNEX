import cv2

#Loading the classifier from saved directory

face_cascade = cv2.CascadeClassifier("/home/hp77/miniconda3/envs/tunex/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

while True:

    _, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

        
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    
cap.release()
cv2.destroyAllWindows()
