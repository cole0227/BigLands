import sys
import random
import copy
import time
import os
from multiprocessing import Process, Queue

import pygame
from pygame.locals import *

import pygame.time
import pygame.font

import globals
from sprite_sheet import *
from tile_map import *
from roman import *
from game_object import *
from screen import *
from game import *
from timer import *


def main_init():

    #inline definitions for button functions

    def game_screen():
        globals.current_screen = "Game"

    def new_game_screen():
        globals.current_screen = "New Game"

    def nothing():
        pass

    def make_map(q=96):

        #q = Queue()
        p = Process(target=generate_map,args=(q,))
        p.start()

    def make_map_small():
        make_map(128)

    def make_map_medium():
        make_map(192)

    def make_map_big():
        make_map(256)

    def make_map_huge():
        make_map(512)

    def make_map_colossal():
        make_map(1024)

    #core initiation
    pygame.init()
    pygame.font.init()
    random.seed()

    #set up the window
    globals.screen_resolution = (600,400)
    globals.window_surface = pygame.display.set_mode((globals.screen_resolution[0],globals.screen_resolution[1]), 0, 32) 
    pygame.display.set_caption(globals.game_name)
    message("")

    #Load in Sprites:
    globals.sprite_cube = pygame.image.load('Assets/GreenBox.png').convert_alpha()
    globals.sprite_tree = pygame.image.load('Assets/Tree.png').convert_alpha()
    globals.sprite_house = pygame.image.load('Assets/House2.png').convert_alpha()
    globals.sprite_road = pygame.image.load('Assets/Brown_Road.png').convert_alpha()
    globals.sprite_icon = pygame.image.load(random_icon())
    globals.sprite_icon.convert_alpha()
    globals.sprite_icon.set_colorkey((0,0,0))

    globals.icons_iu = Sprite_Sheet("Assets/Game-Icons-Mods/icon_underlays.png","Alpha")
    globals.icons_ut = Sprite_Sheet("Assets/Game-Icons-Mods/underlays.png","Alpha")
    globals.icons_ov = Sprite_Sheet("Assets/Game-Icons-Mods/overlays2.png","Alpha")
    globals.icons_corner_chunk = Sprite_Sheet("Assets/Game-Icons-Mods/corners.png","Alpha")
    globals.icons_overtest = pygame.image.load("Assets/Game-Icons-Mods/overlays2.png")

    globals.icons_overtest.convert_alpha()

    print "Loaded Sprites"

    # Make the Screens
    Screen("Main Menu").add()

    globals.screens["Main Menu"].add_button(Button("Big Lands",(20,20),nothing,7))
    globals.screens["Main Menu"].add_button(Button("Play",(60,100),game_screen))
    globals.screens["Main Menu"].add_button(Button("New Game",(60,150),new_game_screen))
    globals.screens["Main Menu"].add_button(Button("Quit",(60,200),main_quit))

    Screen("New Game").add()
    globals.screens["New Game"].add_button(Button("New Game",(20,20),nothing,7))
    globals.screens["New Game"].add_button(Button("Make Tiny Map",(60,100),make_map))
    globals.screens["New Game"].add_button(Button("Make Small Map",(60,150),make_map_small))
    globals.screens["New Game"].add_button(Button("Make Medium Map",(60,200),make_map_medium))
    globals.screens["New Game"].add_button(Button("Make Big Map",(60,250),make_map_big))
    globals.screens["New Game"].add_button(Button("Make Huge Map",(60,300),make_map_huge))
    globals.screens["New Game"].add_button(Button("Make Colossal Map",(60,350),make_map_colossal))

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
            last = time.clock()
            util = 0
            

if __name__ == '__main__':

    main_init()
    main_game_loop()