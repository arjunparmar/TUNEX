# Django libs
from django.shortcuts import render
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files import File
from django.http import StreamingHttpResponse

#Libraries of ourselves
from .form import ImageForm
from .models import Image
from .camera import VideoCamera

# Standard Libraries
import os
import threading
import io

# 3rd party libraries
import cv2
import PIL
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


#Constants
IMG_SIZE = 48
EMOTIONS = ["afraid", "angry", "disgust", "happy", "neutral", "sad", "surprised"]
HF_PATH = 'haarcascade_frontalface_default.xml'
try:

    HF = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
except Exception as e:
    print("HF error is {}".format(e))



# Create your views here.

def home(request):
    return render(request, 'home.html', context={})

def prepare(img):
    img_array = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_array=img_array/255.0  
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize image to match model's expected sizing
    return new_array.reshape(-1,IMG_SIZE, IMG_SIZE,1)



def predict_image(image_array, name_image):
    label="Nothing predicted"
    try:
        print('Inside predict_image shape: {}'.format(image_array.shape))
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        img = image_array.copy()
        #print("img is {}".format(img))
        faces = HF.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        print("faces is {}".format(faces))
        try:
            print("Before faces")
            faces = sorted(faces, reverse=True, key = lambda x: (x[2]-x[0]) *(x[3]-x[1]))[0]
            print("After faces")
            (x,y,w,h)=faces
            print("After coordinatese")  
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(220,40,50),2)
            print("Before roi")
            roi = img[y:y+h, x:x+w]
            print("Afer roi")
            model_path = os.path.join(settings.BASE_DIR, '6/')
            model=load_model(model_path, compile=False)
            print('Image shape is {}'.format(img.shape))
            prediction = model.predict([prepare(roi)])
            
            preds = prediction[0]
            print("prediction is {}".format(preds))
            print("max index is {}".format(preds.argmax()))
            label = EMOTIONS[preds.argmax()]
            print("label is {}".format(label))
            cv2.rectangle(img,(x,y+h+10),(x+w,y+h+70),(220,40,50),-2)
            cv2.putText(img,label, (x+10, y+h+50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (225, 225, 225), 3)
            cv2.imwrite('result.jpeg', img)
        except Exception as e:
            print("Something happened during prediction")
            print(e)

        
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        _, buffer_img = cv2.imencode('.jpeg', img)
        f_img = buffer_img.tobytes()
        f1 = ContentFile(f_img)
        image_file = File(f1, name=name_image)
        return image_file, label
    except Exception as e:
        print(e)



def form(request):
    modified_image = Image()
    if request.method=="POST":
        form=ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            print("Image saved")
            obj=form.instance
            print("obj is {}".format(obj))
            print("returning just obj")
            name_image= obj.image.name
            test_image = obj.image
           # image_bytes = test_image.reads()
            target_image = PIL.Image.open(str(settings.BASE_DIR) + obj.image.url)
            #target_image = target_image.resize((IMG_SIZE, IMG_SIZE), PIL.Image.ANTIALIAS)
            print(type(target_image))
            image_array = np.array(target_image)
            image_file, x1 = predict_image(image_array, name_image)
            print('Image_file type: {}'.format(type(image_file)))
            modified_image.image = image_file
            print("next step")
            modified_image.save()

            return render(request, "predict.html", {"obj":obj, "prediction":x1, "modified_image":modified_image})
        
    
    else:
        form = ImageForm()
        print("It came into else")
        img = Image.objects.last()
        print("Image is {}".format(img))

    return render(request, "predict.html", {"img":img,"form":form})

cam = VideoCamera()


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def livefeed(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:  # This is bad! replace it with proper handling
        print(e)
