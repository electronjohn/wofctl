import pygame
import sys
import itertools 

black = (0,0,0)
red = (255,0,0)
white = (255,255,255)

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

  def addText(self, rectx, recty):
    self.window.blit(self.font.render('E', True, red), (rectx, recty+1))

  def addLetter(self, row, col):
    # Adds a letter at positions on the wheel of fortune board in the format x, y, 
    # where 0, 0 is the top left, and 4, 12 is the bottom right. 
    self.addRect(53 + col*(Wm.rectwidth + Wm.buf), 61+ row*(Wm.rectheight + Wm.buf))
    self.addText(53 + col*(Wm.rectwidth + Wm.buf), 61+ row*(Wm.rectheight + Wm.buf))

  def addBg(self):
    self.window.blit(self.bgimg, (0,0))


if __name__ == '__main__':
  run = True

  Wm = Window()
  Wm.addBg()
  Wm.addLetter(0, 0)
  Wm.addLetter(1, 1)
  Wm.addLetter(1, -1)
  Wm.addLetter(2, 2)
  Wm.addLetter(3, 3)
  Wm.addLetter(3, 11)
  pygame.display.flip()
  while run:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
              run = False  
  pygame.quit() 
  sys.exit()