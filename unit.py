import random
import copy

import pygame
import pygame.time
from pygame.locals import *
import pygame.mouse

import globals
from timer import *
from util import *

class Unit(object):

	def __init__(self, health = 100):

		self.health = health