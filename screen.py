import random

import pygame
import pygame.time
from pygame.locals import *

import globals

class button(object):

	def ___init___(self,text,rect):

		self.m_text = globals.basic_font[3].render(text),1,(240,220,200))
		self.m_rect = rect

	def draw(self):
		
		globals.window_surface.blit(self.text,rect[:2])

class Screen(object):

	def ___init___(self,name):

		self.m_name = name
		self.m_buttons = []

	def input(self, event):

		pass

	def update(self, delta):

		pass

	def draw(self):

		for button in self.m_buttons

			button.draw()