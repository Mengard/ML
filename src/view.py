import pygame
import numpy as np
# array access
X = 0
Y = 1

# graphical size of one logical pixel
PX_SIZE = 20

# color
BLACK = (0x00, 0x00, 0x00)
DGRAY = (0x40, 0x40, 0x40)
GRAY  = (0x80, 0x80, 0x80)
LGRAY = (0xC0, 0xC0, 0xC0)
WHITE = (0xFF, 0xFF, 0xFF)


class GameView:
	'''
	This class purpose is to handled the representation of a GameLogic class
	It will draw what GameLogic contains
	'''

	def __init__(self, logic):
		self.logic = logic
		print logic.l_size
		pygame.init()
		pygame.display.set_caption("Cross the road")
		self.font = pygame.font.SysFont("monospace", PX_SIZE * 2, bold=True)
		self.g_size = (np.array(self.logic.l_size) + [0, 2]) * PX_SIZE # 2 more row for the score
		self.screen = self.screen = pygame.display.set_mode(self.g_size)

	'''
	principal method of GameView
	this is the method that will be called by the game engine to refresh the view
	'''
	def draw(self):
		l_size = self.logic.l_size
		self.screen.fill(WHITE)
		self.draw_text(BLACK, str(self.logic.score), [0, 0])
		self.draw_pixel(LGRAY, self.logic.player_pos[X], self.logic.player_pos[Y] + 2)
		for row in range(len(self.logic.obstacles)):
			for obstacle in self.logic.obstacles[row]:
				self.draw_line(BLACK, [obstacle, row + 2], self.logic.obstacle_size, "h")
		pygame.display.flip()
		
	'''
	paint a single logical pixel
		colour : the colour of the pixel
		x      : the logical abscissa of the pixel
		y      : the logical ordinate of the pixel
	'''
	def draw_pixel(self, colour, x, y):
		self.screen.fill(colour, [x * PX_SIZE, y * PX_SIZE, PX_SIZE, PX_SIZE])

	'''
	Create a grid 1px thick on the view
		space  : the spacing of the grid (repeat pattern every space)
		colour : the colour of the grid
		type   : the pattern of the grid, 
					"vertical" for vertical line
					"horizontal" for horizontal line
					"cell" for both
	'''
	def draw_grid(self, colour, space, type="cell"):
		l_size = self.logic.l_size
		# vertical line
		if(type in ["cell", "vertical"]):
			for x in range(0, l_size[X], space):
				self.draw_line(colour, [x, 0], l_size[Y], "v")
		# horizontal line
		if(type in ["cell", "horizontal"]):
			for y in range(0, l_size[Y], space):
				self.draw_line(colour, [0, y], l_size[X], "h")
	
	'''
	paint a straight line
		colour    : the colour of the line
		pos       : an array of 2 value [logical x, logical y] defining the starting position of the line
		length    : the length of the line which can be negative
			positive length implies left to right, or top to bottom
			negative length implies right to left, or bottom to top
		direction : the direction of the line
			"v" or "vertical" for a vertical line (following the y axis)
			"h" or "horizontal" for an horizontal line (following the x axis)
	'''
	def draw_line(self, colour, pos, length, direction):
		step = 1 if length > 0 else -1
		# horizontal line
		if (direction in ["h", "horizontal"]):
			for i in range(0, length, step):
				self.draw_pixel(colour, pos[X] + i, pos[Y])
		# vertical line
		if (direction in ["v","vertical"]):
			for i in range(0, length, step):
				self.draw_pixel(colour, pos[X], pos[Y] + i)
			
	'''
	paint a straight rectangle
		colour    : the colour of the rectangle
		pos       : an array of 2 values [logical x, logical y] defining the principal corner of the rectangle
		dim       : an array of 2 values [logical x length, logical y length] defining the length of the sides, length can be negative
			positive length implies left to right, or top to bottom
			negative length implies right to left, or bottom to top
		fill      : if the inside of the rectangle shares its colour
	'''
	def draw_rect(self, colour, pos, dim, fill=False):
		# no pixel to draw
		if(dim[X] == 0 or dim[Y] == 0):
			return
		# draw the rectangle
		if not fill:
			# compute the two point from which we will draw lines
			other_pos = np.array(pos) + dim
			other_pos[X] += 1 if dim[X] < 0 else -1
			other_pos[Y] += 1 if dim[Y] < 0 else -1
			self.draw_line(colour, pos,        dim[X], "h")
			self.draw_line(colour, pos,        dim[Y], "v")
			self.draw_line(colour, other_pos, -dim[X], "h")
			self.draw_line(colour, other_pos, -dim[Y], "v")
		else:
			start_x = pos[X] if dim[X] > 0 else pos[X] + dim[X] + 1 # +1 to have the correct length and not draw too far
			end_x   = pos[X] + dim[X] - 1 if dim[X] > 0 else pos[X] # -1 to have the correct length and not draw too far
			for x in range(start_x, end_x + 1): # +1 for inclusive range
				self.draw_line(colour, [x, pos[Y]], dim[Y], "v")

	'''
	draw a text
		colour : the colour of the text
		text   : what text to draw
		pos    : an array of 2 values [logical x, logical y] defining the upper left corner where the text will be draw
	'''
	def draw_text(self, colour, text, pos):
		self.screen.blit(self.font.render(text, 1, colour), pos)