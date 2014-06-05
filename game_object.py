import random

import pygame
import pygame.time
from pygame.locals import *

import globals
from timer import *

class Game_Object(object):

    def __init__(self,pos,name="An Object"):
        
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

        if( sqrt((self.m_pos[0] - gameObj.m_pos[0]) ** 2 +
                 (self.m_pos[1] - gameObj.m_pos[1]) ** 2) <
                 (gameObj.m_width + self.m_width)/2 ):

            print "Collision Alert"

    def draw(self):
        
        globals.window_surface.blit(globals.sprite_cube, (self.m_pos[0]-self.m_width/2,self.m_pos[1]-self.m_width/2))

    def update(self, delta):

        pass

    def input(self,event):

        pass

    def __str__(self):

        return self.m_name

class Game_Actor(Game_Actor):

    def __init__(self, posn, name="Minion", health=100, armour=0, attack_damage=10, attack_speed=0):

        Game_Object.__init__(self, posn, name)
        self.m_health = health
        self.m_armour = armour
        self.m_attack_damage = attack_damage
        self.m_attack_speed = attack_speed

    def attack(self, source):

        self.m_health =
            min(self.m_health,
            source.m_attack_damage * 100 / (100+self.m_armour)
