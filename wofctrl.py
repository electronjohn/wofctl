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
class WOFComputerPlayer(WOFPlayer):
  SORTED_FREQUENCIES = "ZQXJKVBPYGFWMUCLDRHSNIOATE"
  
  def __init__(self, name, difficulty ):
    WOFPlayer.__init__(self, name)
    self.difficulty = difficulty
      
  def smartCoinFlip(self):                 # give difficulty level
    if random.randint(1, 10) <= self.difficulty:
      return False
    else:
      return True 
      
  def getPossibleLetters(self, guessed):
    will_guess = []
    
    for i in LETTERS:
      if (i not in guessed) and (i not in VOWELS) and (i in LETTERS):
        will_guess.append(i)
      elif (i not in guessed) and (i in VOWELS):
        if self.prizeMoney > VOWEL_COST:
          will_guess.append(i)
    return will_guess
  
  def getMove(self, category, obscuredPhrase, guessed):
    will_guess = self.getPossibleLetters(guessed)
    
    if will_guess == []:
      return 'pass'
    else:
      if self.smartCoinFlip() is True:
        for i in self.SORTED_FREQUENCIES[::-1]:
          if i in will_guess:
            return i
      else:
        return random.choice(will_guess)
  
# Spins the wheel of fortune wheel to give a random prize
# Examples:
#    { "type": "cash", "text": "$950", "value": 950, "prize": "A trip to Ann Arbor!" },
#    { "type": "bankrupt", "text": "Bankrupt", "prize": false },
#    { "type": "loseturn", "text": "Lose a turn", "prize": false }
def spinWheel():
  with open("wheel.txt", 'r') as f:
    wheel = json.loads(f.read())
    return random.choice(wheel)

# Returns a category & phrase (as a tuple) to guess
# Example:
#     ("Artist & Song", "Whitney Houston's I Will Always Love You")
def getRandomCategoryAndPhrase():
  with open("phrases.txt", 'r') as f:
    phrases = json.loads(f.read())

    category = random.choice(list(phrases.keys()))
    phrase   = random.choice(phrases[category])
    return (category, phrase.upper())
    
# Given a phrase and a list of guessed letters, returns an obscured version
# Example:
#     guessed: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
#     phrase:  "GLACIER NATIONAL PARK"
#     returns> "_L___ER N____N_L P_RK"
def obscurePhrase(phrase, guessed):
  rv = ''
  for s in phrase:
    if (s in LETTERS) and (s not in guessed):
      rv = rv+'_'
    else:
      rv = rv+s
  return rv

# num_human = getNumberBetween('How many human players?', 0, 10)
num_human = 0

# Create the human player instances
human_players = [WOFHumanPlayer('Player 1')]

# num_computer = getNumberBetween('How many computer players?', 0, 10)
num_computer = 2

# If there are computer players, ask how difficult they should be
if num_computer >= 1:
    # difficulty = getNumberBetween('What difficulty for the computers? (1-10)', 1, 10)
    difficulty = 10

# Create the computer player instances
computer_players = [WOFComputerPlayer('Computer {}'.format(i+1), difficulty) for i in range(num_computer)]

players = human_players + computer_players

# No players, no game :(
if len(players) == 0:
    print('We need players to play!')
    raise Exception('Not enough players')

# category and phrase are strings.
category, phrase = getRandomCategoryAndPhrase()
# guessed is a list of the letters that have been guessed
guessed = ['R', 'S', 'T', 'L', 'N', 'E']

# playerIndex keeps track of the index (0 to len(players)-1) of the player whose turn it is
playerIndex = 0

# will be set to the player instance when/if someone wins
winner = False

def requestPlayerMove(player, category, guessed):
  while True: # we're going to keep asking the player for a move until they give a valid one
    time.sleep(0.1) # added so that any feedback is printed out before the next prompt

    move = player.getMove(category, obscurePhrase(phrase, guessed), guessed)
    move = move.upper() # convert whatever the player entered to UPPERCASE
    if move == 'EXIT' or move == 'PASS':
      return move
    elif len(move) == 1: # they guessed a character
      if move not in LETTERS: # the user entered an invalid letter (such as @, #, or $)
        print('Guesses should be letters. Try again.')
        continue
      elif move in guessed: # this letter has already been guessed
        print('{} has already been guessed. Try again.'.format(move))
        continue
      elif move in VOWELS and player.prizeMoney < VOWEL_COST: # if it's a vowel, we need to be sure the player has enough
        print('Need ${} to guess a vowel. Try again.'.format(VOWEL_COST))
        continue
      else:
        return move
    else: # they guessed the phrase
      return move


class Window(object):
  def __init__(self):
    pygame.init()
    self.height = 240
    self.width = 320

    self.window = pygame.display.set_mode((self.width, self.height), 0, 32)
    self.font = pygame.font.SysFont(None, 25)
    self.fontInfo = pygame.font.SysFont(None, 18)
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
    if letter != '_':
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
  
  def addCategory(self, category):
    # Adds a category below the board
    text = self.font.render(category, True, white)
    textrect = text.get_rect(center = (self.width/2, 170))
    self.window.blit(text, textrect)

  def addGuessed(self, guessed):
    # Adds a list of guessed letters below the board
    resultString = ', '.join(guessed)
    resultString = '[' + resultString + ']'
    self.window.blit(self.fontInfo.render(resultString, True, white), (10,180))
  
  def addPrize(self, prize):
    # Adds a prize below the board
    self.window.blit(self.fontInfo.render(prize, True, white), (10,200))

  def addBg(self):
    self.window.blit(self.bgimg, (0,0))

if __name__ == '__main__':
  run = True
  Wm = Window()
  pygame.display.flip()
  while run:
    Wm.clearBoard()
    obscuredPhrase = obscurePhrase(phrase, guessed)
    Wm.addWords(obscuredPhrase)
    Wm.addCategory(category)
    Wm.addGuessed(guessed)

    player = players[playerIndex]
    wheelPrize = spinWheel()
    Wm.addPrize(wheelPrize["text"])
    pygame.display.flip()
    time.sleep(1) # pause again for more dramatic effect!

    if wheelPrize['type'] == 'bankrupt':
      player.goBankrupt()
    elif wheelPrize['type'] == 'loseturn':
      pass # do nothing; just move on to the next player
    elif wheelPrize['type'] == 'cash':
      move = requestPlayerMove(player, category, guessed)
      if move == 'EXIT': # leave the game
        print('Until next time!')
        break
      elif move == 'PASS': # will just move on to next player
        print('{} passes'.format(player.name))
      elif len(move) == 1: # they guessed a letter
        guessed.append(move)

        print('{} guesses "{}"'.format(player.name, move))

        if move in VOWELS:
          player.prizeMoney -= VOWEL_COST

        count = phrase.count(move) # returns an integer with how many times this letter appears
        if count > 0:
          if count == 1:
            print("There is one {}".format(move))
          else:
            print("There are {} {}'s".format(count, move))

          # Give them the money and the prizes
          player.addMoney(count * wheelPrize['value'])
          if wheelPrize['prize']:
            player.addPrize(wheelPrize['prize'])

          # all of the letters have been guessed
          if obscurePhrase(phrase, guessed) == phrase:
            winner = player
            break

          continue # this player gets to go again

        elif count == 0:
          print("There is no {}".format(move))
      else: # they guessed the whole phrase
        if move == phrase: # they guessed the full phrase correctly
          winner = player

          # Give them the money and the prizes
          player.addMoney(wheelPrize['value'])
          if wheelPrize['prize']:
            player.addPrize(wheelPrize['prize'])

          break
        else:
          print('{} was not the phrase'.format(move))

    # Move on to the next player (or go back to player[0] if we reached the end)
    playerIndex = (playerIndex + 1) % len(players)

if winner:
  # In your head, you should hear this as being announced by a game show host
  print('{} wins! The phrase was {}'.format(winner.name, phrase))
  print('{} won ${}'.format(winner.name, winner.prizeMoney))
  if len(winner.prizes) > 0:
    print('{} also won:'.format(winner.name))
    for prize in winner.prizes:
      print('    - {}'.format(prize))
else:
  print('Nobody won. The phrase was {}'.format(phrase))

for event in pygame.event.get():
  if event.type == pygame.QUIT:
    run = False  
pygame.quit() 
sys.exit()