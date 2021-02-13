# Django related libs
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.core.files.base import ContentFile
from django.core.files import File


#libraries existing in the project
from .models import Image
from .forms import ImageForm, TempForm
from backend.settings import BASE_DIR

# Standard Libraries
import os
import threading
import io

# 3rd Party Libraries
import cv2
import PIL
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model



#Constants
IMG_SIZE = 48
EMOTIONS = ["afraid", "angry", "disgust", "happy", "neutral", "sad", "surprised"]
HF = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Views

def home(request):
    '''
    Home view manages the first page of the website
    '''
    return render(request, 'index.html', {})


def predict(request):
    '''
    The Heart of the project,
    From here the user will be able to ask for recommendation
    '''
    return render(request, 'predict.html', {})


def prepare(img):
    SIZE = 48        # image size
    img_array = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_array=img_array/255.0  
    new_array = cv2.resize(img_array, (SIZE, SIZE))  # resize image to match model's expected sizing
    return new_array.reshape(-1,SIZE, SIZE,1)


def predict_image(image_array, category, name_image):
    try:
        print('Inside predict_image shape: {}'.format(image_array.shape))
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        img = image_array.copy()
        faces = HF.detectMultiScale(gray, 1.3, 8)
        try:
            faces = sorted(faces, reverse=True, key = lambda x: (x[2]-x[0]) *(x[3]-x[1]))[0]
            (x,y,w,h)=faces
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(220,40,50),2)
            roi = img[y:y+h, x:x+w]
            model_path = os.path.join(BASE_DIR, '6/')
            model=load_model(model_path, compile=False)
            print('Image shape is {}'.format(img.shape))
            prediction = model.predict([prepare(roi)])
            preds = prediction[0]
            label = EMOTIONS[preds.argmax()]
            cv2.rectangle(img,(x,y+h+10),(x+w,y+h+70),(220,40,50),-2)
            cv2.putText(img,label, (x+10, y+h+50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (225, 225, 225), 3)
        except:
            print("Something happened during prediction")
        _, buffer_img = cv2.imencode('.jpeg', img)
        f_img = buffer_img.tobytes()
        f1 = ContentFile(f_img)
        image_file = File(f1, name=name_image)
        return image_file, label
    except Exception as e:
        print(e)







def form_view(request):
    flag = 0
    context_dict = {}
    upload_image = Image()
    modified_image = Image()
    temp_form = TempForm({'recommend': 'no'})
    image_form = ImageForm()
    if request.method=="POST":
        temp_form = TempForm(request.POST)
        t_value=request.POST.get('recommend')

        if t_value == 'yes':
            print("YEs it is happening")
            img_obj = Image.objects.filter().order_by('-id')[0]
            print("image object = {}".format(img_obj))
            print("image object image = {}".format(img_obj.uploads))
            category = img_obj.category
            name_image = img_obj.uploads.name
            print(name_image)
            print(type(img_obj))
            print('retrieved')
            test_image = img_obj.uploads
            image_bytes = test_image.reads()
            target_image = PIL.Image.open(io.BytesIO(image_bytes))
            target_image = target_image.resize((IMG_SIZE, IMG_SIZE), PIL.Image.ANTIALIAS)
            print(type(target_image))
            image_array = np.array(target_image)
            image_file, x1 = predict_image(image_array, category, name_image)
            print('Image_file type: {}'.format(type(image_file)))
            modified_image.uploads = img_obj.uploads
            print("next step")
            modified_image.save()
            context_dict = {'form': image_form, 'temp_form': temp_form, 'prediction': x1, 'image_show': modified_image}
        else:
            image_form = ImageForm(request.POST, request.FILES) 
            if image_form.is_valid():
                print('inside form.valid function')
                category = image_form.cleaned_data['category']
                if request.FILES.get("uploads", None) is not None:
                    print("image prese")
                    test_image = request.FILES["uploads"]
                    image_byte = test_image.read()
                    target_image = PIL.Image.open(io.BytesIO(image_byte))
                    name_image = image_form.cleaned_data['uploads'].name
                    flag = 1
                    if 'uploads' in request.FILES:
                        print('inside function')
                        upload_image.category = image_form.cleaned_data['category']
                        upload_image.uploads = request.FILES['uploads']
                        upload_image.save()
                        print('Saved image -> {}'.format(upload_image.uploads.name))
                        upload_obj = Image.objects.filter().order_by('-id')[0]
                        image_id = upload_obj.id
                        print("Upload obj is {} ".format(upload_obj))

                        print("image id = {}".format(image_id))
                        print("Image show is {} and type is {} and URL is {} ".format(upload_image.uploads, type(upload_image), upload_image.uploads.url))
                        context_dict = {'form': image_form, 'temp_form': temp_form, 'image_show': upload_image }
                else:
                    print("These are image errors")
                    print(image_form.errors)

    else:
        image_form = ImageForm()
        context_dict = {'form': image_form, 'temp_form': temp_form}
        print(context_dict)
    print("This is the last step")
    print("Context dict is {}".format(context_dict))
    return render(request, 'statRes.html', context=context_dict)


    




def capture_from_cam():
    cap = cv2.VideoCapture(0)
    currentFrame = 0
    while True:

        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)
        currentFrame += 1
    print("The function is over")

class VideoCapture(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.read) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image )
        return jpeg.tobytes()

    
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
        


#cam = VideoCapture()


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame \r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
              


# I am following code from here https://stackoverflow.com/questions/49680152/opencv-live-stream-from-camera-in-django-webpage
# to implement a webcam


def livefe(request):
    try:
        return StreamingHttpResponse(capture_from_cam())
    
    except:
        print("Error occured")
