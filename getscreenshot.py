import pydirectinput as pdi
import pyautogui
import time
from getBoundingBox import getBoundingBox
import cv2
import numpy
from PIL import Image,ImageShow

#first get the bounding box
topLeft = getBoundingBox()

img =pyautogui.screenshot(region= (topLeft[0],topLeft[1],640,400))
processedImage = numpy.asarray(img)
print(processedImage.ndim)
print(processedImage.shape)
print(processedImage.size)
print(processedImage[0,0,:])
#PIL.ImageShow.show(img)

newIm = Image.fromarray(processedImage)
ImageShow.show(newIm)