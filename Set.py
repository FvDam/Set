from tkinter import *
from itertools import combinations
import random
import os

cardsCounter = 0
counter = 0
clickedArray = [[99, 99],[99, 99],[99, 99]]
cardImageArray = [[0 for y in range(3)] for x in range(5)]
cardNumberArray = [[['0','0','0','0'] for y in range(3)] for x in range(5)]
cardDeckArray = [[a,b,c,d] for a in ['1','2','3'] for b in ['1','2','3'] for c in ['1','2','3'] for d in ['1','2','3']]

os.chdir("C://Users//frans//Documents//Thuis//Python//Set//Set")

# Function for filling initial button array
def fillImageButtonArray():
    global cardsCounter
    global cardDeckArray
    global cardImageArray

    random.shuffle(cardDeckArray)
    for x in range(0, 4):
        for y in range(0, 3):
            cardImageArray[x][y] = PhotoImage(file=''.join(map(str, cardDeckArray[cardsCounter]))+".png")
            cardNumberArray[x][y] = cardDeckArray[cardsCounter]
            cardsCounter = cardsCounter + 1

def checkCards(clickedArray, cardNumberArray):
    cards = [[],[],[]]
    checkArray = [0,0,0,0]

    for i in range(0,3):
        cards[i] = cardNumberArray[clickedArray[i][0]][clickedArray[i][1]]

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
        print(f"You found a set: ", clickedArray)
        return True
    else:
        return False

def checkAllCards():
    global cardNumberArray
    numberOfSets = 0
    arrayForCheck = [[99, 99],[99, 99],[99, 99]]

    if cardNumberArray[4][0][0] != '0':
        # If deck contains 15 cards
        for item in combinations(range(15),3):
            for card in range(0,3):
                arrayForCheck[card] = [item[card]%5, item[card]//5]
            numberOfSets = numberOfSets + checkCards(arrayForCheck, cardNumberArray)
    else:
        for item in combinations(range(12),3):
            for card in range(0,3):
                arrayForCheck[card] = [item[card]%4, item[card]//4]
            numberOfSets = numberOfSets + checkCards(arrayForCheck, cardNumberArray)
        if numberOfSets == 0:
            fillCardsToFifteen()

    print(f"Total amount of sets found: {numberOfSets}\n\n",)

def fillCardsToFifteen():
    global clickedArray
    global counter
    global cardsCounter
    global cardImageArray
    global cardNumberArray

    for y in range(3):
        cardImageArray[4][y] = PhotoImage(file=''.join(map(str, cardDeckArray[cardsCounter]))+".png")
        cardNumberArray[4][y] = cardDeckArray[cardsCounter]
        cardsCounter = cardsCounter + 1
        btnCardArray[4][y].config(bg="SystemButtonFace", state=NORMAL, bd=2, image=cardImageArray[4][y])
    
    # Reset array and counter
    clickedArray = [[99, 99],[99, 99],[99, 99]]
    counter = 0

def refreshButtonImage():
    global clickedArray
    global counter
    global cardsCounter
    global cardImageArray
    global cardNumberArray
    
    if checkCards(clickedArray, cardNumberArray):
        if cardsCounter == 81:
           print("Game done")
            
        if cardNumberArray[4][0][0] != '0':
            # If deck contains 15 cards
            cardsY = [0,1,2]
            for card_x, card_y in clickedArray:
                if card_x == 4:
                    cardsY.remove(card_y)

            print("CardsY: ", cardsY)

            cardsYCounter = 0
            for card_x, card_y in clickedArray:
                if card_x < 4:
                    cardImageArray[card_x][card_y] = cardImageArray[4][cardsY[cardsYCounter]]
                    cardNumberArray[card_x][card_y] = cardNumberArray[4][cardsY[cardsYCounter]]
                    btnCardArray[card_x][card_y].config(bg="SystemButtonFace", image=cardImageArray[card_x][card_y])
                    cardsYCounter = cardsYCounter + 1
            # Disable cards
            for y in range(3):
                cardNumberArray[4][y] = '0'
                btnCardArray[4][y].config(bg="SystemButtonFace", state=DISABLED, bd=0, image=PhotoImage(file='testEmpty.png'))
        else:
            for card_x, card_y in clickedArray:
                cardImageArray[card_x][card_y] = PhotoImage(file=''.join(map(str, cardDeckArray[cardsCounter]))+".png")
                cardNumberArray[card_x][card_y] = cardDeckArray[cardsCounter]
                cardsCounter = cardsCounter + 1
                btnCardArray[card_x][card_y].config(bg="SystemButtonFace", image=cardImageArray[card_x][card_y])
            print(f"Number of cards: {cardsCounter}")
    else:
        # Set colors back to default if it isn't containing a set
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
        refreshButtonImage()

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

btnCardArray = [[0 for y in range(3)] for x in range(5)]
cardValueArray = [[0 for y in range(3)] for x in range(5)]


emptyImage= PhotoImage(file='testEmpty.png')

fillImageButtonArray()
## Row 1
for x in range(0, 5):
    if x < 4:
        btnCardArray[x][0] = Button(setUpperFrame, image=cardImageArray[x][0], command = lambda x=x, y=0: color_change(x, 0))
        btnCardArray[x][0].pack(side = LEFT )
            
        btnCardArray[x][1] = Button(setCenterFrame, image=cardImageArray[x][1], command = lambda x=x, y=1: color_change(x, 1))
        btnCardArray[x][1].pack(side = LEFT)

        btnCardArray[x][2] = Button(setLowerFrame, image=cardImageArray[x][2], command = lambda x=x, y=2: color_change(x, 2))
        btnCardArray[x][2].pack(side = LEFT)
    else:
        btnCardArray[x][0] = Button(setUpperFrame, image=emptyImage, state=DISABLED, bd=0, command = lambda x=x, y=0: color_change(x, 0))
        btnCardArray[x][0].pack(side = LEFT)
            
        btnCardArray[x][1] = Button(setCenterFrame, image=emptyImage, state=DISABLED, bd=0, command = lambda x=x, y=1: color_change(x, 1))
        btnCardArray[x][1].pack(side = LEFT)

        btnCardArray[x][2] = Button(setLowerFrame, image=emptyImage, state=DISABLED, bd=0, command = lambda x=x, y=2: color_change(x, 2))
        btnCardArray[x][2].pack(side = LEFT)

btnCheckCards = Button(buttonFrame, text="CheckCards", command = checkAllCards)
btnCheckCards.pack( fill = BOTH, expand = True)

scoreFrame.pack (fill = BOTH, expand = True)

setMainFrame.pack(fill = BOTH, expand = True)
setFrame.pack(fill = BOTH, expand = True)
setUpperFrame.pack(expand = True)
setCenterFrame.pack(expand = True)
setLowerFrame.pack(expand = True)
buttonFrame.pack(fill = BOTH, expand = True)

window.mainloop()