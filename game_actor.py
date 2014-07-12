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
        self.m_attack_timer = Timer(400/(unit.get("attack_speed")+100))

    def draw(self):
        
        Game_Object.draw(self)

    def input(self, event):

        Game_Object.input(self,event)

        if (event.type == KEYDOWN):
            if(event.key == K_F5):
                print self.m_unit.m_current_health


    def update(self, delta):

        Game_Object.update(self, delta)

        if(self.m_unit.m_current_health <= 0):
            self.m_delete = True
            print "Time to Die"

    def collide(self, other):

        collision = Game_Object.collide(self,other)

        if( collision and not(other == self) and hasattr(other, "m_unit")):

            pass

    def attack(self, target, mult):
        print "Can Attack:", str(self.m_attack_timer)
        if(self.m_attack_timer.attempt_action()):

            print "Damage: ",self.m_unit.attack(target.m_unit,mult)


    def __str__(self):

        return self.m_name+"<#"+self.m_id+">\n"+str(self.m_unit)

class Player_Actor(Game_Actor):

    def __init__(self, posn, name="Minion", icon=globals.sprite_cube, width = 20, unit=None):

        Game_Actor.__init__(self, posn, name, icon, width, unit)

        self.m_target = [posn[0],posn[1]]


    def input(self, event):

        Game_Actor.input(self,event)

        if pygame.mouse.get_pressed()[0]:
            self.m_target = pygame.mouse.get_pos()

        elif pygame.mouse.get_pressed()[2]:
            print "Right Click"
            if(distance(self.m_pos,self.m_target) < self.m_unit.get("attack_range")):
                other = globals.screens["Game"].object_at(self.m_target)

                if(other != None and hasattr(other, "m_unit")):

                    self.attack(other,1.0)

            self.m_target = pygame.mouse.get_pos()            

    def update(self,delta):

        Game_Actor.update(self,delta)

        dx = self.m_target[0] - self.m_pos[0]
        dy = self.m_target[1] - self.m_pos[1]
        d = self.m_unit.get("movement_speed") * delta

        if (((dx)**2 + (dy) ** 2) ** 0.5 >= d):
            if( dx != 0 and dy != 0 ):
                self.move([dx/abs(dx) * d, dy/abs(dy) * d])
            elif( dx != 0 ):
                self.move([dx/abs(dx) * d, 0])
            elif( dy != 0 ):
                self.move([0, dy/abs(dy) * d])
        else: # we're not in a movement state
            pass

