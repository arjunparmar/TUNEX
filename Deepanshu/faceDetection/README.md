# Face Detection using OpenCV python library
### There are three files in this folder `faceD_basic.py`, `faceD_webCam.py` and `faceD_adv.py`
> faceD_basic.py
#### Simple Face Detection on a given image file.
> faceD_webCam.py
#### Face Detetion on live video throuh Web Cam.
> faceD_adv.py
#### Face, Eyes and Smile Detection on an image, where image file is passed through the argument.
#
#
#
### These are some of the Prolems occured, Doubts, Limitations, etc. got during these implementations :

# 1.
While using the function **detecMultiScale()**, variying the input parameters **ScaleFactor** and **minNeighbours** gave very different and interestin results:
* In these cases, setting the value of **ScaleFactor** to low (about 1.2 to 1.4) and **minNeighbours** to relatively high (above 4 or 5) gives good results.
* Keeping both low (i.e., **ScaleFactor** <= 1.2, **minNeighour** <= 2 or 3) will output other parts of the image too.
* Keepin both very high does not give any highlighted output.
* Abnormality also occurs at some other combination of values.
##### To check: Is there any particular defined ratio of both of those values that we should use, inorder to get desired output? Or this changes for diferent cases?

### Got solution on: [towardsdatascience](https://towardsdatascience.com/computer-vision-detecting-objects-using-haar-cascade-classifier-4585472829a9) (step 3, under section 1-Face Detection)


# 2.
Here there are 3 files.
**deeps_1.jpeg** is side-faced, whereas **deeps_2.jpeg** and **deeps_3.jpeg** are front-faced.
The codes used above cannot detect the face in **deeps_1.jpeg** or any side-faced image and also face goes to side in videos, as the haarcascade file used here can only detect frontal-face.

# 3.
**waitKey()** function caused a lot of problem.
* First, it was mistakenly placed out of while loop and thus caused errors.
###### Fixed that later on, after realising.
* Secondly, video ran on loop even after closin it multiple times.
###### Then I did set the values to 27, 32 and 13, which are the values for "Esc", "Space" and "Enter" respectively.
