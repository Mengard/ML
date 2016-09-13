# Import a library of functions called 'pygame'
import pygame
import numpy as np
import matplotlib.pyplot as plt
from logic import *
from view import *
from sarsa import *
	 	
def main():
	scores = []
	pygame.init()
	# create the game logic and associate a view to it
	gl = GameLogic(6, 7, 1)
	gv = GameView(gl)
	solver = Sarsa(gl, 0.95, 0.9, 0.2, [0, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]) # 0 symbolise "pass turn"
	clock = pygame.time.Clock()
	done = False
	turn = 0
	old_state = gl.get_state()
	old_action = 0
	while not done:
		#clock.tick(100)
		if(turn % 1000 == 0):
			scores += [gl.score]
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done=True # Flag that we are done so we exit this loop
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					plt.plot(range(len(scores)), scores)
					plt.show()
				gl.add_input(event.key)
		old_score = gl.score # to know when we scored
		# operate the solver action
		gl.add_input(old_action)
		gl.next_step()
		# learn from it
		new_state = gl.get_state()
		new_action = solver.choose_action(new_state)
		reward = gl.score - old_score
		solver.learn(old_state, old_action, new_state, new_action, reward)
		old_state = new_state
		old_action = new_action
		# draw the new game state
		gv.draw()
		turn += 1
	# Be IDLE friendly
	pygame.quit()


if __name__ == "__main__":
	main()