from tkinter import *
import random

cardsCounter = 0
counter = 0
clickedArray = [[99, 99],[99, 99],[99, 99]]
cardImageArray = [[0 for x in range(5)] for x in range(3)]
cardsArray = [[a,b,c,d] for a in ['1','2','3'] for b in ['1','2','3'] for c in ['1','2','3'] for d in ['1','2','3']]

# Function for filling initial button array
def fillImageButtonArray():
    global cardsCounter
    global cardsArray
    global cardImageArray

    for x in range(0, 3):
        for y in range(0, 5):
            cardImageArray[x][y] = PhotoImage(file=''.join(map(str, cardsArray[cardsCounter]))+".png")
            cardsCounter = cardsCounter + 1

def refreshButtonImage(x, y):
    global clickedArray
    global counter
    global clicked_btn
    global cardsCounter
    global cardImageArray

    for card_x, card_y in clickedArray:
        cardImageArray[card_x][card_y] = PhotoImage(file=''.join(map(str, cardsArray[cardsCounter]))+".png")
        cardsCounter = cardsCounter + 1
        btnCardArray[card_x][card_y].config(bg="SystemButtonFace", image=cardImageArray[card_x][card_y])

    # Reset array and counter
    clickedArray = [[99, 99],[99, 99],[99, 99]]
    counter = 0

def color_change(x, y):
    global clickedArray
    global counter

    ## Check if button already pressed
    if [x, y] in clickedArray:
        for i in range(0,3):
            if clickedArray[i] == [x, y]:
                counter = counter - 1
                clickedArray[i] = [99, 99]
                btnCardArray[x][y].config(bg="SystemButtonFace")
    else:
        # Search first empty spot in clicked array
        for i in range(0,3):
            if clickedArray[i] == [99, 99]:
                clickedArray[i] = [x, y]
                break
        btnCardArray[x][y].config(bg="red")
        counter = counter + 1

    print(clickedArray)
    
    if counter == 3:
        refreshButtonImage(x, y)
    print(x,y)

window = Tk()

window.title("Set")
window.geometry("1000x650")

## Score counter frame
scoreFrame = Frame(window)

## Set frame
setMainFrame = Frame(window)
setFrame = Frame(setMainFrame)
setUpperFrame = Frame(setFrame)
setCenterFrame = Frame(setFrame)
setLowerFrame = Frame(setFrame)

## Set extra frame
setExtraFrame = Frame(window)

## Button frame
buttonFrame = Frame(window)

btnCardArray = [[0 for x in range(5)] for x in range(3)]
cardValueArray = [[0 for x in range(5)] for x in range(3)]


emptyImage= PhotoImage(file='testEmpty.png')

fillImageButtonArray()
## Row 1
for y in range(0, 5):
    if y < 4:
        btnCardArray[0][y] = Button(setUpperFrame, image=cardImageArray[0][y], command = lambda x=0, y=y: color_change(0, y))
        btnCardArray[0][y].pack(side = LEFT )
            
        btnCardArray[1][y] = Button(setCenterFrame, image=cardImageArray[1][y], command = lambda x=1, y=y: color_change(1, y))
        btnCardArray[1][y].pack(side = LEFT)

        btnCardArray[2][y] = Button(setLowerFrame, image=cardImageArray[2][y], command = lambda x=2, y=y: color_change(2, y))
        btnCardArray[2][y].pack(side = LEFT)
    else:
        btnCardArray[0][y] = Button(setUpperFrame, image=emptyImage, state=DISABLED, bd=0, command = lambda x=0, y=y: color_change(0, y))
        btnCardArray[0][y].pack(side = LEFT)
            
        btnCardArray[1][y] = Button(setCenterFrame, image=emptyImage, state=DISABLED, bd=0, command = lambda x=1, y=y: color_change(1, y))
        btnCardArray[1][y].pack(side = LEFT)

        btnCardArray[2][y] = Button(setLowerFrame, image=emptyImage, state=DISABLED, bd=0, command = lambda x=2, y=y: color_change(2, y))
        btnCardArray[2][y].pack(side = LEFT)


setMainFrame.pack(fill = BOTH, expand = True)
setFrame.pack(side = LEFT, fill = BOTH, expand = True)
setUpperFrame.pack(expand = True)
setCenterFrame.pack(expand = True)
setLowerFrame.pack(expand = True)

window.mainloop()