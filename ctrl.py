'''Set up game mechanics for a complete Schulte Grid game where the player needs to click on the images of numbers 1-25 in sequence and measure the time'''

import pygame # Import the pygame library
import numpy as np # Import the numpy library
import itertools # Import the itertools library
import time # Import the time library

pygame.init()  # Initialize pygame
width = 320  # Define the width
height = 240  # Define the height
size = (width, height)  # Define the size
screen = pygame.display.set_mode(size)  # Create the game window with the size (240,320)

# Load sound effect
wavFileName = 'sounds/fire.wav'  # Set the sound effect file path
sndTrack = pygame.mixer.music.load(wavFileName)  # Load the sound effect file
# Timer text preparation
font = pygame.font.SysFont('Arial', 60)  # Create a Font object for the timer text

# Set image coordinates
Xpts = [0, 64, 128, 192, 256, 320]  # x coordinates
Ypts = [0, 30, 60, 90, 120, 150]  # y coordinates
# map = np.array(list(itertools.product(Xpts, Ypts)))  # 25 image coordinates
ha = itertools.product(Xpts, Ypts)  # Generate all permutations of x and y coordinates, resulting in 25 sets of data
haha = list(ha)  # Convert the permutations to a list
'''Result: [(0, 0), (0, 48), (0, 96), (0, 144), (0, 192), (48, 0), (48, 48), (48, 96), (48, 144),
 (48, 192), (96, 0), (96, 48), (96, 96), (96, 144), (96, 192), (144, 0), (144, 48), (144, 96),
 (144, 144), (144, 192), (192, 0), (192, 48), (192, 96), (192, 144), (192, 192)]'''
map = np.array(haha)  # Convert the list data to an array

print(map)

# Define the ready function to determine the image sequence
def ready():
	global list1  # Define a global variable list1
	list1 = ['A', 'B', 'C', 'D', 'E', 'Z', 'F', 'G', 'H', 'I', 'J', '_', 'K', 'L'
	  					, 'M', 'N', 'O', '_', 'P', 'Q', 'R', 'S', 'T', '[', 'U', 'V'
							, 'W', 'X', 'Y', 'WHL']  # Define a list of 36 letters
# Define the start page
def start(start_page):
	while start_page:  # When on the start page
		for event in pygame.event.get():  # Iterate through all events
			if event.type == pygame.QUIT:  # If the window is closed, exit
				pygame.quit()  # Quit pygame
			screen.blit(pygame.image.load("pic/start-5.png"), (30, 190))  # Display the image "start-5.png" at (30,190)

			global t_x, t_y  # Define two global variables t_x and t_y
			t_x, t_y = pygame.mouse.get_pos()  # Get the x and y coordinates of the mouse and store them in variables t_x and t_y
			if 30 <= t_x <= 200 and 190 <= t_y <= 250:  # If the mouse is within the range of the "start game" image
				screen.blit(pygame.image.load("pic/start-6.png"), (30, 190))  # Switch the image to "start-6.png" at (30,190)
			if event.type == pygame.MOUSEBUTTONUP and 30 <= t_x <= 200 and 190 <= t_y <= 250:  # If the mouse is released and the coordinates are within the range of the "start game" image
				start_page = False  # Set the start page status to False, exit the start page
				game_page = True  # Set the game page status to True, enter the game page
				global time_start  # Define the global variable for starting time
				screen.fill((0, 0, 0))  # Fill the screen with black
				time_start = time.time()  # Start the timer, returns the current time as a timestamp
		pygame.display.flip()  # Update the display

# Define the game interface
def gamePage(game_page):
	while game_page:  # When entering the game page
		screen.blit(pygame.image.load("pic/keys.png"), (0, 0))  # Display the image "keys.png" at (0,0)
		for event in pygame.event.get():  # Traverse all events
			if event.type == pygame.QUIT:  # If the window is closed, quit
				pygame.quit()  # Quit pygame
			for i in range(36):  # Loop 36 times
				# If the mouse is released and within the range of a certain letter image
				if event.type == pygame.MOUSEBUTTONUP and map[i][0] <= event.pos[0] <= map[i][0] + 64 and map[i][1] <= event.pos[1] <= map[i][1] + 30:
					print(*list1[i])  # Print the letter corresponding to the clicked position
					print(event.pos) # Print the coordinates of the clicked position
		pygame.display.flip()  # Update all displays

start_page = True  # Define the initial start page status as True
game_page = True  # Define the initial game page status as True
while True:  # Loop
	ready()  # Call the ready function
	start(start_page)  # Call the start function
	gamePage(game_page)  # Call the gamePage function