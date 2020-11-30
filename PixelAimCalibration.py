import pydirectinput as pdi
import pyautogui
import time
from getBoundingBox import getBoundingBox

#first get the bounding box
topLeft = getBoundingBox()




print("you have 5 seconds before calibration starts")
time.sleep(5)

# Aim Down Sight and wait a sec for it to aim
pdi.keyDown('end')
time.sleep(1)

#Fire first shot
pdi.click()

time.sleep(1)
#one press to the right
for i in range(1):
    pdi.press('right')

time.sleep(1)
#second shot
pdi.click()

time.sleep(1)
#aim up
pdi.keyUp('end')

time.sleep(1)
#save a screenshot
pyautogui.screenshot('calibration.png',region= (topLeft[0],topLeft[1],640,400))

