import pydirectinput as pdi
import pyautogui
import time
from getBoundingBox import getBoundingBox

#first get the bounding box
#topLeft = getBoundingBox()

#print("you have 5 seconds before calibration starts")
time.sleep(5)

# Aim Down Sight and wait a sec for it to aim
pdi.keyDown('end')

time.sleep(1)
#save a screenshot
#pyautogui.screenshot('test.png',region= (topLeft[0],topLeft[1],640,400))

for i in range(13):
    pdi.press('right')

for i in range(8):
    pdi.press('up')
