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
		self.turn = 0 
		self.obstacle_size = obstacle_size
		self.nb_lines = nb_lines
		self.width = width
		self.score = 0
		self.l_size = [width, nb_lines + 1] # one line for start position, 2 lines for score TODO size for score should not be handled in game logic
		self.pygame = pygame.init()
		self.player_pos = [self.l_size[X]/2, self.l_size[Y]-1]
		self.obstacles = np.zeros((nb_lines+1, (width + obstacle_size)))
		for _ in range(width): # init the game board to not be empty when game start
			self.next_step()
	
	'''
	Execute one logical step in the game
	'''
	def next_step(self):
		# player will be able to move twice before the obstacles
		# self.turn = (self.turn + 1) % 2
		if(self.turn % 1 == 0): # always true
			self.player_move()
			self.check_position()
		if(self.turn % 2 == 0): # half the time
			self.obstacles_move()
			self.check_position()
	
	'''
	Handle the player movement
	'''
	def player_move(self):
		next_pos = np.array(self.player_pos)
		# handle movement
		if self.input == pygame.K_UP:
			next_pos[Y] -= 1
		if self.input == pygame.K_DOWN:
			next_pos[Y] += 1
		if self.input == pygame.K_LEFT:
			next_pos[X] -= 1
		if self.input == pygame.K_RIGHT:
			next_pos[X] += 1
		if(next_pos[Y] == -1 or self.is_in_board(next_pos[X], next_pos[Y])):
			self.player_pos = next_pos
		self.input = None # reset key
	'''
	Handle the obstacles movements
	'''
	def obstacles_move(self):
		# handle new obstacle
		if(random.random() > 0.8):
			new_obstacle = random.randint(0, self.nb_lines - 1)
			self.obstacles[new_obstacle][self.width:self.width + self.obstacle_size] = 1 # fill the line from the end to the offscreen end (obstacle size) 
		# handle obstacles roll
		self.obstacles[:,0] = 0 # remove first column, the one that  will be rolled out
		self.obstacles = np.roll(self.obstacles, -1, axis=1) # shift left, by the column

	'''
	Handle when the player win, or lose
	'''
	def check_position(self):	
		# handle win
		if self.player_pos[Y] == -1: # win !
			self.score += 1
			self.player_pos = [self.l_size[X]/2, self.l_size[Y]-1]
		# handle lose, no penalty beside going back
		if self.player_pos[Y] != self.nb_lines and self.obstacles[self.player_pos[Y]][self.player_pos[X]] == 1: # does not check safe zone
			self.player_pos = [self.l_size[X]/2, self.l_size[Y]-1]
			self.score -= 1 #testing something
			
	
	def get_state(self):
		rang = 1 # TODO move, rename( can't override "range")
		p = self.player_pos
		m = np.zeros((2*rang+1,2*rang+1), dtype=int)
		# TODO optimize
		for x in range(-rang, rang+1):
			for y in range(-rang, rang+1):
				if(self.is_in_board(p[X] + x, p[Y] + y)):
					m[y+rang][x+rang] = self.obstacles[p[Y] + y][p[X] + x]
		m = m.flatten()
		m = np.append(m[:(rang * 2 + 1)+ rang], m[(rang * 2 + 1)+ rang + 1:])
		s = p[X]
		s = (s << 3) + p[Y]
		s = (s << 1) + self.turn
		s = (s << 8) + np.packbits(m)[0]
		# state is here 17 bits long, 6 for player position (3 + 3), 1 for the turn, and 8 for the horizon
		return s
		
		
	def is_in_board(self, x, y):
		if(y < 0):
			return False
		if(y > self.nb_lines):
			return False
		if(x < 0):
			return False
		if(x >= self.width):
			return False
		return True
	'''
	Handle key input event
		input : the key that was pressed (int value)
	'''
	def add_input(self, input):
		self.input = input