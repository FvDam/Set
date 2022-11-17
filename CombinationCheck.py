from telnetlib import theNULL
from tkinter import *
from itertools import combinations
import random

counter = 0
clickedArray = [[99, 99],[99, 99],[99, 99]]
cardImageArray = [[0 for x in range(5)] for x in range(3)]
cardNumberArray = [[['0','0','0','0'] for x in range(5)] for x in range(3)]
cardDeckArray = [[a,b,c,d] for a in ['1','2','3'] for b in ['1','2','3'] for c in ['1','2','3'] for d in ['1','2','3']]
# random.shuffle(cardDeckArray)


def checkCards(cards):
    global counter
    checkArray = [0,0,0,0]


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
        counter = counter + 1
        # print(cards)
        # input(counter)
        return True
    else:
        return False

def checkAllCards():
    global cardNumberArray
    global cardDeckArray
    arrayForCheck = [[99, 99],[99, 99],[99, 99]]

    totalLoop = 1000000
    lowerBound = 15
    amountOfCards = 15

    for numberOfCards in range(lowerBound, amountOfCards+1):
        falseCounter = 0
        for i in range(totalLoop):
            tCheck = False
            random.shuffle(cardDeckArray)
            for item in combinations(range(numberOfCards),3):
                for card in range(0,3):
                    arrayForCheck[card] = cardDeckArray[item[card]]
                tCheck = tCheck or checkCards(arrayForCheck)
            if not tCheck:
                # print(cardDeckArray[0:12])
                falseCounter = falseCounter + 1
        print(f"Amount of cards:{numberOfCards} Gives:({falseCounter}/{totalLoop})*100={(falseCounter/totalLoop)*100}%")
    
    # for item in combinations(range(81),3):
    #     for card in range(0,3):
    #         arrayForCheck[card] = cardDeckArray[item[card]]
    #     checkCards(arrayForCheck)


checkAllCards()
print(counter)