import pygame
import sys
import json
import random
import time

black = (0,0,0)
white = (255,255,255)

VOWEL_COST = 250
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS = 'AEIOU'

class WOFPlayer():
  def __init__(self, name):
    self.name = name
    self.prizeMoney = 0
    self.prizes = []
      
  def addMoney(self, amt):
    self.prizeMoney = amt + self.prizeMoney
  
  def goBankrupt(self):
    self.prizeMoney = 0
      
  def addPrize(self,prize):
    self.prizes.append(prize)
  
  def __str__(self):
    return "{} (${})".format(self.name, self.prizeMoney)

class WOFHumanPlayer(WOFPlayer):
  def __init__(self, name):
    WOFPlayer.__init__(self, name)
  
  def getMove(self, category, obscuredPhrase, guessed):
    print("{},has (${})".format(self.name, self.prizeMoney))
    
    print("Category:", category)
    print("Phrase:", obscuredPhrase)
    print("Guessed:", guessed)
    
    choose = (input("Guess a letter, phrase, or type 'exit' or 'pass':"))
    return choose

class Window(object):
  def __init__(self):
    pygame.init()
    self.height = 240
    self.width = 320

    self.window = pygame.display.set_mode((self.width, self.height), 0, 32)
    self.font = pygame.font.SysFont(None, 25)
    self.bgimg = pygame.image.load("1997-puzzle-board.png")
    self.rectheight = 17
    self.rectwidth = 13
    self.buf = 5.4

  def addRect(self, rectx, recty):
    self.rect = pygame.draw.rect(self.window, white, (rectx, recty, self.rectwidth, self.rectheight))

  def addText(self, rectx, recty, letter):
    # Adds a letter to the board at the position rectx, recty, where 0, 0 is the top left, 
    # centered on the background rectangle
    text = self.font.render(letter, True, black)
    textrect = text.get_rect(center = (rectx + self.rectwidth/2, recty + self.rectheight/2))
    self.window.blit(text, textrect)

  def addLetter(self, row, col, letter):
    # Adds a letter at positions on the wheel of fortune board in the format x, y, 
    # where 0, 0 is the top left, and 4, 12 is the bottom right. 
    self.addRect(53 + col*(Wm.rectwidth + Wm.buf), 61+ row*(Wm.rectheight + Wm.buf))
    self.addText(53 + col*(Wm.rectwidth + Wm.buf), 61+ row*(Wm.rectheight + Wm.buf), letter)

  def addWords(self, letters):
    # Adds a list of letters to the board, starting at position startrow, startcol
    # Tokenizes the string to determine how many words will fit on a row of length 12
    # and then adds the words to the board, starting at column zero for new words
    # and starting at the end of the previous word for words that continue from the
    # previous line.
    startrow = 0
    startcol = 0
    letters = letters.upper()
    words = letters.split()
    for word in words:
      # TODO: Add a check to see if the word will fit on a new line, and if not,
      # hyphenate it and add the rest to the next line
      if startcol + len(word) > 12:
        startrow += 1
        startcol = 0
      for letter in word:
        self.addLetter(startrow, startcol, letter)
        startcol += 1
      startcol += 1

  def clearBoard(self):
    # Clears the board of all letters
    self.window.fill(black)
    self.addBg()

  def addBg(self):
    self.window.blit(self.bgimg, (0,0))


if __name__ == '__main__':
  run = True
  Wm = Window()
  Wm.clearBoard()
  Wm.addWords("Jim Carrey As Ace Ventura")
  pygame.display.flip()
  while run:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
              run = False  
  pygame.quit() 
  sys.exit()