import pydirectinput as pdi
import pyautogui
import time
import numpy
import cv2
from getBoundingBox import getBoundingBox
import math
from skimage.feature import match_template
from scipy.linalg import eigh
from PIL import Image,ImageShow

#Uses the covariance tracking based on the slides in class. This is VERY slow 
def covarianceSearch(topLeft,template):
    img =pyautogui.screenshot(region= (topLeft[0],topLeft[1]+80,640,320))
    processedImage = numpy.asarray(img)
    processedTemplate = numpy.asarray(template)
    
    templateHeight, templateWidth,depth = numpy.shape(processedTemplate)
    #first build template model
    templateModel = buildModel(processedTemplate)
    
    #search all possible patches, from top corner to side - height or side -width to account for template size
    #look for smallest distance
    
    smallestDistance = 1000000000000
    smallestX = -1
    smallestY = -1
    
    for y in range(0,320-templateHeight):
        for x in range(0,639-templateWidth):
            print(x)
            print(y)
            patch = processedImage[y:y+templateHeight,x:x+templateWidth,:]
            patchModel = buildModel(patch)
            distance = Distance(templateModel,patchModel)
            if distance<smallestDistance:
                smallestDistance = distance
                smallestX = x
                smallestY = y
                print(smallestX)
                print(smallestY)


    return smallestX,smallestY

#builds the model by taking in the processedImage array and using the x, y and 
def buildModel(processedImage):

    imgHeight, imgWidth, depth = numpy.shape(processedImage)

    meanX = imgWidth/2
    meanY = imgHeight/2
    meanRed = math.floor(numpy.mean(processedImage[:,:,0]))
    meanGreen = math.floor(numpy.mean(processedImage[:,:,1]))
    meanBlue = math.floor(numpy.mean(processedImage[:,:,2]))

    means = numpy.array([meanX,meanY,meanRed,meanGreen,meanBlue])

    model = numpy.zeros((5,5))

    for y in range(imgHeight):
        for x in range(imgWidth):
            
            featureRed = processedImage[y,x,0]
            featureGreen = processedImage[y,x,1]
            featureBlue = processedImage[y,x,2]
            feature = numpy.array([x,y,featureRed,featureGreen,featureBlue])
            
            firstPart = feature-means
            secondPart = numpy.transpose(firstPart)
            model = model + numpy.multiply(secondPart,firstPart)


    model = model / (imgHeight*imgWidth)

    return model

#Computes distance metric between model and candidate using Riemannian Manifold discussed in class
def Distance(CModel,CCandidate):
    distance = 0
    #print("template")
    #print(CModel)
    #print("patch")
    #print(CCandidate)
    try:
        eigenvalues,eigenvectors = eigh(CModel,CCandidate,eigvals_only=False)
    except:
        #print("Eigenvalue failure")
        eigenvalues = [1,1,1,1,1]
    

    for eigenvalue in eigenvalues:
        output = numpy.log(eigenvalue)
        output = numpy.square(output)
        output = numpy.sqrt(output)
        distance = distance + output


    return distance




#Uses Normalized Cross Correlation Template Matching from Scikit Image library
#https://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.match_template
def searchNCC(topLeft,template):
    img =pyautogui.screenshot(region= (topLeft[0],topLeft[1]+80,640,320))
    processedImage = numpy.asarray(img)
    processedTemplate = numpy.asarray(template)
    result = match_template(processedImage,processedTemplate)
    #thresholds result to see if there is something there
    x = -1 
    y = -1
    if(numpy.amax(result)>.6):
        ind = numpy.unravel_index(numpy.argmax(result, axis=None), result.shape)
        #location of best match
        x = ind[1]
        y = ind[0]+80
    
    return x,y
    

#search function based on color
def searchColor(topLeft):
    #get screenshot, remove miscellanious game info from top bar which equates to 80 pixels. (hense +80 and 400-80 = 320)
    img =pyautogui.screenshot(region= (topLeft[0],topLeft[1]+80,640,320))
    processedImage = numpy.asarray(img)
    #scan for color, which for us is red (r>100,g<50,b<50)
    red = processedImage[:,:,1]
    
    found = False
    for x in range(640):
        
        for y in range (320):
            
            #if red is found to be high (>100)
            if(processedImage[y,x,0] >= 100):
                #if green is found to be low
                if(processedImage[y,x,1] <= 50):
                    #if blue is found to be low
                    if(processedImage[y,x,2] <= 50):
                        print("FOUND ")
                        print("Color being processed")
                        print(processedImage[y,x,:])
                        found = True
                        return x,y+80
    print('Couldnt Find Anything, returning -1,-1')
    return -1,-1





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
    pdi.keyUp('end')



#starts by getting the box of where the game is
template = Image.open('FlagTemplate.png')
topLeft = getBoundingBox()
print("5 seconds before aiming and shooting.")
time.sleep(5)

while(True):
    time.sleep(.25)
    x,y = searchColor(topLeft)
    #x,y = searchNCC(topLeft,template)
    #x,y = covarianceSearch(topLeft,template)
    if(x>=0 and y>=0):
        print(x)
        print(y)
        moveAim(x,y)
        shoot()