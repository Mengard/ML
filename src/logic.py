from view import *
import pygame
from time import sleep
import random
X = 0
Y = 1

class GameLogic:
	'''
	This class will handle the game logic itself
	It will handle how to game progress through the time as well as user input
	'''

	'''
	Initialize the game logic
		nb_lines      : vertical size, the number of row to cross to increase the score
		width         : horizontal size
		obstacle_size : the horizontal length of the obstacles 
	'''
	def __init__(self, nb_lines, width, obstacle_size):
		random.seed(1)
		self.input = None
		self.obstacle_size = obstacle_size
		self.nb_lines = nb_lines
		self.width = width
		self.score = 0
		self.l_size = [width, nb_lines + 1] # one line for start position, 2 lines for score TODO size for score should not be handled in game logic
		self.pygame = pygame.init()
		self.player_pos = [self.l_size[X]/2, self.l_size[Y]-1]
		self.obstacles = [[] for i in range(nb_lines)]
		for _ in range(width): # init the game board to not be empty when game start
			self.next_step()
	
	'''
	Execute one logical step in the game
	'''
	def next_step(self):
		if self.input == pygame.K_UP:
			self.player_pos[Y] -= 1
		if self.input == pygame.K_DOWN:
			self.player_pos[Y] += 1
		if self.input == pygame.K_LEFT:
			self.player_pos[X] -= 1
		if self.input == pygame.K_RIGHT:
			self.player_pos[X] += 1
		self.input = None # reset key 
		new_obstacle = random.randint(0, self.nb_lines - 1)
		self.obstacles[new_obstacle] += [self.width]
		new_obstacles = [[] for i in range(self.nb_lines)]
		for row in range(len(self.obstacles)):
			for obstacle in self.obstacles[row]:
				if obstacle > -self.obstacle_size:
					new_obstacles[row] += [obstacle - 1]
		self.obstacles = new_obstacles

	'''
	Handle key input event
		input : the key that was pressed (int value)
	'''
	def add_input(self, input):
		self.input = input