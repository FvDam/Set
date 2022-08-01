from tkinter import *
import random


counter = 0
clickedArray = [[99, 99],[99, 99],[99, 99]]
cardsArray = [[a, b, c, d] for a in [1,2,3] for b in [1,2,3] for c in [1,2,3] for d in [1,2,3]]
random.shuffle(cardsArray)


print(cardsArray)
def refreshButtonCollor(x, y):
    global clickedArray
    global counter
    global clicked_btn

    
    # Reset colors
    for card_x, card_y in clickedArray:
        btnCard[card_x][card_y].config(bg="SystemButtonFace", image=clicked_btn)
        


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
                btnCard[x][y].config(bg="SystemButtonFace")
    else:
        # Search first empty spot in clicked array
        for i in range(0,3):
            if clickedArray[i] == [99, 99]:
                clickedArray[i] = [x, y]
                break
        btnCard[x][y].config(bg="red")
        counter = counter + 1

    print(clickedArray)
    
    if counter == 3:
        refreshButtonCollor(x, y)
    print(x,y)

window = Tk()

window.title("Set")
window.geometry("1500x800")

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

btnCard = [[0 for x in range(5)] for x in range(3)]
click_btn= PhotoImage(file='test.png')
clicked_btn= PhotoImage(file='testing.png')

## Row 1
for y in range(0, 5):
    if y < 4:
        btnCard[0][y] = Button(setUpperFrame, image=click_btn, command = lambda x=0, y=y: color_change(0, y))
        btnCard[0][y].pack(side = LEFT, fill = BOTH, expand=True)
            
        btnCard[1][y] = Button(setCenterFrame, image=click_btn, command = lambda x=1, y=y: color_change(1, y))
        btnCard[1][y].pack(side = LEFT, fill = BOTH, expand=True)

        btnCard[2][y] = Button(setLowerFrame, image=click_btn, command = lambda x=2, y=y: color_change(2, y))
        btnCard[2][y].pack(side = LEFT, fill = BOTH, expand=True)
    else:
        btnCard[0][y] = Button(setUpperFrame, command = lambda x=0, y=y: color_change(0, y))
        btnCard[0][y].pack(side = LEFT, fill = BOTH, expand=True)
            
        btnCard[1][y] = Button(setCenterFrame, command = lambda x=1, y=y: color_change(1, y))
        btnCard[1][y].pack(side = LEFT, fill = BOTH, expand=True)

        btnCard[2][y] = Button(setLowerFrame, command = lambda x=2, y=y: color_change(2, y))
        btnCard[2][y].pack(side = LEFT, fill = BOTH, expand=True)


setMainFrame.pack(fill = BOTH, expand=True)
setFrame.pack(side = LEFT, fill = BOTH, expand=True)
setUpperFrame.pack(fill = BOTH, expand=True)
setCenterFrame.pack(fill = BOTH, expand=True)
setLowerFrame.pack(fill = BOTH, expand=True)

window.mainloop()