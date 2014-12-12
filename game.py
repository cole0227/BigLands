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
        self.add_object(Player_Actor([random.randint(0,300),random.randint(0,300)],"Dude1",pygame.image.load(random_icon()),random.randint(30,70),
            Actor_Unit({"health":(80,1),  "health_regeneration":(1,0.05), "armour":(8,0.1),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100, "critical_chance":0, "critical_damage":0, "dodge_chance":0, "attack_range":100})))
        self.add_object(  Game_Actor([random.randint(0,300),random.randint(0,300)],"Dude2",pygame.image.load(random_icon()),random.randint(30,70),
            Actor_Unit({"health":(80,1),  "health_regeneration":(1,0.05), "armour":(8,0.1),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100, "critical_chance":0, "critical_damage":0, "dodge_chance":0, "attack_range":100})))
        self.add_object(  Game_Actor([random.randint(0,300),random.randint(0,300)],"Dude3",pygame.image.load(random_icon()),random.randint(30,70),
            Actor_Unit({"health":(80,1),  "health_regeneration":(1,0.05), "armour":(8,0.1),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100, "critical_chance":0, "critical_damage":0, "dodge_chance":0, "attack_range":100})))


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

        self.m_game_objects = [ x  for x in self.m_game_objects if (not x.m_delete) ]

        '''
        rem = 0
        for i in xrange(len(self.m_game_objects) - rem):
            if (self.m_game_objects[i] is not None) and (self.m_game_objects[i].m_delete):
                self.m_game_objects.pop(i)
                rem += 1
                i   -= 1
        '''
        Screen.update(self, delta)

    def draw(self):

        for obj in self.m_game_objects:
            obj.draw()

        Screen.draw(self)

    def object_at(self, posn, source):

        for obj in self.m_game_objects:
            
            rect = obj.get_rect()

            if(obj != source and
               posn[0] > rect[0] and
               posn[0] < rect[0]+rect[2] and
               posn[1] > rect[1] and
               posn[1] < rect[1]+rect[3]):
                return obj

        return None

if __name__ == '__main__':

    import BigLands
    BigLands.main_init()
    BigLands.main_game_loop()