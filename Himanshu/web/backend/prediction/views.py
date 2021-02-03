from django.shortcuts import render
import cv2
import threading
# Create your views here.
def home(request):
    return render(request, 'index.html', {})


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
        


cam = VideoCapture()


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame \r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
              


# I am following code from here https://stackoverflow.com/questions/49680152/opencv-live-stream-from-camera-in-django-webpage
# to implement a webcam


