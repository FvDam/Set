from telnetlib import theNULL
from tkinter import *
from itertools import combinations
import random

cardsCounter = 0
counter = 0
clickedArray = [[99, 99],[99, 99],[99, 99]]
cardImageArray = [[0 for x in range(5)] for x in range(3)]
cardNumberArray = [[['0','0','0','0'] for x in range(5)] for x in range(3)]
cardDeckArray = [[a,b,c,d] for a in ['1','2','3'] for b in ['1','2','3'] for c in ['1','2','3'] for d in ['1','2','3']]
# for item in combinations(range(12),3):
#     print(item)

# Function for filling initial button array
def fillImageButtonArray():
    global cardsCounter
    global cardDeckArray
    global cardImageArray

    random.shuffle(cardDeckArray)
    for x in range(0, 3):
        for y in range(0, 4):
            cardImageArray[x][y] = PhotoImage(file=''.join(map(str, cardDeckArray[cardsCounter]))+".png")
            cardNumberArray[x][y] = cardDeckArray[cardsCounter]
            cardsCounter = cardsCounter + 1

def checkCards(clickedArray, cardNumberArray):
    cards = [[],[],[]]
    checkArray = [0,0,0,0]

    for i in range(0,3):
        cards[i] = cardNumberArray[clickedArray[i][0]][clickedArray[i][1]]
    # print(cards)

    # Check if cards are all te same
    for atri in range(0, 4):
        for card in range(0, 2):
            if cards[card][atri] == cards[card+1][atri]:
                checkArray[atri] = checkArray[atri] + 1
    
    # Check if all cards are different (1+2+3=6)
    for atri in range(0,4):
        tCounter = 0
        if checkArray[atri] != 2:
            for card in range(0,3):
                tCounter = tCounter + int(cards[card][atri])
            if tCounter != 6:
                break
            else:
                checkArray[atri] = 2

    if sum(checkArray)==8:
        print(cards)
        print("You found a set: ", clickedArray)
        return True
    else:
        return False

def checkAllCards():
    global cardNumberArray
    arrayForCheck = [[99, 99],[99, 99],[99, 99]]

    if cardNumberArray[0][4][0] != '0':
        for item in combinations(range(15),3):
            for card in range(0,3):
                arrayForCheck[card] = [item[card]//5, item[card]%5]
            checkCards(arrayForCheck, cardNumberArray)
    else:
        for item in combinations(range(12),3):
            for card in range(0,3):
                arrayForCheck[card] = [item[card]//4, item[card]%4]
            # print("Short: ",arrayForCheck)
            checkCards(arrayForCheck, cardNumberArray)

    # for item in combinations(range(12),3):
    

    print("Happy!")

def refreshButtonImage(x, y):
    global clickedArray
    global counter
    global cardsCounter
    global cardImageArray
    global cardNumberArray

    if checkCards(clickedArray, cardNumberArray):
        for card_x, card_y in clickedArray:
            cardImageArray[card_x][card_y] = PhotoImage(file=''.join(map(str, cardDeckArray[cardsCounter]))+".png")
            cardNumberArray[card_x][card_y] = cardDeckArray[cardsCounter]
            cardsCounter = cardsCounter + 1
            btnCardArray[card_x][card_y].config(bg="SystemButtonFace", image=cardImageArray[card_x][card_y])
    else:
        for card_x, card_y in clickedArray:
            btnCardArray[card_x][card_y].config(bg="SystemButtonFace", image=cardImageArray[card_x][card_y])
    # Reset array and counter
    clickedArray = [[99, 99],[99, 99],[99, 99]]
    counter = 0

def color_change(x, y):
    global clickedArray
    global cardNumberArray
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
    # print(x,y)

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

btnCheckCards = Button(buttonFrame, text="CheckCards", command = checkAllCards)
btnCheckCards.pack( fill = BOTH, expand = True)

setMainFrame.pack(fill = BOTH, expand = True)
setFrame.pack(fill = BOTH, expand = True)
setUpperFrame.pack(expand = True)
setCenterFrame.pack(expand = True)
setLowerFrame.pack(expand = True)
buttonFrame.pack(fill = BOTH, expand = True)

window.mainloop()