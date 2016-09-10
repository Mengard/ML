# Import a library of functions called 'pygame'
import pygame
import numpy as np
	 
# Colors used in RGB
BLACK = (0x00, 0x00, 0x00)
DGRAY = (0x40, 0x40, 0x40)
GRAY  = (0x80, 0x80, 0x80)
LGRAY = (0xC0, 0xC0, 0xC0)
WHITE = (0xFF, 0xFF, 0xFF)
# window dimension
PX_SIZE = 10                 # size of one game-logic pixel
L_SIZE  = np.array([50, 50]) # size of the game-logic window
G_SIZE  = L_SIZE * PX_SIZE   # size of the graphic (real) window 
 
def draw_grid(screen, space, colour, width=1, type="grid"):
	space *= PX_SIZE
	width *= PX_SIZE
	# type not in "grid, vertical, horizontal" will not be handled
	# vertical line
	if(type in ["grid", "vertical"]):
		for i in range(width/2-1, G_SIZE[0] + width/2-1, space):
			pygame.draw.line(screen, colour, [i, 0], [i, G_SIZE[1]], width)
	# horizontal line
	if(type in ["grid", "horizontal"]):
		for i in range(width/2-1, G_SIZE[1] + width/2-1, space):
			pygame.draw.line(screen, colour, [0, i], [G_SIZE[0], i], width)

# paint the pixel in (x,y) in the given colour
def draw_pixel(screen, colour, x, y):
	g_x = x * PX_SIZE
	g_y = y * PX_SIZE
	screen.fill(colour, [g_x, g_y, PX_SIZE, PX_SIZE])

# paint the line starting in (x, y) of the given length, in the given colour, in the given direction
# direction needs to be "horizontal", "vertical", "v" or "h"
def draw_line(screen, colour, pos, length, direction):
	step = 1 if length > 0 else -1
	# horizontal line
	if (direction in ["h", "horizontal"]):
		for i in range(0, length, step):
			draw_pixel(screen, colour, pos[0] + i, pos[1])
	# vertical line
	if (direction in ["v","vertical"]):
		for i in range(0, length, step):
			draw_pixel(screen, colour, pos[0], pos[1] + i)
			
# draw a rectangle of size (dim) from the position (pos), starting from the upper left corner
# size is in pixel, meaning that if dim[0] == 2, the rectangle will cover 2 pixel width 
def draw_rect(screen, colour, pos, dim):
	# no pixel to draw
	if(dim[0] == 0 or dim[1] == 0):
		return
	# compute the two point from which we will draw lines
	corner_one = np.array(pos)
	corner_two = np.array(pos)
	corner_two[0] += dim[0]
	corner_two[1] += dim[1]
	corner_two[0] += 1 if dim[0] < 0 else -1
	corner_two[1] += 1 if dim[1] < 0 else -1
	# draw the rectangle
	draw_line(screen, colour, corner_one, dim[0], "h")
	draw_line(screen, colour, corner_one, dim[1], "v")
	draw_line(screen, colour, corner_two, -dim[0], "h")
	draw_line(screen, colour, corner_two, -dim[1], "v")
		
		
		
def main():
	# Initialize the game engine
	pygame.init()
	 
	# Set the height and width of the screen
	screen = pygame.display.set_mode(G_SIZE)
	 
	pygame.display.set_caption("Example code for the draw module")
	 
	#Loop until the user clicks the close button.
	done = False
	clock = pygame.time.Clock()
	pos = np.array([10, 10]) 
	while not done:
	 
		# This limits the while loop to a max of 10 times per second.
		# Leave this out and we will use all CPU we can.
		clock.tick(10)
		# pos[0] += 1
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done=True # Flag that we are done so we exit this loop
	 
		# All drawing code happens after the for loop and but
		# inside the main while done==False loop.
		 
		# Clear the screen and set the screen background
		screen.fill(WHITE)
		draw_grid(screen, 2, LGRAY, type="grid")
		draw_grid(screen, 10, GRAY, type="grid")
		draw_rect(screen, BLACK, [20, 20], [5, -5])
		pygame.display.flip()
	 
	# Be IDLE friendly
	pygame.quit()


if __name__ == "__main__":
	main()