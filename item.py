import random
import copy
import pickle
import re

import pygame
import pygame.time
from pygame.locals import *
import pygame.mouse

import globals
from timer import *
from util import *
from unit import *
from ability import *

column_type_name = ["ring","ring","ring","sling","boots","boots",
"sword","sword","sword","sword","sword","sword","knife","knife","knife",
"totem","wand","wand","wand","armour","armour","book","book","book","book","book","book","book","book","book","book","gem","sigil","sigil","sigIl","sigIl","Sigil","Sigil","siGil","siGil","sigiL","sigiL"]

def make_item(bonus_count = 4, level = 0):
	col = random.randint(0,len(column_type_name)-1)
	row = random.randint(0,7)

	effect_number = random.randint(0,len(Effect)-1)

	name = column_type_name[col]
	if(bonus_count > 4):
		name = Effect[effect_number] + " " + column_type_name[col]

	negatives = 1
	item_unit = None

	if(bonus_count > 4):

		item_unit = Ability(bonus_count-1,negatives,(name,effect_number)).unit
		attr = Effect_Attrib[Effect[effect_number]]
		if(attr == "health_regeneration" or attr == "armour" or attr == "movement_speed" or attr == "critical_chance" or attr == "dodge_chance"):
			item_unit.merge(Unit({attr:Attribute(item_unit,2.5,1.2)}))
		if(attr == "health"):
			item_unit.merge(Unit({attr:Attribute(item_unit,80,40)}))
		else:
			item_unit.merge(Unit({attr:Attribute(item_unit,5,2.5)}))

	else:

		item_unit = Ability(bonus_count,negatives,(name,effect_number)).unit

	item_unit.level_up(level)
	item_unit.clear_bonus()

	unit_title_name = (item_unit.output_attribs()).split("\n",1)

	if(len(unit_title_name)>1):
		unit_title_name = "".join(re.split("\(|\)",unit_title_name[1])[0::2])
		if(bonus_count > 2):
			attr = item_unit.random_attrib()
			if((col == 19 or col == 20)):
				name = name[:-6]+random.choice(("cuirass", "plate", "outfit"))
			if(attr == "armour" or attr == "dodge_chance"):
				name += random.choice((" of Protection"," of Defense"," of Defiance"))
			else:
				name += " of " + attr
		else:
			name = random.choice(("Worn", "Old", "Musty", "Bent", "Cracked"))+" "+name
		name = name.replace("_"," ").title()

		print (name+" ["+str(item_unit.m_level)+"]\n"+unit_title_name).replace("_"," ").title()
	else:
		print name.title()
	print

	icon = globals.icons_items.image_by_coords(60,col,row)
	icon.blit(globals.icons_items_outlines,(0,0),(60*(3-bonus_count/2),0,60,60))
	icon.blit(globals.icons_items_outlines,(1,1),(60*(3-bonus_count/2),0,60,60))
	icon.blit(globals.icons_items_outlines,(-1,-1),(60*(3-bonus_count/2),0,60,60))
	pygame.image.save(icon,"Saved Games/0/Items/"+name+".png")
	write_file("Saved Games/0/Items/"+name+".pkl",item_unit)
	return name,item_unit,icon


pygame.init()
pygame.font.init()
random.seed()
globals.screen_resolution = (1,1)
globals.window_surface = pygame.display.set_mode((globals.screen_resolution[0],globals.screen_resolution[1]), 0, 32) 
pygame.display.set_caption(globals.game_name)
message("")
globals.icons_items = Sprite_Sheet("Assets/PD/Free_Icons.png")
globals.icons_items_outlines = pygame.image.load("Assets/PD/Free_Icons_Outlines.png")
globals.icons_items_outlines.set_colorkey((0,0,0))
globals.icons_items_outlines = globals.icons_items_outlines.convert_alpha()
for i in range(10):
	make_item(0)
	make_item(1)
	make_item(2)
	make_item(5)
	make_item(5,2)
