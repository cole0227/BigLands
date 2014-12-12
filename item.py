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
from roman import int_to_roman as roman

column_type_name = ["ring","ring","ring","sling","boots","boots",
  "sword","sword","sword","sword","sword","sword","knife","knife","knife",
  "totem","wand","wand","wand","armour","armour",
  "book","book","book","book","book","book","book","book","book","book",
  "gem","sigil","sigil","sigIl","sigIl","Sigil","Sigil","siGil","siGil","sigiL","sigiL"]

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
		attr = Effect_Attrib[Effect[effect_number]]
		item_unit = Ability(bonus_count-1,negatives,(name,effect_number),force_power=attr).unit

	else:

		item_unit = Ability(bonus_count,negatives,(name,effect_number)).unit

	item_unit.level_up(level)
	item_unit.clear_bonus()
	bonus_count = item_unit.attrib_count()

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
		if(level > 0):
			name += " " + str(roman(level))

		print (name+"\n"+unit_title_name.replace("_"," ").title())
	else:
		name = name.title()
		if(level > 0):
			name += " " + str(roman(level))
		print name
	print

	icon = globals.icons_items.image_by_coords(60,col,row)
	icon.blit(globals.icons_items_outlines, (0,0),   (60*(3-(bonus_count+1)/2), 0, 60, 60))
	icon.blit(globals.icons_items_outlines, (2,2),   (60*(3-(bonus_count+1)/2), 0, 60, 60))
	icon.blit(globals.icons_items_outlines, (-2,-2), (60*(3-(bonus_count+1)/2), 0, 60, 60))
	icon.blit(globals.icons_items_outlines, (-2,2),  (60*(3-(bonus_count+1)/2), 0, 60, 60))
	icon.blit(globals.icons_items_outlines, (2,-2),  (60*(3-(bonus_count+1)/2), 0, 60, 60))
	icon.convert()
	#pygame.image.save(icon,"Saved Games/0/Items/"+name+".png")
	#write_file("Saved Games/0/Items/"+name+".pkl",item_unit)

	ret = (name, item_unit, icon, item_unit.attrib_count(), int(max(max(item_unit.m_level,0.5) * item_unit.attrib_count() * item_unit.attrib_count() * 10, 13)*random.uniform(0.7,1.3)))
	#has to be reset for the next item
	bonus_count = 4

	return ret
	# item( name, unit, icon, bonus count, cost )

class item_generator(object):

	def __init__(self,level=0, bonus_count=[0,66,99,42,24,15,7,3]):

		self.m_level = level
		self.m_bonus_count = bonus_count
		self.regen()

	def get(self):

		r = random.randint(0,len(self.d)-1);
		item = self.d[r]
		self.d.remove(item)
		return item

	def regen(self):

		self.d = []
		for z in range(len(self.m_bonus_count)):
			for i in range(self.m_bonus_count[z]):
				self.d.append(make_item(z,self.m_level))
		#print len(self.d)

	def __str__(self):

		string = ""
		for i in self.d:
			string += i[0]+" $"+str(i[4])+"\n"

		return string

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
for i in range(1):
	i = item_generator(0)
	print i
	for j in range(12):
		item = make_item(random.randint(1,6),random.randint(1,6))
		pygame.image.save(item[2],item[0]+".png")
