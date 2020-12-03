import pydirectinput as pdi
import pyautogui
import time
import numpy
import cv2
from getBoundingBox import getBoundingBox
import math
from skimage.feature import match_template
from PIL import Image,ImageShow

#first get the bounding box
topLeft = getBoundingBox()
print("5 seconds before capture")
time.sleep(5)
img =pyautogui.screenshot(region= (topLeft[0],topLeft[1]+80,640,320))
processedImage = numpy.asarray(img)
template = Image.open('FlagTemplate.png')
processedTemplate = numpy.asarray(template)
result = match_template(processedImage,processedTemplate)
print(numpy.amax(result))
ind = numpy.unravel_index(numpy.argmax(result, axis=None), result.shape)
print(ind)
