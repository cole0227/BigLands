import random

import pygame
import pygame.time
import pygame.font
from pygame.locals import *

import globals
from screen import *
from game_object import *

class Game(Screen):

    def __init__(self, name):

        Screen.__init__(self, name)
        self.m_game_objects = []

    def add_object(self, game_object):

        self.m_game_objects.append(game_object)

    def input(self, event):

        for obj in self.m_game_objects:
            obj.input(event)

        Screen.input(self, event)

    def update(self, delta):

        for obj in self.m_game_objects:
            obj.input(delta)

        Screen.update(self, delta)

    def draw(self):

        for obj in self.m_game_objects:
            obj.draw()

        Screen.draw(self)
