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
import game_object
import screen


def main_init():

    pygame.init()
    pygame.font.init()
    random.seed()

    globals.window_surface = pygame.display.set_mode((globals.screen_resolution[0],globals.screen_resolution[1]), 0, 32) 
    pygame.display.set_caption(globals.game_name)

def main_quit():

    pygame.quit() 
    sys.exit()


def main_input():

    for event in pygame.event.get():

        if event.type == QUIT: 

            main_quit()

        elif event.type == KEYDOWN:

            if(event.key == K_F12):

                main_quit()


def main_update(delta):

    print("#Update")

def main_draw():

    print("#Draw")

def main_game_loop():

    clock = pygame.time.Clock()

    while( True ):

        clock.tick(globals.frame_rate)

        main_input()

        if(globals.game_pause == False):
            main_update(clock.get_time())

        main_draw()

if __name__ == '__main__':

    main_init()
    main_game_loop()