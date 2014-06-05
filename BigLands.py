import sys
import random
import copy

import pygame
from pygame.locals import *

import pygame.time
import pygame.font

from spritesheet import SpriteSheet
from roman import *
import globals
from game_object import *
from screen import *
from game import *


def main_init():

    def game_screen():
        globals.current_screen = "Game"

    def nothing():
        pass

    pygame.init()
    pygame.font.init()
    random.seed()

    globals.window_surface = pygame.display.set_mode((globals.screen_resolution[0],globals.screen_resolution[1]), 0, 32) 
    pygame.display.set_caption(globals.game_name)

    # Make the Screens
    Screen("Main Menu").add()

    globals.screens["Main Menu"].add_button(Button("Big Lands",(20,20,1,1),game_screen,6))
    globals.screens["Main Menu"].add_button(Button("Play",(60,100,70,45),game_screen,4))
    globals.screens["Main Menu"].add_button(Button("Quit",(60,150,70,45),main_quit,4))
    globals.current_screen = "Main Menu"
    Game("Game").add()

    #Load in Sprites:
    globals.sprite_cube = pygame.transform.scale(pygame.image.load('Assets/GreenBox.png'), (10, 10)).convert_alpha()

def main_quit():

    pygame.quit() 
    sys.exit()


def main_input():

    for event in pygame.event.get():

        globals.screens[globals.current_screen].input(event)

        if event.type == QUIT: 

            main_quit()

        elif event.type == KEYDOWN:

            if(event.key == K_F12):

                main_quit()

            elif(event.key == K_F2):

                globals.game_pause

            elif(event.key == K_ESCAPE):

                globals.current_screen = "Main Menu"


def main_game_loop():

    clock = pygame.time.Clock()

    while( True ):

        clock.tick(globals.frame_rate)

        main_input()

        if(globals.game_pause == False):
            
            globals.screens[globals.current_screen].update(clock.get_time())

        globals.window_surface.fill((0,0,100))
        globals.screens[globals.current_screen].draw()
        pygame.display.update()

if __name__ == '__main__':

    main_init()
    main_game_loop()