import random

import pygame
import pygame.time
from pygame.locals import *

import globals

class GameObject(object):

    def __init__(self,pos=(0,0),name="An Object"):
        
        self.m_pos = pos
        self.m_name = name
        self.m_active = True
        self.m_width = 10

        self.m_id = globals.id_game_object
        globals.id_game_object += 1

    def get_rect(self):

        return(self.x,self.y,self.m_width,self.m_width)

    def to_dict(self):
        
        return {self.m_id:self}

    def collide(self, gameObj):
        
        pass

    def draw(self):
        
        windowSurface.blit(g_sprite_cube, (self.m_pos[0]+23,self.m_pos[1]+23))

    def update(self, delta):

        pass

    def input(self,event):

        pass

    def __str__(self):

    	return self.m_name