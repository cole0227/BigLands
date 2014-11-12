import random
import copy
import pickle

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

    def __init__(self,name,level, count_attribs_limit=3, stat_limits=-1, starting_attribs={}):

        self.m_name = name
        self.m_level = level
        self.m_unit = Unit(starting_attribs,level)

        self.m_count_attribs_limit = count_attribs_limit
        if(stat_limits == -1):
            self.m_stat_limits=[1.5,3.0,1.5,2.0]
        else:
            self.m_stat_limits=stat_limits

    def add(self,string,attrib_name,attrib_mult=1.0, minimum=1):

        name = self.m_name.lower()
        instances = name.count(string)

        if(instances >= minimum):

            self.m_unit.merge_attrib(attrib_name,Attribute(self.m_unit,
                random.uniform(self.m_stat_limits[0]*attrib_mult,self.m_stat_limits[1]*attrib_mult),
                random.uniform(self.m_stat_limits[2]*attrib_mult,self.m_stat_limits[3]*attrib_mult)))

    def gen(self):

        self.add("a","precision")
        self.add("a","precision",0.3,minimum=2)
        self.add("b","constitution")
        self.add("b","constitution",0.3,minimum=2)
        self.add("e","might")
        self.add("e","might",0.3,minimum=3)
        self.add("n","finesse")
        self.add("n","finesse",0.3,minimum=3)
        self.add("s","agility")
        self.add("s","agility",0.3,minimum=3)
        self.add("t","toughness")
        self.add("t","toughness",0.3,minimum=3)

        self.add("p","attack_damage",4)
        self.add("g","attack_damage",4)
        self.add("j","attack_damage",4)
        self.add("o","attack_speed",3)

        self.add("k","movement_speed",0.6)
        self.add("c","movement_speed",0.6)

        self.add("l","critical_chance",0.4)
        self.add("u","critical_damage",2)
        self.add("r","critical_damage",2)
        self.add("f","critical_damage",2)

        self.add("i","dodge_chance",0.4)

        self.add("h","health",20)
        self.add("h","health",15,minimum=2)
        self.add("q","health",20)
        self.add("q","health",15,minimum=2)
        self.add("v","health_regeneration",0.4)
        self.add("w","health_regeneration",0.4)

        self.add("d","armour",0.5)
        self.add("d","armour",0.3,minimum=2)
        self.add("x","armour",0.5)
        self.add("x","armour",0.3,minimum=2)
        self.add("y","armour",0.5)
        self.add("y","armour",0.3,minimum=2)
        self.add("z","armour",0.5)
        self.add("z","armour",0.3,minimum=2)

        if(self.m_count_attribs_limit < len(self.m_unit.m_attribs.keys())):
            #selecting N from the highlighted attributes
            keys=random.sample(self.m_unit.m_attribs.keys(),self.m_count_attribs_limit)
            for key in self.m_unit.m_attribs.keys():
                if not(key in keys):
                    del self.m_unit.m_attribs[key]


        return self

    def get(self):

        return self.m_unit

    def __str__(self):

        return self.m_unit.output_attribs()

# Attribs:
#
# unit
# name
# image
#
class Ability (object):
    
    def __init__(self,power_count=3,downside_count=0):

            gen = self.gen(power_count)
            if(downside_count > 0):

                gen[0].merge(self.gen(-downside_count)[0])

            pygame.image.save(gen[1],"Saved Games/0/Abilities/"+gen[0].m_name+".png")

            # Pickle to store things in files
            write_file("Saved Games/0/Abilities/"+gen[0].m_name+".pkl",gen[0])
            read = read_file("Saved Games/0/Abilities/"+gen[0].m_name+".pkl")

            self.unit = gen[0]
            self.name = gen[0].m_name
            self.image= gen[1]

    def gen(self,power_count=6):

        #generate an icon
        ico_vals = save_icon_double()
        #print ico_vals

        #manipulate the string
        ico_vals[0] = ico_vals[0][:-4] + random.choice([random.choice([" with "," and "," of "," for "]) + ico_vals[3][:-4]," "+ico_vals[3][:-4],""])
        ico_vals[0] = ico_vals[0].replace("-"," ").replace("_"," ").replace("dice six faces ","").replace("perspective ","")
        eff = random.randint(0,len(Effect)-1)
        ico_vals[0] = Effect[eff]+" "+ico_vals[0]

        if(ico_vals[1] > 13):
            ico_vals[0] = "Mega "+ico_vals[0]
        elif(ico_vals[1] > 9):
            ico_vals[0] = "Penta "+ico_vals[0]
        elif(ico_vals[1] > 5):
            ico_vals[0] = "Octo "+ico_vals[0]
        elif(ico_vals[1] < 3):
            ico_vals[0] = "Core "+ico_vals[0]

        # colour
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
        blank = Actor_Unit({"health":0,  "health_regeneration":0, "armour":0,  "attack_speed":0, "attack_damage":0, "movement_speed":0, "critical_chance":0, "critical_damage":0, "dodge_chance":0},name=ico_vals[0])

        #print ico_vals[0]
        if(power_count >= 2):
            i = Ability_Unit_Builder(Effect[eff],0,2,stat_limits=[3,5,2.0,2.5]).gen()
            b = blank.copy()
            b.merge(i.get())
            #print i.get().output_attribs()
            u = Ability_Unit_Builder(ico_vals[0],0,power_count-2).gen()
            blank.merge(u.get())
            blank.merge(b)
        elif(power_count == 1):
            blank.merge(Ability_Unit_Builder(Effect[eff],0,1,stat_limits=[3,5,2.0,2.5]).gen().get())
        elif(power_count < 0):
            blank.merge(Ability_Unit_Builder(Effect[eff],0,-power_count,stat_limits=[-2,-4,-1.5,-2.0]).gen().get())

        return blank,ico_vals[4]

if __name__ == '__main__':

    pygame.init()
    pygame.font.init()
    random.seed()
    globals.screen_resolution = (1,1)
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

    gen = Ability(3,2).unit
    print gen.m_name
    print gen.output_attribs()
    gen.m_level = 2
    print gen.output_attribs()
    #print gen[0].output_attribs()
    #pygame.image.save(gen[1],"Saved Games/0/Abilities/"+gen[0].m_name+".png")

    # Pickle to store things in files
    #write_file("Saved Games/0/Abilities/"+gen[0].m_name+".pkl",gen[0])
    #print read_file("Saved Games/0/Abilities/"+gen[0].m_name+".pkl")