# Import a library of functions called 'pygame'
import pygame
import numpy as np
from logic import *
from view import *
	 	
def main():
	pygame.init()
	# create the game logic and associate a view to it
	gl = GameLogic(5, 10, 2)
	gv = GameView(gl)
	clock = pygame.time.Clock()
	done = False
	while not done:
		clock.tick(1)
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done=True # Flag that we are done so we exit this loop
			if event.type == pygame.KEYUP:
				print event.key
		# allow game to resume
		gl.next_step()
		# draw the new game state
		gv.draw()
	# Be IDLE friendly
	pygame.quit()


if __name__ == "__main__":
	main()