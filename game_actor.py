import random
import copy
import math
import sys

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
        self.m_stun_timer = Timer(0.2)
        self.m_stun_timer.set(0) # set the timer to have run on January 1st, 1970

    def draw(self):
        shakeX,shakeY = 0,0
        if(not self.m_stun_timer.test()):
            shakeX = random.randint(-2,2)
            shakeY = random.randint(-2,2)
            
        globals.window_surface.blit(self.m_icon, (int(self.m_pos[0]-self.m_width/2)+shakeX,int(self.m_pos[1]-self.m_width/2)+shakeY))

    def input(self, event):

        Game_Object.input(self,event)

        if (event.type == KEYDOWN):
            if(event.key == K_F6):
                print self.m_unit.m_current_health


    def update(self, delta):
        # set m_disabled before calling up the heirarchy
        self.m_disabled = (self.m_stun_timer.test() or self.m_animation_lock < 0)
        Game_Object.update(self, delta)
        self.m_animation_lock -= delta;
    def update_action(self, delta):

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
            target.m_stun_timer.trigger()
            target.m_stun_timer.set(0.2)
            self.m_stun_timer.trigger()
            self.m_stun_timer.set(0.05)

    def __str__(self):

        return self.m_name+"<#"+str(self.m_id)+">\n"+str(self.m_unit)

class Player_Actor(Game_Actor):

    def __init__(self, posn, name="Minion", icon=globals.sprite_cube, width = 20, unit=None):

        Game_Actor.__init__(self, posn, name, icon, width, unit)

        self.m_target = [posn[0],posn[1]]
        self.m_leftHoldFrames = 0
        self.m_rightHoldFrames = 0
        self.m_mouse_pos = (0,0)

    def input(self, event):

        Game_Actor.input(self,event)

    def update(self,delta):

        Game_Actor.update(self,delta)
        self.m_mouse_pos = pygame.mouse.get_pos()

            

    def update_action(self, delta):

        Game_Actor.update_action(self, delta)
        
        # clicking actions
        if pygame.mouse.get_pressed()[0]: # left click
            self.m_leftHoldFrames += 1
        else:
            if  self.m_leftHoldFrames > 0:
                if():
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

        dx = float(self.m_target[0] - self.m_pos[0])
        dy = float(self.m_target[1] - self.m_pos[1])
        dBoth = float(dx**2+dy**2)**(0.5)
        d = self.m_unit.get("movement_speed") * delta

        if (dBoth >= d):
            if( dx != 0 and dy != 0 ):
                self.move([d/dBoth*dx, d/dBoth*dy])
            elif( dx != 0 ):
                self.move([dx/abs(dx) * d, 0])
            elif( dy != 0 ):
                self.move([0, dy/abs(dy) * d])
        else: # we're not in a movement state
            #print "Reseting Target to Self"
            self.m_target = self.m_pos

    def left_click(self):

        distance = (self.m_pos[0]-self.m_mouse_pos[0])**2+(self.m_pos[1]-self.m_mouse_pos[1])**2
        clickedOn = globals.screens["Game"].object_at(self.m_mouse_pos,self)

        if(clickedOn != None and type(clickedOn) is Game_Actor and (self.m_unit.get("attack_range")+self.m_width/2.0+clickedOn.m_width/2.0+1)**2 > distance):
            print "Attack the thing with " + str(clickedOn.m_unit.get("health")) + "HP"
            Game_Actor.attack(self, clickedOn, 1)
            self.m_animation_lock = 1.5
        else:
            self.m_target = self.m_mouse_pos
            if(clickedOn != None):
                #naive targeting
                self.m_target = [clickedOn.m_pos[0],clickedOn.m_pos[1]]
                
                distance = ((self.m_pos[0]-self.m_target[0])**2+(self.m_pos[1]-self.m_target[1])**2 )**0.5
                slope = ((self.m_target[0]-self.m_pos[0])/distance,(self.m_target[1]-self.m_pos[1])/distance)
                x = self.m_target[0]-slope[0]*(self.m_unit.get("attack_range")+self.m_width/2.0+clickedOn.m_width/2.0+1)
                y = self.m_target[1]-slope[1]*(self.m_unit.get("attack_range")+self.m_width/2.0+clickedOn.m_width/2.0+1)
                self.m_target = [x,y]


    def right_click(self):
        print "Right Click"
        self.m_animation_lock = 0.9
        for obj in globals.screens["Game"].objects_in_circle(self.m_mouse_pos,200,self):
            obj.m_animation_lock = 1.0

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