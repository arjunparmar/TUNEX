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
import random
import json

# 3rd party libraries
import cv2
import requests as rq
import PIL
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


#Constants
IMG_SIZE = 48
EMOTIONS = ["afraid", "angry", "disgust", "happy", "neutral", "sad", "surprised"]

HF_PATH = 'haarcascade_frontalface_default.xml'
BASE_URL = "https://api.spotify.com/v1/recommendations"
MARKET = "IN" #market from which songs are recommended
SA = "4NHQUGzhtTLFvgF5SZesLK" #seed artist for spotify (this is not a constant will update as per the genre)
SA_D = {"hiphop": "7dGJo4pcD2V6oG8kP0tJRR", # eminem
        "rock": "31hrPUMBg96szrqNAb3oqP", # blacklite district
        "country": "1UTPBmNbXNTittyMJrNkvw", # Blake Shelton
        "pop": "5IH6FPUwQTxPSXurCrcIov", # alec benjamin
        "metal": "2ye2Wgw4gimLv2eAKyk1NB", # metallica
        "disco": "4tZwfgrHOc3mvqYlEYSvVi", # daft punk
        "reggae": "6BH2lormtpjy3X9DyrGHVj", # bob marley
        "jazz": "1Mxqyy3pSjf8kZZL4QVxS0", # frank sinatra
        "bollywoodpop": "6CXEwIaXYfVJ84biCxqc9k", # vishal dadlani
        "classical": "3WrFJ7ztbogyGnTHbHJFl2", # beatles
        "blues": "3WrFJ7ztbogyGnTHbHJFl2", #B. B king
        }
ST = "0c6xIDDpzE81m2q797ordA" #seed track for spotify
ST_D = {
    "hiphop": "7MJQ9Nfxzh8LPZ9e9u68Fq",
    "jazz": "0elmUoU7eMPwZX1Mw1MnQo",
    "rock": "1DWiVxo482tHbgTWKHMWqg",
    "metal": "1hKdDCpiI9mqz1jVHRKG0E",
    "country": "0cB74Rrq9gKE5iUjwG9raA",
    "reggae": "4dbaWokGcqEWvwTZDBbMD3",
    "disco": "2cGxRwrMyEAp8dEbuZaVv6",
    "pop": "1xQ6trAsedVPCdbtDAmk0c",
    "classical": "7pKfPomDEeI4TPT6EOYjn9",
    "blues": "3cg0dJfrQB66Qf2YthPb6G"
}
TOKEN = "BQBUBVI6ndX-R2t70WMCz3H1kjFNY7Pih0e9wg4kyjW-k-V3kHAlTIxxneT3CiM9-zXakDi9-qFk3YLkMspWbtWZ1NttlcZo6pvebJJZvMQMZkXovgHgenlqWADoLdkEZer_MFsgu3wV9fqFjvi4rNd7-x0IWYyYWyI"
HEADER = {
    "content-Type": "application/json"
}
HEADER["authorization"] = "Bearer "+TOKEN

res = ""  #result that we will pass to the result page



try:

    HF = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
except Exception as e:
    print("HF error is {}".format(e))

model_path = os.path.join(settings.BASE_DIR, '6')
model=load_model(model_path, compile=False)

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

def predict_video(image_array, name_image):
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

        
        # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        _, buffer_img = cv2.imencode('.jpeg', img)
        f_img = buffer_img.tobytes()
        f1 = ContentFile(f_img)
        image_file = File(f1, name=name_image)
        res = label
        print("This is res -> {}".format(res))
        return img, label
    except Exception as e:
        print(e)




def process_json(json):
    artists_l = []
    songs = []
    urls = []
    s_images = []
    inde = []
    counter = 0
    # print(json.keys())
    for entry in json:
        #print("entry is {}".format(entry))
        #print("keys of album are {}".format(entry.keys()))
        print(entry["artists"][0].keys())
        if entry["preview_url"] != None: 
            artists_l.append(entry["artists"][0]["name"])
            songs.append(entry["name"])
            urls.append(entry["preview_url"])
            s_images.append(entry["album"]["images"][0]["url"])
            inde.append(counter)
            counter = counter + 1
    print("artists are {} songs are {} and urls are {}".format(artists_l, songs, urls))
    return zip(inde, artists_l, songs, urls, s_images)

        

def form(request):
    modified_image = Image()
    result_dic = {}
    genre=""
    img=""

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
            genre = egmap(x1)
            print("genre is {}".format(genre))
            if genre != '':
                SA = SA_D[genre]
                ST = ST_D[genre]
            url = BASE_URL+'?limit=14&market='+MARKET+'&seed_artists='+SA+'&seed_genres='+genre+'&seed_tracks='+ST
            r = rq.get(url, headers=HEADER)
            print(r.status_code)
            if r.json():
                json_text = json.loads(r.text)
                # print(json_text)
                result_dic = process_json(json_text["tracks"])
            else:
                print("Bad Request")
            
            print("result is {}".format(result_dic))

            return render(request, "predict.html", {"obj":obj, "prediction":x1, "modified_image":modified_image, "result_dic": result_dic})
        
    
    else:
        form = ImageForm()
        print("It came into else")
        img = Image.objects.last()
        print("Image is {}".format(img))

    return render(request, "predict.html", {"img":img,"form":form})

def egmap(emotionout):
    '''
    link between genre and emotion
    '''
    print("emotionout is {}".format(emotionout))
    genrechosen=""
    afraidlist = ["hiphop"]
    angrylist = ["rock", "metal"]
    disgustlist = ["hiphop", "jazz"]
    happylist = ["pop", "disco"]
    neutrallist = ["reggae", "classical"]
    sadlist = ["blues", "classical", "country"]
    surprisedlist = ["disco"]
    
    if emotionout == 'afraid':
        genrechosen = random.choice(afraidlist)
    if emotionout == 'angry':
        genrechosen = random.choice(angrylist)
    if emotionout == 'disgust':
        genrechosen = random.choice(disgustlist)
    if emotionout == 'happy':
        genrechosen = random.choice(happylist)
    if emotionout == 'neutral':
        genrechosen = random.choice(neutrallist)
    if emotionout == 'sad':
        genrechosen = random.choice(sadlist)
    if emotionout == 'surprise':
        genrechosen = random.choice(surprisedlist)
    print("genrechosen is {}".format(genrechosen))
    return genrechosen


cam = VideoCamera()


def gen(camera):
    while True:
        frame = cam.get_frame()
        # print(frame)
        m_image, lab =predict_video(frame, "result")
        print("This is in gen")
        SA = SA_D[lab]
        ST = ST_D[lab]
        print(lab)
        # m_image = cv2.cvtColor(m_image, cv2.COLOR_RGB2BGR)
        ret, m_image = cv2.imencode('.jpg', m_image)
        m_image = m_image.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + m_image + b'\r\n\r\n')


def livefeed(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:  # This is bad! replace it with proper handling
        print(e)

def showlive(request):
    submitb = request.POST.get('submit')
    print(submitb)
    context = {'submitb':submitb} if submitb else {'submitb': None}
    return render(request, 'live.html', context)



def liveres(request):
    print("This is live res")
    genre = egmap(res)
    print("genre is {}".format(genre))
    if genre != '':
        SA = SA_D[genre]
        ST = ST_D[genre]
    url = BASE_URL+'?limit=7&market='+MARKET+'&seed_artists='+SA+'&seed_genres='+genre+'&seed_tracks='+ST
    r = rq.get(url, headers=HEADER)
    print(r.status_code)
    if r.json():
       json_text = json.loads(r.text)
       # print(json_text)
       result_dic = process_json(json_text["tracks"])
    context = {'result_dic': result_dic, 'emotion': res}
    return render(request, 'liveres.html', context)
    
