import random

import pygame
import pygame.time
from pygame.locals import *


global screen_resolution
screen_resolution = (random.randint(1024,1680),random.randint(768,1050))

global frame_rate
frame_rate = 120

global game_name
game_name = "Big Lands"

global id_game_object
id_game_object = 0;