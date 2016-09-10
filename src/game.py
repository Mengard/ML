# Import a library of functions called 'pygame'
import pygame
import numpy as np
	 
# Colors used in RGB
BLACK = (0x00, 0x00, 0x00)
DGRAY = (0x80, 0x80, 0x80)
LGRAY = (0xB0, 0xB0, 0xB0)
WHITE = (0xFF, 0xFF, 0xFF)
# window dimension
SIZE  = [716, 356]

def grid(screen, space, color, width=1, type="grid"):
	# type not in "grid, vertical, horizontal" will not be handled
	# vertical line
	if(type in ["grid", "vertical"]):
		for i in range(0, SIZE[0], space):
			pygame.draw.line(screen, color, [i, 0], [i, SIZE[1]], width)
	# horizontal line
	if(type in ["grid", "horizontal"]):
		for i in range(0, SIZE[1], space):
			pygame.draw.line(screen, color, [0, i], [SIZE[0], i], width)

def main():
	# Initialize the game engine
	pygame.init()
	 
	# Set the height and width of the screen
	screen = pygame.display.set_mode(SIZE)
	 
	pygame.display.set_caption("Example code for the draw module")
	 
	#Loop until the user clicks the close button.
	done = False
	clock = pygame.time.Clock()
	 
	while not done:
	 
		# This limits the while loop to a max of 10 times per second.
		# Leave this out and we will use all CPU we can.
		clock.tick(10)
		 
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done=True # Flag that we are done so we exit this loop
	 
		# All drawing code happens after the for loop and but
		# inside the main while done==False loop.
		 
		# Clear the screen and set the screen background
		screen.fill(WHITE)
		grid(screen, 10, LGRAY, type="grid")
		# Go ahead and update the screen with what we've drawn.
		# This MUST happen after all the other drawing commands.
		pygame.display.flip()
	 
	# Be IDLE friendly
	pygame.quit()


if __name__ == "__main__":
	main()