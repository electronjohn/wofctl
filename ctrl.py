'''Set up game mechanics for a complete Schulte Grid game where the player needs to click on the images of numbers 1-25 in sequence and measure the time'''

import pygame # Import the pygame library
import numpy as np # Import the numpy library
import itertools # Import the itertools library
import sys # Import the sys library

pygame.init()  # Initialize pygame
width = 320  # Define the width
height = 240  # Define the height
size = (width, height)  # Define the size
screen = pygame.display.set_mode(size)  # Create the game window with the size (240,320)

# Timer text preparation
font = pygame.font.SysFont('Arial', 60)  # Create a Font object for the timer text

# Set image coordinates
Xpts = np.linspace(0,width,6)  # x coordinates
Ypts = np.linspace(0,height-90,6)  # y coordinates
ha = itertools.product(Xpts, Ypts)  # Generate all permutations of x and y coordinates, resulting in 25 sets of data
haha = list(ha)  # Convert the permutations to a list
'''
Result: [( 0.0 , 0.0 ), ( 0.0 , 30.0 ), ( 0.0 , 60.0 ), ( 0.0 , 90.0 ), ( 0.0 , 120.0 ), ( 0.0 , 150.0 ), ( 64.0 , 0.0 ), ( 64.0 , 30.0 ), ( 64.0 , 60.0 ), ( 64.0 , 90.0 ), ( 64.0 , 120.0 ), ( 64.0 , 150.0 ), ( 128.0 , 0.0 ), ( 128.0 , 30.0 ), ( 128.0 , 60.0 ), ( 128.0 , 90.0 ), ( 128.0 , 120.0 ), ( 128.0 , 150.0 ), ( 192.0 , 0.0 ), ( 192.0 , 30.0 ), ( 192.0 , 60.0 ), ( 192.0 , 90.0 ), ( 192.0 , 120.0 ), ( 192.0 , 150.0 ), ( 256.0 , 0.0 ), ( 256.0 , 30.0 ), ( 256.0 , 60.0 ), ( 256.0 , 90.0 ), ( 256.0 , 120.0 ), ( 256.0 , 150.0 ), ( 320.0 , 0.0 )]
'''
map = np.array(haha)  # Convert the list data to an array

# Define the ready function to determine the image sequence
def ready():
	global list1  # Define a global variable list1
	list1 = ['A', 'B', 'C', 'D', 'E', 'Z', 'F', 'G', 'H', 'I', 'J', ' ', 'K', 'L'
	  					, 'M', 'N', 'O', ' ', 'P', 'Q', 'R', 'S', 'T', '[', 'U', 'V'
							, 'W', 'X', 'Y', '\r\n']  # Define a list of 3 letters

# Define the game interface
def gamePage(game_page):
	while game_page:  # When entering the game page
		screen.blit(pygame.image.load("pic/keys.png"), (0, 0))  # Display the image "keys.png" at (0,0)
		for event in pygame.event.get():  # Traverse all events
			if event.type == pygame.QUIT:  # If the window is closed, quit
				pygame.quit()  # Quit pygame
				sys.exit()
			for i in range(31):  # Loop 31 times
				# If the mouse is released and within the range of a certain letter image
				if event.type == pygame.MOUSEBUTTONUP and map[i][0] <= event.pos[0] <= map[i][0] + 64 and map[i][1] <= event.pos[1] <= map[i][1] + 30:
					print(*list1[i])  # Print the letter corresponding to the clicked position
					print(event.pos) # Print the coordinates of the clicked position
		pygame.display.flip()  # Update all displays

game_page = True  # Define the initial game page status as True
while True:  # Loop
	ready()  # Call the ready function
	gamePage(game_page)  # Call the gamePage function