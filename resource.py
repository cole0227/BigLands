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

			if(self.m_name == ""):
				string_name = ""

			string_count = self.get()
			dims = globals.basic_font[7].size(string_name+string_count)

			# only the first time
			if(self.m_stale_val == -42):
				self.m_image = pygame.transform.scale(self.m_image,(dims[1],dims[1]));

			resource_offset = globals.basic_font[7].size(string_name)[0]
			m_surf = pygame.Surface((dims[0]+dims[1]+2,dims[1]+2),SRCALPHA,32).convert_alpha()
			m_surf.blit(globals.basic_font[7].render(string_name+string_count,1,(0,0,0)),(dims[1]+2,2))
			m_surf.blit(globals.basic_font[7].render(string_name,1,(240,230,140)),(dims[1],0))
			m_surf.blit(globals.basic_font[7].render(string_count,1,self.m_image.get_at((dims[1]/2,dims[1]/2))),(resource_offset+dims[1],0))
			m_surf.blit(self.m_image,(0,0))

			self.m_stale_val = self.m_val

			return m_surf

		else:
			return self.m_surf

	def get_surface(self):

		self.m_surf = self.update_surface()
		return self.m_surf

	def get_cost_surface(self, cost):
		self.m_stale_val = -1
		val_temp = self.m_val
		self.m_val = cost
		name_temp = self.m_name
		self.m_name = ""
		surf = self.update_surface()
		self.m_val = val_temp
		self.m_name = name_temp
		return surf


	def get(self):

		multiple_names = ["K", "M", "G", "T", "P", "E", "Z", "Y"]
		def make_str(i,c=0):
			val = i / (1000.0**c)
			if(c >= len(multiple_names)):
				return str(i)[:4]
			if(val>999):
				return make_str(i,c+1)
			elif(val < 10 and val != int(val)):
				return str(val)[:3]+multiple_names[c]
			elif(val < 100 and val != int(val)):
				return str(val)[:2]+multiple_names[c]
			elif(i<1000):
				return str(int(i))
			else:
				return str(int(val))[:3]+multiple_names[c]

		return make_str(int(self.m_val))

	def add(self, bonus):

		self.m_val += bonus

class Square_Resource(Resource):

	def __init__(self, name, image, val=0, rarity=3):

		Resource.__init__(self, name, image, val)
		self.m_rarity = rarity

	def update_surface(self):


		if(self.m_val != self.m_stale_val):
			string_count = str(self.get())
			dims = globals.basic_font[7].size(string_count)
			w = int(dims[1]*3)
			#w=60

			# only the first time
			if(self.m_stale_val == -42):
				self.m_image = pygame.transform.scale(self.m_image,(w,w));
				temp_surf = pygame.transform.scale(globals.icons_items_outlines,(w*4,w))
				self.m_image.blit(temp_surf, (0,0),   (w*(3-(self.m_rarity)), 0, w, w))
				self.m_image.blit(temp_surf, (-1,-1),   (w*(3-(self.m_rarity)), 0, w, w))
				self.m_image.blit(temp_surf, (1,1),   (w*(3-(self.m_rarity)), 0, w, w))

			m_surf = pygame.Surface((w,w),SRCALPHA,32).convert_alpha()
			m_surf.blit(self.m_image,(0,0))
			shadow = globals.basic_font[7].render(string_count,1,(0,0,0))
			m_surf.blit(shadow,(w-dims[0]-4+2,w-dims[1]+4+2))
			#m_surf.blit(shadow,(w-dims[0]-4-2,w-dims[1]+4-2))
			#m_surf.blit(shadow,(w-dims[0]-4+2,w-dims[1]+4-2))
			#m_surf.blit(shadow,(w-dims[0]-4-2,w-dims[1]+4+2))
			m_surf.blit(globals.basic_font[7].render(string_count,1,(240,230,140)),(w-dims[0]-4,w-dims[1]+4))#self.m_image.get_at((w/2,w/2))),(w-dims[0]-4,w-dims[1]+4))

			self.m_stale_val = self.m_val

			return m_surf

		else:
			return self.m_surf

if __name__ == '__main__':

	pygame.init()
	pygame.font.init()
	random.seed()
	globals.screen_resolution = (1,1)
	globals.window_surface = pygame.display.set_mode((globals.screen_resolution[0],globals.screen_resolution[1]), 0, 32) 
	pygame.display.set_caption(globals.game_name)
	message("")
	globals.icons_items_outlines = pygame.image.load("Assets/PD/Free_Icons_Outlines.png")
	globals.icons_items_outlines.set_colorkey((0,0,0))
	globals.icons_items_outlines = globals.icons_items_outlines.convert_alpha()

	r = Resource("Gold",pygame.image.load('Assets/Gold.png').convert_alpha(),0)
	pygame.image.save(r.get_surface(),""+r.m_name+".png")
	r.add(1560)
	pygame.image.save(r.get_surface(),""+r.m_name+"2.png")
	r.add(98760000)
	pygame.image.save(r.get_surface(),""+r.m_name+"3.png")
	r.add(9876000000)
	pygame.image.save(r.get_surface(),""+r.m_name+"4.png")
	r.add(9876000000000)
	pygame.image.save(r.get_surface(),""+r.m_name+"5.png")
	r.add(76999000000000000)
	pygame.image.save(r.get_surface(),""+r.m_name+"6.png")
	r.add(9876000000000000000)
	pygame.image.save(r.get_surface(),""+r.m_name+"7.png")
	pygame.image.save(r.get_cost_surface(12),""+r.m_name+"_cost.png")

	r2 = Resource("Demon Hearts",pygame.image.load('Assets/Heart.png').convert_alpha(),0)
	pygame.image.save(r2.get_surface(),""+r2.m_name+".png")
	r2.add(3451289645398)
	pygame.image.save(r2.get_surface(),""+r2.m_name+"2.png")

	r3 = Resource("Gems",pygame.image.load('Assets/Gem.png').convert_alpha(),0)
	pygame.image.save(r3.get_surface(),""+r3.m_name+".png")
	r3.add(26)
	pygame.image.save(r3.get_surface(),""+r3.m_name+"2.png")
