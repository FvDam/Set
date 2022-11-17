from PIL import Image
import os
from os import listdir
from os.path import isfile, join


def convertImage():
    # os.chdir(os.getcwd()+'/ScreenShot')
    onlyfiles = [f for f in listdir(os.getcwd()) if join(os.getcwd(), f)[-4:]==".png"]

    for file in onlyfiles:
        img = Image.open(file)
        img = img.convert("RGBA")

        datas = img.getdata()
        newData = []

        for items in datas:
            if items[0] == 255 and items[1] == 255 and items[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append((0, 0, 0, 255))
                #newData.append((255, 192, 203, 255))
                


        img.putdata(newData)
        img.save(f"{file}", "PNG")
        print(f"Successful: {file}")

convertImage()
