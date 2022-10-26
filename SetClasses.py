from tkinter import *
import tkinter as tk
from tkinter import ttk
from itertools import combinations
import os
import random
import time #time.perf_counter()

# Handy links
# Password manager:
# https://github.com/Why-not-dx/PassManager/blob/main/data_base_exercise/app_handle.py
# https://www.youtube.com/watch?v=CygEKc2bi_0&ab_channel=TILTW
# Paper about set
# https://www.playmonster.com/wp-content/uploads/2019/10/SETPROOF.pdf
# 


LARGEFONT =("Verdana", 35)

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		print("Init")
		self.title("Set")
		self.geometry("1000x700")
		# creating a container
		self.container = tk.Frame(self)
		self.container.pack(side = "top", fill = "both", expand = True)
		self.container.grid_rowconfigure(0, weight = 1)
		self.container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}
		self.Pages = (StartPage, ActualGame, StatsPage)
		# iterating through a tuple consisting
		# of the different page layouts
		for F in self.Pages:
			frame = F(self.container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		for F in self.Pages:
			self.frames[F].resetVisible()
		
		frame = self.frames[cont]

		frame.setVisible()
		frame.tkraise()
	
	def reloadGame(self):
		self.frames[ActualGame].destroy()
		frame = ActualGame(self.container, self)
		self.frames[ActualGame] = frame
		frame.grid(row = 0, column = 0, sticky ="nsew")

# first window frame startpage

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		# label of frame Layout 2
		label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
		
		# putting the grid in its place by using
		# grid
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		button1 = ttk.Button(self, text ="Start Game",
					command = lambda : controller.show_frame(ActualGame))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		## button to show frame 2 with text layout2
		button2 = ttk.Button(self, text ="Stats page",
					command = lambda : controller.show_frame(StatsPage))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

	def setVisible(self):
		self.visible = True

	def resetVisible(self):
		self.visible = False

		

# second window frame page1
class ActualGame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.resetVisible()
		self.inGameTime = 0
		self.startTime = time.perf_counter()
		self.cardsCounter = 0
		self.cardsClickedCounter = 0
		self.score = 0
		self.wrongCounter = 0
		self.clickedArray = [[99, 99],[99, 99],[99, 99]]
		self.cardImageArray = [[0 for y in range(3)] for x in range(5)]
		self.cardNumberArray = [[['0','0','0','0'] for y in range(3)] for x in range(5)]
		self.cardDeckArray = [[a,b,c,d] for a in ['1','2','3'] for b in ['1','2','3'] for c in ['1','2','3'] for d in ['1','2','3']]
		
		## Score counter frame
		self.scoreFrame = tk.Frame(self)

		## Set frame
		self.setMainFrame = tk.Frame(self)
		self.setFrame = tk.Frame(self.setMainFrame)
		self.setUpperFrame = tk.Frame(self.setFrame)
		self.setCenterFrame = tk.Frame(self.setFrame)
		self.setLowerFrame = tk.Frame(self.setFrame)

		## Button frame
		self.buttonFrame = tk.Frame(self)
		
		self.btnCardArray = [[0 for y in range(3)] for x in range(5)]
		self.cardValueArray = [[0 for y in range(3)] for x in range(5)]
		os.chdir("playingCards")
		self.fillImageButtonArray()
		self.emptyImage= PhotoImage(file='testEmpty.png')
		os.chdir("..//")
		for x in range(0, 5):
			if x < 4:
				self.btnCardArray[x][0] = tk.Button(self.setUpperFrame, 
														image = self.cardImageArray[x][0], 
														command = lambda x=x, 
														y=0: self.color_change(x, 0))
				self.btnCardArray[x][0].pack(side = LEFT )
					
				self.btnCardArray[x][1] = tk.Button(self.setCenterFrame, 
														image = self.cardImageArray[x][1], 
														command = lambda x=x, 
														y=1: self.color_change(x, 1))
				self.btnCardArray[x][1].pack(side = LEFT)

				self.btnCardArray[x][2] = tk.Button(self.setLowerFrame, 
														image = self.cardImageArray[x][2], 
														command = lambda x=x, 
														y=2: self.color_change(x, 2))
				self.btnCardArray[x][2].pack(side = LEFT)
			else:
				self.btnCardArray[x][0] = tk.Button(self.setUpperFrame, 
														image = self.emptyImage, 
														state = DISABLED, 
														command = lambda x=x,
														bd=0,
														y=0: self.color_change(x, 0))
				self.btnCardArray[x][0].pack(side = LEFT)
					
				self.btnCardArray[x][1] = tk.Button(self.setCenterFrame, 
														image = self.emptyImage, 
														state = DISABLED, 
														command = lambda x=x,
														bd=0,
														y=1: self.color_change(x, 1))
				self.btnCardArray[x][1].pack(side = LEFT)

				self.btnCardArray[x][2] = tk.Button(self.setLowerFrame, 
														image = self.emptyImage, 
														state = DISABLED, 
														command = lambda x=x,
														bd=0,
														y=2: self.color_change(x, 2))
				self.btnCardArray[x][2].pack(side = LEFT)
		
		# Labels
		self.lblScore = tk.Label(self.scoreFrame, text = "Score: 0")
		self.lblScore.pack(side = LEFT, expand = True)

		self.lblWrong = tk.Label(self.scoreFrame, text = "Wrong: 0")
		self.lblWrong.pack(side = LEFT, expand = True)

		self.lblTime = tk.Label(self.scoreFrame, text = "Time: 0000")
		self.lblTime.pack(side = LEFT, expand = True)
		self.updateRunTime()

		self.lblNumberOfCards = tk.Label(self.scoreFrame, text = "Number of cards: 12/81")
		self.lblNumberOfCards.pack(side = LEFT, expand = True)

		self.scoreFrame.pack (fill = BOTH, expand = True)

		self.setMainFrame.pack(fill = BOTH, expand = True)
		self.setFrame.pack(fill = BOTH, expand = True)
		self.setUpperFrame.pack(expand = True)
		self.setCenterFrame.pack(expand = True)
		self.setLowerFrame.pack(expand = True)
		

		btnCheckCards = tk.Button(self.buttonFrame, text="CheckCards", command = self.checkAllCards)
		btnCheckCards.pack( side=LEFT,  expand = True)

		self.btnResetGame = tk.Button(self.buttonFrame, text = "Reset Game",
							command = lambda : controller.reloadGame())
		self.btnResetGame.pack(side=LEFT, expand = True)

		self.btnStatsPage = tk.Button(self.buttonFrame, text = "Stats page",
							command = lambda : controller.show_frame(StatsPage))

		self.btnStatsPage.pack(side=LEFT, expand = True)
		self.buttonFrame.pack(fill = BOTH, expand = True)
	
	def fillImageButtonArray(self):
		random.shuffle(self.cardDeckArray)
		for x in range(0, 4):
			for y in range(0, 3):
				self.cardImageArray[x][y] = tk.PhotoImage(file=''.join(map(str, self.cardDeckArray[self.cardsCounter]))+".png")
				self.cardNumberArray[x][y] = self.cardDeckArray[self.cardsCounter]
				self.cardsCounter = self.cardsCounter + 1
	
	def color_change(self, x, y):
		## Check if button already pressed
		if [x, y] in self.clickedArray:
			for i in range(0,3):
				if self.clickedArray[i] == [x, y]:
					self.cardsClickedCounter = self.cardsClickedCounter - 1
					self.clickedArray[i] = [99, 99]
					self.btnCardArray[x][y].config(bg="SystemButtonFace")
		else:
			# Search first empty spot in clicked array
			for i in range(0,3):
				if self.clickedArray[i] == [99, 99]:
					self.clickedArray[i] = [x, y]
					break
			self.btnCardArray[x][y].config(background="red")
			self.cardsClickedCounter = self.cardsClickedCounter + 1

		print(self.clickedArray)
		
		if self.cardsClickedCounter == 3:
			self.refreshButtonImage()

	def checkAllCards(self):	
		numberOfSets = 0
		arrayForCheck = [[99, 99],[99, 99],[99, 99]]

		# If deck contains 15 cards
		if self.cardNumberArray[4][0][0] != '0':
			for item in combinations(range(15),3):
				for card in range(0,3):
					arrayForCheck[card] = [item[card]%5, item[card]//5]
				numberOfSets = numberOfSets + self.checkCards(arrayForCheck)
		# If deck contains 12
		elif self.cardNumberArray[3][0][0] != '0':
			for item in combinations(range(12),3):
				for card in range(0,3):
					arrayForCheck[card] = [item[card]%4, item[card]//4]
				numberOfSets = numberOfSets + self.checkCards(arrayForCheck)
			# If the last 12 cards contain a set don't add non existing cards
			if numberOfSets == 0 and self.cardsCounter != 81:
				self.fillCardsToFifteen()
		# If deck contains 9 cards
		elif self.cardNumberArray[2][0][0] != '0':
			for item in combinations(range(9),3):
				for card in range(0,3):
					arrayForCheck[card] = [item[card]%3, item[card]//3]
				numberOfSets = numberOfSets + self.checkCards(arrayForCheck)
		# If deck contains 6 cards
		elif self.cardNumberArray[1][0][0] != '0':
			for item in combinations(range(6),3):
				for card in range(0,3):
					arrayForCheck[card] = [item[card]%2, item[card]//2]
				numberOfSets = numberOfSets + self.checkCards(arrayForCheck)
		# If deck contains 3 cards will probably never happen
		elif self.cardNumberArray[0][0][0] != '0':
			for item in combinations(range(3),3):
				for card in range(0,3):
					arrayForCheck[card] = [item[card]%1, item[card]//1]
				numberOfSets = numberOfSets + self.checkCards(arrayForCheck)

		print(f"Total amount of sets found: {numberOfSets}\n\n",)
		return numberOfSets > 0

	def checkCards(self, clickedArray):
		cards = [[],[],[]]
		checkArray = [0,0,0,0]

		for i in range(0,3):
			cards[i] = self.cardNumberArray[clickedArray[i][0]][clickedArray[i][1]]

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
	
	def updatePointCounter(self):
		typeOfSet = 0
		cards = [[],[],[]]
		points = (3,1,2,4)
		for i in range(0,3):
			cards[i] = self.cardNumberArray[self.clickedArray[i][0]][self.clickedArray[i][1]]
		
		# Check if cards are all te same
		for atri in range(0, 4):
			tMatch = 0
			for card in range(0, 2):
				if cards[card][atri] == cards[card+1][atri]:
					tMatch = tMatch + 1
			if tMatch == 2:
				typeOfSet = typeOfSet + 1

		self.score = self.score + points[typeOfSet]
		self.lblScore.config(text = f"score: {self.score: <3} ")

	def reorganiseCards(self, prevAmountRows):
		remaningCardsY = [0,1,2]
		for card_x, card_y in self.clickedArray:
			if card_x == prevAmountRows:
				remaningCardsY.remove(card_y)

		print("CardsY: ", remaningCardsY)

		cardsYCounter = 0
		for card_x, card_y in self.clickedArray:
			if card_x < prevAmountRows:
				self.cardImageArray[card_x][card_y] = self.cardImageArray[prevAmountRows][remaningCardsY[cardsYCounter]]
				self.cardNumberArray[card_x][card_y] = self.cardNumberArray[prevAmountRows][remaningCardsY[cardsYCounter]]
				self.btnCardArray[card_x][card_y].config(bg="SystemButtonFace", image=self.cardImageArray[card_x][card_y])
				cardsYCounter = cardsYCounter + 1
		# Disable cards
		for y in range(3):
			self.cardNumberArray[prevAmountRows][y] = '0'
			self.btnCardArray[prevAmountRows][y].config(bg="SystemButtonFace", state=DISABLED, bd=0, image=PhotoImage(file='testEmpty.png'))

	def refreshButtonImage(self):
		if self.checkCards(self.clickedArray):
			self.updatePointCounter()	
			if self.cardNumberArray[4][0][0] != '0':
				self.reorganiseCards(4)
			elif self.cardNumberArray[3][0][0] != '0' and self.cardsCounter != 81:
				for card_x, card_y in self.clickedArray:
					self.cardImageArray[card_x][card_y] = PhotoImage(file=''.join(map(str, self.cardDeckArray[self.cardsCounter]))+".png")
					self.cardNumberArray[card_x][card_y] = self.cardDeckArray[self.cardsCounter]
					self.cardsCounter = self.cardsCounter + 1
					self.btnCardArray[card_x][card_y].config(bg="SystemButtonFace", 
															image=self.cardImageArray[card_x][card_y])
				self.lblNumberOfCards.config(text = f"Number of cards:{self.cardsCounter}/81")
				print(f"Number of cards: {self.cardsCounter}")
			# Last 12 cards
			elif self.cardNumberArray[3][0][0] != '0':
				self.reorganiseCards(3)
				if self.checkAllCards:
					tk.messagebox.showinfo(title='Game done!', 
											message = f"Good job you finished the game in: \n{self.inGameTime} secondes")
					self.btnResetGame.invoke()
					self.btnStatsPage.invoke()
			# Last 9 cards
			elif self.cardNumberArray[2][0][0] != '0':
				self.reorganiseCards(2)
				if self.checkAllCards:
					tk.messagebox.showinfo(title='Game done!', 
											message = f"Good job you finished the game in: \n{self.inGameTime} secondes")
					self.btnResetGame.invoke()
					self.btnStatsPage.invoke()
			# Last 6 cards
			elif self.cardNumberArray[1][0][0] != '0':
				self.reorganiseCards(1)
				if self.checkAllCards:
					tk.messagebox.showinfo(title='Game done!', 
											message = f"Good job you finished the game in: \n{self.inGameTime} secondes")
					self.btnResetGame.invoke()
					self.btnStatsPage.invoke()
			# Last 3 cards
			elif self.cardNumberArray[1][0][0] != '0':
				tk.messagebox.showinfo(title='Game done!', message = f"Good job you finished the game in: \n{self.inGameTime} secondes")
				self.btnResetGame.invoke()
				self.btnStatsPage.invoke()
		else:
			print("This isn't a set")
			# Update wrong counter
			self.wrongCounter = self.wrongCounter + 1
			self.lblWrong.config(text = f"Wrong: {self.wrongCounter}" )
			# Set colors back to default if it isn't containing a set
			for card_x, card_y in self.clickedArray:
				self.btnCardArray[card_x][card_y].config(bg="SystemButtonFace", image=self.cardImageArray[card_x][card_y])

		# Reset array and counter
		self.clickedArray = [[99, 99],[99, 99],[99, 99]]
		self.cardsClickedCounter = 0

	def fillCardsToFifteen(self):
		for y in range(3):
			self.cardImageArray[4][y] = PhotoImage(file=''.join(map(str, self.cardDeckArray[self.cardsCounter]))+".png")
			self.cardNumberArray[4][y] = self.cardDeckArray[self.cardsCounter]
			self.cardsCounter = self.cardsCounter + 1
			self.btnCardArray[4][y].config(bg="SystemButtonFace", state=NORMAL, bd=2, image=self.cardImageArray[4][y])
		
		# Reset array and counter
		self.clickedArray = [[99, 99],[99, 99],[99, 99]]
		self.cardsClickedCounter = 0

	def updateRunTime(self):
		# self.lblTime.config(text = f"Time: {int(time.perf_counter()-self.startTime):0>4}")
		self.lblTime.config(text = f"Time: {self.inGameTime:0>4}")
		self.inGameTime = self.inGameTime + 1
		# print(f"Label: {self.visible}")
		# print(f"Time: {self.inGameTime:0>4}")
		self.lblTime.after(1000, self.updateRunTime)

	def setVisible(self):
		self.visible = True

	def resetVisible(self):
		self.visible = False

# third window frame page2
class StatsPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Stats template", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="ActualGame",
							command = lambda : controller.show_frame(ActualGame))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 3 with text
		# layout3
		button2 = ttk.Button(self, text ="Startpage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

	def setVisible(self):
		self.visible = True

	def resetVisible(self):
		self.visible = False

os.chdir("C://Users//frans//Documents//Thuis//Python//Set//Set")
# Driver Code

Set = tkinterApp

Set().mainloop()