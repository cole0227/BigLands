import random
import glob
import os


import pygame
import pygame.time
import pygame.font
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.display.init()

global screen_resolution
screen_resolution = (random.randint(1024,1680),random.randint(768,1050))

global frame_rate
frame_rate = 120

global game_name
game_name = "Big Lands"

global game_pause
game_pause = False

global id_game_object
id_game_object = 0;

global window_surface
window_surface = None

global basic_font
basic_font = []
for i in range (0, 12):
    basic_font.append(pygame.font.SysFont("Arial", i*7+12))
global heavy_font
heavy_font = []
for i in range (0, 12):
    heavy_font.append(pygame.font.SysFont("Arial Black", i*7+12))

global current_screen
current_screen = 0

global screens
screens = {}

global sprite_cube
sprite_cube = None

global sprite_icon
sprite_icon = None

global icon_list
icon_list = []
prev = os.getcwd()
os.chdir("Assets/Game-Icons")
icon_list.extend(glob.glob("*.png"))
os.chdir(prev)
