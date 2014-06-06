import globals
import random
import copy


def clamp(l,m,g):
	
	return max(l,min(g,m))


def random_icon():
	
	return "Assets/Game-Icons/"+globals.icon_list[random.randint(0,len(globals.icon_list)-1)]

