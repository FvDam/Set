import cv2
import numpy as np

# font
font = cv2.FONT_HERSHEY_SIMPLEX
  
# fontScale
fontScale = 1
   
# Blue color in BGR
color = (0, 255, 0)
  
# Line thickness of 2 px
thickness = 2
   
image_height = 191
image_width = 148
number_of_color_channels = 3
# color = (255,0,255)
pixel_array = np.full((image_height, image_width, number_of_color_channels), color, dtype=np.uint8)

cardsArray = [[a,b,c,d] for a in ['1','2','3'] for b in ['1','2','3'] for c in ['1','2','3'] for d in ['1','2','3']]
for card in cardsArray:
    imageText = ''.join(map(str, card))
    cv2.imwrite(imageText+".png", pixel_array)

# org
org = (35, 110)
color = (0, 0, 0)
for card in cardsArray:
    imageText = ''.join(map(str, card))
    image = cv2.imread(imageText+".png")
    image = cv2.putText(image, imageText, org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    cv2.imwrite(imageText+".png", image)