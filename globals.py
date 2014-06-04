import random

import pygame
import pygame.time
import pygame.font
from pygame.locals import *


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

pygame.font.init()
global basic_font
basic_font = []
for i in range (0, 7):
    basic_font.append(pygame.font.SysFont("Arial", i*7+12))
global heavy_font
heavy_font = []
for i in range (0, 7):
    heavy_font.append(pygame.font.SysFont("Arial Black", i*7+12))

global current_screen
current_screen = 0

global screens
screens = {}