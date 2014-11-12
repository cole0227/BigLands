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
            if(event.key == K_F6):
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
        self.m_leftHoldFrames = 0;
        self.m_rightHoldFrames = 0;


    def input(self, event):

        Game_Actor.input(self,event)

    def update(self,delta):

        Game_Actor.update(self,delta)

        if pygame.mouse.get_pressed()[0]: # left click

            self.m_leftHoldFrames += 1
        else:
            if  self.m_leftHoldFrames > 0:
                print "Left Tap",self.m_leftHoldFrames
            self.m_leftHoldFrames = 0

        if self.m_leftHoldFrames >= globals.time_hold_mouse_button*globals.frame_rate:
                
            print "Left Hold"
            self.m_leftHoldFrames = 0

        if pygame.mouse.get_pressed()[2]: # right click

            self.m_rightHoldFrames += 1
        else:
            if self.m_rightHoldFrames > 0:
                print "Right Tap",self.m_rightHoldFrames
            self.m_rightHoldFrames = 0

        if self.m_rightHoldFrames >= globals.time_hold_mouse_button*globals.frame_rate:

            print "Right Hold"
            self.m_rightHoldFrames = 0

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

