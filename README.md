# TUNEX

⇥To build a deploy-able system that detects our emotions at real time using webcam feed and smartly classifies one’s playlist into genres, at last playing a song that suits the current emotion and behavior of the person, as specified by the facial analysis.

## Errors Faced
1. In HaarCascade to detect face, we have to import a xml file which is already present in OpenCV, but when I was doing
```python
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#The above xml file was not detected
#maybe because it was not stored in bin of OpenCV as I had installed opencv in miniconda environment

```
To overcome this, I did [this](https://github.com/arjunparmar/TUNEX/blob/main/Himanshu/faceDet.py#L4)
