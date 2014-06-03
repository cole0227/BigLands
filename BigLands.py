import random

import pygame
import pygame.time
from pygame.locals import *

from spritesheet import SpriteSheet
from roman import *
import globals
import game_object
import screen

def main_input():

    for event in pygame.event.get():

        if event.type == QUIT: 
            pygame.quit() 
            sys.exit()


def main_update():

    print("#Update")

def main_draw():

    print("#Draw")

def main_game_loop():

    clock = pygame.time.Clock()

    while( True ):

        clock.tick(globals.frame_rate)

        main_input()

        main_update()

        main_draw()

if __name__ == '__main__':
    
    pygame.init()
    random.seed()

    globals.window_surface = pygame.display.set_mode((globals.screen_resolution[0],globals.screen_resolution[1]), 0, 32) 
    pygame.display.set_caption(globals.game_name)

    main_init()
    main_game_loop()