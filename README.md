# TUNEX

⇥To build a deploy-able system that detects our emotions at real time using webcam feed and smartly classifies one’s playlist into genres, at last playing a song that suits the current emotion and behavior of the person, as specified by the facial analysis.

## Timeline


## Errors Faced
1. In HaarCascade to detect face, we have to import a xml file which is already present in OpenCV, but when I was doing
```python
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#The above xml file was not detected
#maybe because it was not stored in bin of OpenCV as I had installed opencv in miniconda environment

```
   To overcome it, I did [this](https://github.com/arjunparmar/TUNEX/blob/main/Himanshu/faceDet.py#L4)  

2. Installing DLib without Pycharm environment:
   using ```pip install dlib``` give errors because several other packages are required before using this command. To know more refer [this](https://www.pyimagesearch.com/2017/03/27/how-to-install-dlib/?fbclid=IwAR1h_ZFwcqXMdE8zGgrVYcgwH1RntRNe0_Nw1dsJw6K7chn7sZ6aDTUhskQ)

3. While arranging the files in the KDEF dataset, You may encounter a key error on Images 'AF31V.JPG' and 'AM31H.JPG'. The reason for the same is we have seven emotions that are thoroughly documented these two images or least their names do not qualify to our expectations and hence can be removed prior to running this [script](https://github.com/arjunparmar/TUNEX/blob/main/Gaurav/arranging_data.py) or [this](https://github.com/arjunparmar/TUNEX/blob/main/Gaurav/reading_data.py).

