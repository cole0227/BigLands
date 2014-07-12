import random
import copy
import math

import pygame
import pygame.time
from pygame.locals import *
import pygame.mouse

import globals
from timer import *
from util import *

class Game_Object(object):

    def __init__(self,pos,name="An Object", icon=None, width = 20):
        
        if(icon==None):
            icon = globals.sprite_cube

        self.m_pos = pos
        self.m_name = name
        self.m_active = True
        self.m_width = width
        self.m_icon = pygame.transform.scale(icon,(width,width))
        self.m_icon.convert_alpha()
        self.m_icon.set_colorkey((0,0,0))

        print self.m_pos

        self.m_delete = False

        self.m_id = globals.id_game_object
        globals.id_game_object += 1

    def get_rect(self):

        return( (self.m_pos[0]-self.m_width/2,self.m_pos[1]-self.m_width/2,self.m_width/2,self.m_width/2) )

    def to_dict(self):
        
        return {self.m_id:self}

    def collide(self, gameObj):

        return (((self.m_pos[0] - gameObj.m_pos[0]) ** 2 +
                 (self.m_pos[1] - gameObj.m_pos[1]) ** 2) ** (0.5) <
                 (gameObj.m_width + self.m_width)/2)

    def move(self, delta):

        self.m_pos[0] = self.m_pos[0] + delta[0]
        self.m_pos[1] = self.m_pos[1] + delta[1]

    def draw(self):
        
        globals.window_surface.blit(self.m_icon, (int(self.m_pos[0]-self.m_width/2),int(self.m_pos[1]-self.m_width/2)))

    def update(self, delta):

        pass

    def input(self,event):

        pass

    def __str__(self):

        return self.m_name+"<#"+self.m_id+">"

class Bullet_Object(Game_Object):
    
    def __init__(self,pos,name="An Object", icon=None, width = 20, source=None, damage=(1.0), ):

        Game_Object.__init__(self,pos,name,icon,width)