import random
import copy

import pygame
import pygame.time
from pygame.locals import *
import pygame.mouse

import globals
from timer import *
from util import *
from unit import *

Effect = ("Tough", "Enduring", "Immortal",
          "Fertile", "Verdant", "Overgrown",
          "Shiny", "Glowing", "Sparkling",
          "Solar", "Lunar", "Starlit", "Martian", "Shadow",
          "Heated", "Flaming", "Molten",
          "Sparking", "Arcing", "Thunderous",
          "Chill", "Frosty", "Frigid",
          "Sharp", "Keen", "Dismembering",
          "Normal", "Fire", "Fighting", "Water", "Flying", "Grass", "Poison", "Electric", "Ground", "Psychic", "Rock", "Ice", "Bug", "Dragon", "Ghost", "Dark", "Steel", "Fairy",
          "Gooey","Slimey","Lesser","Greater","Giant","Tiny","Oozing","Spikey","Cosmic","Melting","Smelly","Stinky","Crusty")

class Ability_Unit_Builder(object):

    def __init__(self,name,level, count_attribs_limit=2, starting_attribs={}):

        self.m_name = name
        self.m_level = level
        self.m_unit = Unit(starting_attribs,level)

        self.m_count_attribs = 0
        self.m_count_attribs_limit = count_attribs_limit

    def add(self,string,attrib_name,attrib, minimum=1, weight=1, min_value = 3.0):

        name = self.m_name.lower()
        instances = name.count(string)

        if(instances >= minimum and self.m_count_attribs < self.m_count_attribs_limit):
            if(attrib.get() >= min_value):
                self.m_unit.merge_attrib(attrib_name,attrib)
                self.m_count_attribs+=weight


    def gen(self):

        stat_limits=[1,3,0.5,1.5]
        self.add("a","charisma",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])))
        self.add("a","charisma",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])),minimum=2,weight=0)
        self.add("b","constitution",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])))
        self.add("e","wisdom",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])))
        self.add("e","wisdom",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])),minimum=3,weight=0)
        self.add("n","intelligence",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])))
        self.add("n","intelligence",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])),minimum=3,weight=0)
        self.add("s","dexterity",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])))
        self.add("s","dexterity",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])),minimum=3,weight=0)
        self.add("t","strength",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])))

        self.add("p","attack_damage",Attribute(self.m_unit,random.uniform(stat_limits[0]*2,stat_limits[1]*3),random.uniform(stat_limits[2],stat_limits[3])))
        self.add("o","attack_speed",Attribute(self.m_unit,random.uniform(stat_limits[0]*2,stat_limits[1]*3),random.uniform(stat_limits[2],stat_limits[3])))
        self.add("r","critical_damage",Attribute(self.m_unit,random.uniform(stat_limits[0]*2,stat_limits[1]*3),random.uniform(stat_limits[2],stat_limits[3])))
        self.add("k","critical_chance",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])))

        self.add("g","critical_chance",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])))
        self.add("u","dodge_chance",Attribute(self.m_unit,random.uniform(stat_limits[0],stat_limits[1]),random.uniform(stat_limits[2],stat_limits[3])))

        self.add("f","health",Attribute(self.m_unit,random.uniform(stat_limits[0]*5,stat_limits[1]*5),random.uniform(stat_limits[2]*4,stat_limits[3]*6)))
        self.add("h","health",Attribute(self.m_unit,random.uniform(stat_limits[0]*5,stat_limits[1]*5),random.uniform(stat_limits[2]*4,stat_limits[3]*6)))
        self.add("h","health",Attribute(self.m_unit,random.uniform(stat_limits[0]*5,stat_limits[1]*5),random.uniform(stat_limits[2]*4,stat_limits[3]*6)),minimum=2)
        self.add("q","health",Attribute(self.m_unit,random.uniform(stat_limits[0]*5,stat_limits[1]*5),random.uniform(stat_limits[2]*4,stat_limits[3]*6)))
        self.add("i","health_regen",Attribute(self.m_unit,random.uniform(stat_limits[0]/2.0,stat_limits[1]/2.0),random.uniform(stat_limits[2]/2.0,stat_limits[3]/2.0)))
        self.add("v","health_regen",Attribute(self.m_unit,random.uniform(stat_limits[0]/2.0,stat_limits[1]/2.0),random.uniform(stat_limits[2]/2.0,stat_limits[3]/2.0)))
        self.add("w","health_regen",Attribute(self.m_unit,random.uniform(stat_limits[0]/2.0,stat_limits[1]/2.0),random.uniform(stat_limits[2]/2.0,stat_limits[3]/2.0)))

        self.add("x","armour",Attribute(self.m_unit,random.uniform(stat_limits[0]/2.0,stat_limits[1]/2.0),random.uniform(stat_limits[2]/2.0,stat_limits[3]/2.0)))
        self.add("x","armour",Attribute(self.m_unit,random.uniform(stat_limits[0]/2.0,stat_limits[1]/2.0),random.uniform(stat_limits[2]/2.0,stat_limits[3]/2.0)),minimum=2,weight=0)
        self.add("y","armour",Attribute(self.m_unit,random.uniform(stat_limits[0]/2.0,stat_limits[1]/2.0),random.uniform(stat_limits[2]/2.0,stat_limits[3]/2.0)))
        self.add("y","armour",Attribute(self.m_unit,random.uniform(stat_limits[0]/2.0,stat_limits[1]/2.0),random.uniform(stat_limits[2]/2.0,stat_limits[3]/2.0)),minimum=2,weight=0)
        self.add("z","armour",Attribute(self.m_unit,random.uniform(stat_limits[0]/2.0,stat_limits[1]/2.0),random.uniform(stat_limits[2]/2.0,stat_limits[3]/2.0)))
        self.add("z","armour",Attribute(self.m_unit,random.uniform(stat_limits[0]/2.0,stat_limits[1]/2.0),random.uniform(stat_limits[2]/2.0,stat_limits[3]/2.0)),minimum=2,weight=0)

        return self

    def __str__(self):

        return self.m_unit.output_attribs()

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    random.seed()
    globals.screen_resolution = (1300,600)
    globals.window_surface = pygame.display.set_mode((globals.screen_resolution[0],globals.screen_resolution[1]), 0, 32) 
    pygame.display.set_caption(globals.game_name)
    message("")
    globals.icons_iu = Sprite_Sheet("Assets/Game-Icons-Mods/icon_underlays.png","Alpha")
    globals.icons_ut = Sprite_Sheet("Assets/Game-Icons-Mods/underlays.png","Alpha")
    globals.icons_ov = Sprite_Sheet("Assets/Game-Icons-Mods/overlays2.png","Alpha")
    globals.icons_corner_chunk = pygame.image.load("Assets/Game-Icons-Mods/corners.png")
    globals.icons_corner_chunk.convert_alpha()
    globals.icons_overtest = pygame.image.load("Assets/Game-Icons-Mods/overlays2.png")
    globals.icons_overtest.convert_alpha()

    #generate an icon
    ico_vals = save_icon_double()
    print ico_vals

    #manipulate the string
    ico_vals[0] = ico_vals[0][:-4] + random.choice([" with "," and "," of "," ajoined "]) + ico_vals[3][:-4]
    ico_vals[0] = ico_vals[0].replace("-"," ").replace("_"," ").replace("dice six faces ","")
    ico_vals[0] = Effect[random.randint(0,len(Effect)-1)]+" "+ico_vals[0]
    if(ico_vals[1] > 13):
        ico_vals[0] = "Mega "+ico_vals[0]
    elif(ico_vals[1] > 9):
        ico_vals[0] = "Penta "+ico_vals[0]
    elif(ico_vals[1] > 5):
        ico_vals[0] = "Octo "+ico_vals[0]
    elif(ico_vals[1] < 3):
        ico_vals[0] = "Base "+ico_vals[0]

    if(ico_vals[2]%6<1):
        ico_vals[0] = "Blue "+ico_vals[0]
    elif(ico_vals[2]%6<2):
        ico_vals[0] = "Purple "+ico_vals[0]
    elif(ico_vals[2]==2):
        ico_vals[0] = "Orange "+ico_vals[0]
    elif(ico_vals[2]%6<3):
        ico_vals[0] = "Red "+ico_vals[0]
    elif(ico_vals[2]%6<4):
        ico_vals[0] = "Yellow "+ico_vals[0]
    elif(ico_vals[2]%6<5):
        ico_vals[0] = "Green "+ico_vals[0]
    else:
        ico_vals[0] = "Aqua "+ico_vals[0]

    ico_vals[0] = ico_vals[0].title()

    #output results    
    print ico_vals[0]
    print Ability_Unit_Builder(ico_vals[0],1).gen()
    print Ability_Unit_Builder(ico_vals[0],10).gen()
