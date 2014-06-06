import random

import pygame
import pygame.time
import pygame.font
from pygame.locals import *

import globals
from screen import *
from game_object import *
from sprite_sheet import *

class Game(Screen):

    def __init__(self, name):

        Screen.__init__(self, name)
        self.m_game_objects = []
        self.add_object(Game_Object([100,100]))
        self.add_object(Game_Actor([random.randint(0,300),random.randint(0,300)],"Dude1",pygame.image.load(random_icon()),random.randint(1,300)))
        self.add_object(Game_Actor([random.randint(0,300),random.randint(0,300)],"Dude1",pygame.image.load(random_icon()),random.randint(1,300)))
        self.add_object(Game_Actor([random.randint(0,300),random.randint(0,300)],"Dude1",pygame.image.load(random_icon()),random.randint(1,300)))


    def add_object(self, game_object):

        self.m_game_objects.append(game_object)

    def input(self, event):

        for obj in self.m_game_objects:
            obj.input(event)

        Screen.input(self, event)

    def update(self, delta):

        for obj in self.m_game_objects:
            obj.update(delta)

        Screen.update(self, delta)

    def draw(self):

        for obj in self.m_game_objects:
            obj.draw()

        Screen.draw(self)