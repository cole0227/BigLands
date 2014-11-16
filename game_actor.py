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
from game_object import *

class Game_Actor(Game_Object):

    def __init__(self, posn, name="Minion", icon=globals.sprite_cube, width = 20, unit=None):

        Game_Object.__init__(self, posn, name, icon, width)
        self.m_unit = unit
        self.m_attack_timer = Timer(400/(unit.get("attack_speed")+100))
        self.m_animation_lock = 0

    def draw(self):
        
        Game_Object.draw(self)

    def input(self, event):

        Game_Object.input(self,event)

        if (event.type == KEYDOWN):
            if(event.key == K_F6):
                print self.m_unit.m_current_health


    def update(self, delta):

        Game_Object.update(self, delta)

        self.m_animation_lock -= delta;

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
        self.m_mouse_pos = (0,0)

    def input(self, event):

        Game_Actor.input(self,event)
    def update(self,delta):

        Game_Actor.update(self,delta)

        self.m_mouse_pos = pygame.mouse.get_pos()

        # clicking actions
        if pygame.mouse.get_pressed()[0]: # left click
            self.m_leftHoldFrames += 1
        else:
            if  self.m_leftHoldFrames > 0:
                if(self.m_animation_lock < 0):
                    self.left_click()
            self.m_leftHoldFrames = 0

        if self.m_leftHoldFrames >= globals.time_hold_mouse_button*globals.frame_rate:
            if(self.m_animation_lock < 0):
                self.left_hold()
                self.m_leftHoldFrames = 0

        if pygame.mouse.get_pressed()[2]: # right click
            self.m_rightHoldFrames += 1
        else:
            if self.m_rightHoldFrames > 0:
                if(self.m_animation_lock < 0):
                    self.right_click()
            self.m_rightHoldFrames = 0

        if self.m_rightHoldFrames >= globals.time_hold_mouse_button*globals.frame_rate:

            if(self.m_animation_lock < 0):
                self.right_hold()
                self.m_rightHoldFrames = 0

        dx = self.m_target[0] - self.m_pos[0]
        dy = self.m_target[1] - self.m_pos[1]
        dBoth = (dx**2+dy**2)**(0.5)
        d = self.m_unit.get("movement_speed") * delta

        if (dBoth >= d):
            if( dx != 0 and dy != 0 ):
                self.move([d/dBoth*dx, d/dBoth*dy])
            elif( dx != 0 ):
                self.move([dx/abs(dx) * d, 0])
            elif( dy != 0 ):
                self.move([0, dy/abs(dy) * d])
        else: # we're not in a movement state
            print "Reseting Target to Self"
            self.m_target = self.m_pos

    def left_click(self):
        distance = (self.m_pos[0]-self.m_mouse_pos[0])**2+(self.m_pos[1]-self.m_mouse_pos[1])**2
        if((self.m_unit.get("attack_range")+self.m_width/2.0+1)**2 > distance):
            clickedOn = globals.screens["Game"].object_at(self.m_mouse_pos,self)
            print "Close:",self.m_mouse_pos
            if(clickedOn != None):
                print "Attack!"
                self.m_animation_lock = 1.5

        else:
            clickedOn = globals.screens["Game"].object_at(self.m_mouse_pos,self)
            self.m_target = self.m_mouse_pos
            if(clickedOn != None):
                x = ((self.m_width)+self.m_unit.get("attack_range"))*(self.m_pos[0]-clickedOn.m_pos[0])/abs(self.m_pos[0]-clickedOn.m_pos[0])+clickedOn.m_pos[0]
                y = ((self.m_width)+self.m_unit.get("attack_range"))*(self.m_pos[1]-clickedOn.m_pos[1])/abs(self.m_pos[1]-clickedOn.m_pos[1])+clickedOn.m_pos[1] 
                self.m_target = [x,y]

    def right_click(self):
        print "Right Click"
        self.m_animation_lock = 0.9

    def left_hold(self):
        print "Left Hold"
        self.m_animation_lock = 1

    def right_hold(self):
        print "Right Hold"
        self.m_animation_lock = 2

if __name__ == '__main__':

    import BigLands
    BigLands.main_init()
    BigLands.main_game_loop()