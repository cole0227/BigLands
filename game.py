import random

import pygame
import pygame.time
import pygame.font
from pygame.locals import *

import globals
from screen import *
from game_object import *

class Game(Screen):

    def input(self, event):

    	Screen.input(self, event)

    def update(self, delta):

        Screen.update(self, delta)

    def draw(self):

        Screen.draw(self)
