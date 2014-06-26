import random
import copy

import pygame
import pygame.time
from pygame.locals import *
import pygame.mouse

import globals
from timer import *
from util import *
from game_object import *

class Game_Actor(Game_Object):

	def __init__(self, posn, name="Minion", icon=globals.sprite_cube, width = 20, unit=None):

		Game_Object.__init__(self, posn, name, icon, width)
		self.m_unit = unit

    def draw(self):
        
        Game_Object.draw(self)

    def input(self, event):

        Game_Object.input(self,event)

    def update(self, delta):

        Game_Object.update(self, delta)

    def __str__(self):

        return self.m_name+"<#"+self.m_id+">\n"+str(self.m_unit)