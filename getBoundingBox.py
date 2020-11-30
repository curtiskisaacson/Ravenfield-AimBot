#This gets the bounding box of the game window

#We will do so by having the user place the cursor over the top left corner
#We know the window size already so we can just create

import pydirectinput as pdi
import pyautogui
import time


def getBoundingBox():
    print("You have 5 seconds to place cursor over top left corner of game window")

    time.sleep(5)

    topLeft = pyautogui.position()
    return topLeft

