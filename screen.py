import random

import pygame
import pygame.time
from pygame.locals import *

import globals

class Button(object):

    def __init__(self,text,rect, action, size=5):

        self.m_text = globals.basic_font[size].render(text,1,(240,220,200))
        self.m_name = text
        self.m_rect = rect
        self.m_action = action

    def draw(self):

        globals.window_surface.blit(self.m_text,self.m_rect[:2])

    def act(self):

        self.m_action()

    def input(self, event):

        if(event.type == pygame.MOUSEBUTTONDOWN):

            if(event.pos[0] > self.m_rect[0] and event.pos[0] < self.m_rect[2] + self.m_rect[0]):

                if(event.pos[1] > self.m_rect[1] and event.pos[1] < self.m_rect[3] + self.m_rect[1]):

                    self.act()


class Screen(object):

    def __init__(self,name):

        self.m_name = name
        self.m_buttons = []

    def add(self):

        globals.screens.update({self.m_name:self})

    def add_button(self,button):

        self.m_buttons.append(button)

    def input(self, event):

        for button in self.m_buttons:

            button.input(event)

    def update(self, delta):

        pass

    def draw(self):

        for button in self.m_buttons:

	       button.draw()
