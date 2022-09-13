# packages
from ctypes import sizeof
from itertools import count
import cv2
import numpy as np
import os
from os import listdir
from os.path import join

counter = 0


def changeColor(image, color):
    NewImage = np.zeros((image.shape[0], image.shape[1], 4), np.uint8)

    #For adding with instead of transparant
    NewImage.fill(255)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j] == 0:
                NewImage[i][j] = color

    return NewImage

def createCard(image):
    global counter
    card1 = np.zeros((4*image.shape[0],image.shape[1],image.shape[2]), np.uint8)
    
    #For adding with instead of transparant
    card1.fill(255)
    card2 = card1.copy()

    # Creating card with only 1 pattern
    y_offset = round(card1.shape[0] * 0.5 - image.shape[0] * 0.5)
    card1[y_offset:y_offset+image.shape[0], 0:image.shape[1]] = image
    counter = counter+1
    card1CorrectSize = cv2.resize(card1, (0, 0), None, 0.236, 0.1935)
    cv2.imwrite(f"{counter}.png", card1CorrectSize)
    # cv2.imwrite(f"{counter}.png", card1)

    # Creating card with 3 times the pattern
    card3 = card1.copy()
    y_offset = round(card3.shape[0] * (1/4) - image.shape[0] * 0.5)
    card3[y_offset:y_offset+image.shape[0], 0:image.shape[1]] = image

    y_offset = round(card3.shape[0] * (3/4) - image.shape[0] * 0.5)
    card3[y_offset:y_offset+image.shape[0], 0:image.shape[1]] = image
    counter = counter+1
    card3CorrectSize = cv2.resize(card3, (0, 0), None, 0.236, 0.1935)
    cv2.imwrite(f"{counter}.png", card3CorrectSize)
    # cv2.imwrite(f"{counter}.png", card3)

    # Creating card with 2 times the pattern
    y_offset = round(card2.shape[0] * (1/3) - image.shape[0] * 0.5)
    card2[y_offset:y_offset+image.shape[0], 0:image.shape[1]] = image

    y_offset = round(card2.shape[0] * (2/3) - image.shape[0] * 0.5)
    card2[y_offset:y_offset+image.shape[0], 0:image.shape[1]] = image
    counter = counter+1
    card2CorrectSize = cv2.resize(card2, (0, 0), None, 0.236, 0.1935)
    cv2.imwrite(f"{counter}.png", card2CorrectSize)
    # cv2.imwrite(f"{counter}.png", card2)



def convertImage():
    global stripes
    colorArray = [(0,0,255,255),(0,255,0,255),(255,0,0,255)]
    os.chdir("TemplateImages")
    onlyfiles = [f for f in listdir(os.getcwd()) if join(os.getcwd(), f)[-8:] == "_000.png"]
    imageStripes = cv2.imread("Stripes.png", cv2.IMREAD_GRAYSCALE)
    os.chdir('..//..//')

    print(onlyfiles)
    for file in onlyfiles:
        os.chdir("ImageCreation//TemplateImages")
        image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        filled  = image.copy()

        mask = np.zeros(image.shape, np.uint8)
        mask.fill(0)

        contours_draw, hierachy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(mask, contours_draw[0],-1,0,-1)
        h, w = image.shape[:2]

        new_background = np.zeros((h+2, w+2), np.uint8)
        cv2.floodFill(filled, new_background,(0,0),0)

        filled = ~filled                        # not x
        onlyStripes = filled | imageStripes     # x or  y
        figureAndStripes = image^ ~ onlyStripes # (x xor not y)

        os.chdir('..//..//')
        for color in colorArray:
            createCard(changeColor(image, color))            # Only outline
            createCard(changeColor(filled, color))              # Filled figure
            createCard(changeColor(figureAndStripes, color))    # Filled with stripes


# stripes = False
convertImage()
cv2.destroyAllWindows()

##########################################################################################
##########################################################################################
                            #Rename Images
##########################################################################################
##########################################################################################
cardsArray = [[a,b,c,d] for a in ['1','2','3'] for b in ['1','2','3'] for c in ['1','2','3'] for d in ['1','2','3']]
print(len(cardsArray))

for card in range(counter):
    imageText = ''.join(map(str, cardsArray[card]))
    print(imageText)
    os.rename(str(card+1) + ".png", imageText + ".png")