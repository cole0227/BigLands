import random
import copy

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

        self.m_id = globals.id_game_object
        globals.id_game_object += 1

    def get_rect(self):

        return(self.x,self.y,self.m_width,self.m_width)

    def to_dict(self):
        
        return {self.m_id:self}

    def collide(self, gameObj):

        return (sqrt((self.m_pos[0] - gameObj.m_pos[0]) ** 2 +
                 (self.m_pos[1] - gameObj.m_pos[1]) ** 2) <
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


class Game_Actor(Game_Object):

    def __init__(self, posn, name="Minion", icon=globals.sprite_cube, width = 20, movement_speed = 15, health=100, armour=0, attack_damage=10, attack_speed=0):

        Game_Object.__init__(self, posn, name, icon, width)

        self.m_health = health
        self.m_armour = armour
        self.m_attack_damage = attack_damage
        self.m_attack_speed = attack_speed
        self.m_target = [posn[0],posn[1]]
        self.m_movement_speed = movement_speed * 1.0

        self.m_atack_timer = Timer(2+100/(100+attack_speed))

    def adjust(health=None, armour=None, attack_damage=None, attack_speed=None):

        if(health != None):
            m_health = health

        elif(armour != None):
            m_armour = armour

        elif(attack_damage != None):
            m_attack_damage = attack_damage

        elif(attack_speed != None):
            m_attack_speed = attack_speed

    def attack(self, source):

        self.m_health = min(self.m_health,
            source.m_attack_damage * 100 / (100+self.m_armour))

    def input(self, event):

        Game_Object.input(self,event)

        if pygame.mouse.get_pressed()[0]:
            self.m_target = pygame.mouse.get_pos()
            


    def update(self, delta):

        Game_Object.update(self, delta)

        dx = self.m_target[0] - self.m_pos[0]
        dy = self.m_target[1] - self.m_pos[1]
        d = self.m_movement_speed * delta

        if (((dx)**2 + (dy) ** 2) ** 0.5 >= d):
            if( dx != 0 and dy != 0 ):
                self.move([dx/abs(dx) * d, dy/abs(dy) * d])
            elif( dx != 0 ):
                self.move([dx/abs(dx) * d, 0])
            elif( dy != 0 ):
                self.move([0, dy/abs(dy) * d])
        else:
            pass#self.m_pos = self.m_target
                
