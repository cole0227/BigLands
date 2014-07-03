import random

import pygame
import pygame.time
import pygame.font
from pygame.locals import *

import globals
from screen import *
from game_object import *
from unit import *
from game_actor import *
from sprite_sheet import *

class Game(Screen):

    def __init__(self, name):

        Screen.__init__(self, name)
        self.m_game_objects = []
        self.add_object(Game_Object([100,100]))
        self.add_object(Player_Actor([random.randint(0,300),random.randint(0,300)],"Dude1",pygame.image.load(random_icon()),random.randint(1,50),Actor_Unit({"health":(80,1),  "armour":(12,0.4),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100})))
        self.add_object(Game_Actor([random.randint(0,300),random.randint(0,300)],"Dude2",pygame.image.load(random_icon()),random.randint(1,30),Actor_Unit({"health":(80,1),  "armour":(8,0.4),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100})))
        self.add_object(Game_Actor([random.randint(0,300),random.randint(0,300)],"Dude3",pygame.image.load(random_icon()),random.randint(1,30),Actor_Unit({"health":(80,1),  "armour":(8,0.4),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100})))


    def add_object(self, game_object):

        self.m_game_objects.append(game_object)

    def input(self, event):

        for obj in self.m_game_objects:
            obj.input(event)

        if (event.type == KEYDOWN):
            if(event.key == K_F3):
                save_icon()
            if(event.key == K_F4):
                pygame.image.save(globals.window_surface,"Screenshots/"+str(pygame.time.get_ticks())+".png")

        Screen.input(self, event)

    def update(self, delta):

        for obj in self.m_game_objects:
            obj.update(delta)

            for obj2 in self.m_game_objects:
                obj.collide(obj2)

        for i in range(0,len(self.m_game_objects)-1):
            if(self.m_game_objects[i].m_delete == True):
                self.m_game_objects.pop(i)

        Screen.update(self, delta)

    def draw(self):

        for obj in self.m_game_objects:
            obj.draw()

        Screen.draw(self)