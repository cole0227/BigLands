import time
import random

from numpy import *
import scipy
import scipy.ndimage
import pygame
from pygame.locals import *
import pygame.time
import pygame.font

import sprite_sheet
import globals
import map_generation

class Tile(object):

	def __init__(self, index):

		self.m_index = index

	def get(self):

		return self.m_index

class Tile_Map(object):

	def __init__(self, height_map, tileset_image, width, height):

		self.m_tileset_image = tileset_image
		self.m_height_map = map_generation.matrix_scale(height_map,0,100)
		
		map_generation.imsave(str(h.size)+".png",h,True)
		
		self.m_height_map = scipy.ndimage.zoom(self.m_height_map, max(width+1,height+1)/(self.m_height_map.size)**0.5, order=0)
		map_generation.imsave(str(self.m_height_map.size)+".png",self.m_height_map,True)
		
		self.m_map = zeros((width,height))

		for row in self.m_map:
			for cell in row:
				cell = []

	def draw(self):
		globals.window_surface.blit()

#core initiation
pygame.init()
pygame.font.init()
random.seed()
globals.window_surface = pygame.display.set_mode((1024,1024), 0, 32) 
pygame.display.set_caption("Tile Test")

#h = map_generation.perlin_main(128, 20, 10, 6)
h = map_generation.perlin_main(128, 5, 1, 3)
t = Tile_Map(h, "Assets/Huge Tileset.png",16,16)