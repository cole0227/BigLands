import random
import copy
import pickle
import re

import pygame
import pygame.time
from pygame.locals import *
import pygame.mouse

import globals
from timer import *
from util import *
from unit import *
from ability import *
from roman import int_to_roman as roman

# resources are things like gold, gems, or whatever else
# since we don't care about inventory management, we just want to keep track of our material stacks and resources together
class Resource(object):

	def __init__(self, name, image, val=0):

		self.m_name = name
		self.m_val = val
		self.m_stale_val = -42
		self.m_image = image

	def update_surface(self):

		if(self.m_val != self.m_stale_val):
			string_name = self.m_name+": "
			string_count = str(int(self.m_val))
			dims = globals.basic_font[4].size(string_name+string_count)

			# only the first time
			if(self.m_stale_val == -42):
				self.m_image = pygame.transform.scale(self.m_image,(dims[1],dims[1]));

			resource_offset = globals.basic_font[4].size(string_name)[0]
			self.m_surf = pygame.Surface((dims[0]+dims[1]+2,dims[1]+2),SRCALPHA,32).convert_alpha()
			self.m_surf.blit(globals.basic_font[4].render(string_name+string_count,1,(0,0,0)),(dims[1]+2,2))
			self.m_surf.blit(globals.basic_font[4].render(string_name,1,(240,230,140)),(dims[1],0))
			self.m_surf.blit(globals.basic_font[4].render(string_count,1,self.m_image.get_at((dims[1]/2,dims[1]/2))),(resource_offset+dims[1],0))
			self.m_surf.blit(self.m_image,(0,0))

			self.m_stale_val = self.m_val

	def get_surface(self):

		self.update_surface()
		return self.m_surf

	def get(self):

		return int(self.m_val)

	def add(self, bonus):

		self.m_val += bonus


if __name__ == '__main__':

	pygame.init()
	pygame.font.init()
	random.seed()
	globals.screen_resolution = (1,1)
	globals.window_surface = pygame.display.set_mode((globals.screen_resolution[0],globals.screen_resolution[1]), 0, 32) 
	pygame.display.set_caption(globals.game_name)
	message("")
	r = Resource("Gold",pygame.image.load('Assets/Gold.png').convert_alpha(),0)
	pygame.image.save(r.get_surface(),""+r.m_name+".png")
	r.add(156)
	pygame.image.save(r.get_surface(),""+r.m_name+"2.png")

	r2 = Resource("Demon Hearts",pygame.image.load('Assets/Heart.png').convert_alpha(),0)
	pygame.image.save(r2.get_surface(),""+r2.m_name+".png")
	r2.add(3451289645398)
	pygame.image.save(r2.get_surface(),""+r2.m_name+"2.png")

	r3 = Resource("Gems",pygame.image.load('Assets/Gem.png').convert_alpha(),0)
	pygame.image.save(r3.get_surface(),""+r3.m_name+".png")
	r3.add(26)
	pygame.image.save(r3.get_surface(),""+r3.m_name+"2.png")
