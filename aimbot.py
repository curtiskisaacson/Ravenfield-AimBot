import pydirectinput as pdi
import pyautogui
import time
from getBoundingBox import getBoundingBox
import math



#search function based on color
def searchColor():
    #get screenshot, remove miscellanious game info from top bar
    img= pyautogui.screenshot('calibration.png',region= (topLeft[0],topLeft[1]+80,640,320))
    #scan for color
    
    # one I hit color, get x,y location of it

    #return x y location of it
    x = 0
    y = 0
    return x,y


def moveAim(TargetX, TargetY):
    #since cursor is at 320,202 of our bounding window
    #and our aim function moves at roughly 22 pixels per click
    # and we know where our Target is

    #Takes the location given, and gives the distance to each pixel location from current cursor 
    moveRelativeX = TargetX - 320
    moveRelativeY = TargetY - 202

    pixelsPerKeyStroke = 23
    #divides by 22 to give the approximate number of key presses to reach target x y
    numberOfXClicks = math.floor(moveRelativeX/pixelsPerKeyStroke)
    numberOfYClicks = math.floor(moveRelativeY/pixelsPerKeyStroke)

    #aim down sight
    pdi.keyDown('end')
    time.sleep(.5)

    #make moves
    if numberOfXClicks<0:
        print('Move Left')
        for i in range(abs(numberOfXClicks)):
            pdi.press('left')

    elif numberOfXClicks>0:
        print('Move Right')
        for i in range(abs(numberOfXClicks)):
            pdi.press('right')

    if numberOfYClicks<0:
        print('Move Up')
        for i in range(abs(numberOfYClicks)):
            pdi.press('up')

    elif numberOfYClicks>0:
        print('Move Down')
        for i in range(abs(numberOfYClicks)):
            pdi.press('down')

    

def shoot():
    pdi.click()



topLeft = getBoundingBox()
print("5 seconds before aiming and shooting")
time.sleep(5)
moveAim(0,0)
shoot()