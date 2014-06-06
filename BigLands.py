import sys
import random
import copy
import time

import pygame
from pygame.locals import *

import pygame.time
import pygame.font

import globals
from sprite_sheet import *
from roman import *
from game_object import *
from screen import *
from game import *
from timer import *


def main_init():

    def game_screen():
        globals.current_screen = "Game"

    def nothing():
        pass

    #core initiation
    pygame.init()
    pygame.font.init()
    random.seed()

    #set up the window
    globals.window_surface = pygame.display.set_mode((globals.screen_resolution[0],globals.screen_resolution[1]), 0, 32) 
    pygame.display.set_caption(globals.game_name)

    #Load in Sprites:
    globals.sprite_cube = pygame.image.load('Assets/GreenBox.png').convert_alpha()
    globals.sprite_icon = pygame.image.load(random_icon())
    globals.sprite_icon.convert_alpha()
    globals.sprite_icon.set_colorkey((0,0,0))
    print "Loaded Sprites"

    # Make the Screens
    Screen("Main Menu").add()

    globals.screens["Main Menu"].add_button(Button("Big Lands",(20,20,1,1),game_screen,7))
    globals.screens["Main Menu"].add_button(Button("Play",(60,100,70,45),game_screen,4))
    globals.screens["Main Menu"].add_button(Button("Quit",(60,150,70,45),main_quit,4))
    globals.current_screen = "Main Menu"
    Game("Game").add()
    print "Finished Init"

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

    util = 0
    last = time.clock()

    while( True ):


        clock.tick(globals.frame_rate)

        main_input()

        if(globals.game_pause == False):
            
            globals.screens[globals.current_screen].update(clock.get_time()/1000.0)

        globals.window_surface.fill((0,0,100))
        globals.screens[globals.current_screen].draw()
        pygame.display.update()

        util =+ clock.get_rawtime()/1000.0
        if (last<time.clock()-5):
            print "Utilization:",float(int(10000.0/(time.clock()-last)*util))/100,"%"
            util = 0
            last = time.clock()


if __name__ == '__main__':

    main_init()
    main_game_loop()