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

Effect_Attrib = {"Tough":"health",
        "Enduring":"health",
        "Immortal":"health",
        "Fertile":"health_regeneration",
        "Verdant":"health_regeneration",
        "Overgrown":"health_regeneration",
        "Shiny":"health",
        "Glowing":"health",
        "Sparkling":"movement_speed",
        "Solar":"movement_speed",
        "Lunar":"movement_speed",
        "Starlit":"movement_speed",
        "Martian":"health_regeneration",
        "Shadow":"movement_speed",
        "Heated":"attack_damage",
        "Flaming":"attack_damage",
        "Molten":"attack_damage",
        "Sparking":"movement_speed",
        "Arcing":"movement_speed",
        "Thunderous":"attack_damage",
        "Chill":"health",
        "Frosty":"health",
        "Frigid":"health",
        "Sharp":"attack_damage",
        "Keen":"attack_damage",
        "Dismembering":"attack_damage",
        "Normal":"health",
        "Fire":"attack_damage",
        "Fighting":"health",
        "Water":"health",
        "Flying":"health",
        "Grass":"health",
        "Poison":"constitution",
        "Electric":"attack_damage",
        "Ground":"health",
        "Psychic":"precision",
        "Rock":"constitution",
        "Ice":"health",
        "Bug":"health",
        "Dragon":"movement_speed",
        "Ghost":"health",
        "Dark":"health",
        "Steel":"movement_speed",
        "Fairy":"health",
        "Gooey":"movement_speed",
        "Slimey":"movement_speed",
        "Lesser":"agility",
        "Greater":"toughness",
        "Giant":"constitution",
        "Tiny":"agility",
        "Oozing":"toughness",
        "Spikey":"health",
        "Cosmic":"precision",
        "Melting":"agility",
        "Smelly":"might",
        "Stinky":"might",
        "Crusty":"finesse"}

attribute_multiplier = {"health": 8,
                        "health_regeneration": 0.4,
                        "armour": 0.3,
                        "attack_speed": 3,
                        "attack_damage": 3,
                        "movement_speed": 0.6,
                        "critical_chance": 0.4,
                        "critical_damage": 2,
                        "dodge_chance": 0.4,
                        "finesse": 0.4,
                        "agility": 0.4,
                        "precision": 0.4,
                        "constitution": 0.4,
                        "toughness": 0.4,
                        "might": 0.4}

class Ability_Unit_Builder(object):

    def __init__(self,name,level, count_attribs_limit=3, stat_limits=-1, starting_attribs={},force_power=None):

        self.force_power = force_power
        self.m_name = name
        self.m_level = level
        self.m_unit = Unit(starting_attribs,level)

        self.m_count_attribs_limit = count_attribs_limit

        if(stat_limits == -1):
            self.m_stat_limits=[1.5,3.0,1.5,2.0]
        else:
            self.m_stat_limits=stat_limits

    def add(self,string,attrib_name,attrib_mult=1.0, minimum=1):
        
        attrib_mult = attribute_multiplier[attrib_name]
        name = self.m_name.lower()
        instances = name.count(string)

        if(instances >= minimum): # && self.m_unit.get(attrib_name) != 0 # <- prevents overly strong attributes
            attr = Attribute(self.m_unit,
                             random.uniform(self.m_stat_limits[0]*attrib_mult,self.m_stat_limits[1]*attrib_mult),
                             random.uniform(self.m_stat_limits[2]*attrib_mult,self.m_stat_limits[3]*attrib_mult))
            if(attr.get() != 0 and self.m_count_attribs_limit + 2 >= len(self.m_unit.m_attribs.keys())):
                self.m_unit.merge_attrib(attrib_name,attr)


    def gen(self):
        
        self.add("ring", "health_regeneration", 0.5)
        self.add("armour", "armour", 0.5)
        self.add("sword", "attack_damage", 4)
        self.add("knife", "attack_speed", 3)
        self.add("wand", "critical_chance", 0.4)
        self.add("sling", "critical_damage", 2)
        self.add("boots", "movement_speed", 0.6)
        self.add("gem", "health", 20)
        self.add("book", "finesse", 0.5)
        self.add("book", "precision", 0.5)
        self.add("totem", "constitution")
        self.add("sigil", "might")
        self.add("sigIl", "toughness")
        self.add("Sigil", "agility")
        self.add("siGil", "finesse")
        self.add("sigiL", "precision")

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

        if(self.force_power != None):
            #delete a random power
            del self.m_unit.m_attribs[random.choice(self.m_unit.m_attribs.keys())]
            #then add our new one
            print 
            self.add("",self.force_power)



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
    
    def __init__(self,power_count=3,downside_count=0,name=None,force_power=None):

            self.force_power = force_power
            if(name == None):
                self.name = self.gen_name()
            else:
                self.name = name[0]
                self.eff = name[1]
            gen = self.gen(power_count)

            if(downside_count > 0):
                gen.merge(self.gen(-downside_count))

            if(name == None):
                pygame.image.save(self.image,"Saved Games/0/Abilities/"+gen.m_name+".png")

                # Pickle to store things in files
                write_file("Saved Games/0/Abilities/"+gen.m_name+".pkl",gen)
                read = read_file("Saved Games/0/Abilities/"+gen.m_name+".pkl")

            self.unit = gen

    def gen_name(self):

        #generate an icon
        ico_vals = save_icon_double()
        #print ico_vals

        #manipulate the string
        ico_vals[0] = ico_vals[0][:-4] + random.choice([random.choice([" with "," and "," of "," for "]) + ico_vals[3][:-4]," "+ico_vals[3][:-4],""])
        ico_vals[0] = ico_vals[0].replace("-"," ").replace("_"," ").replace("dice six faces ","").replace("perspective ","")
        eff = random.randint(0,len(Effect)-1)
        self.eff = eff
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

        self.name = ico_vals[0].title()
        self.image = ico_vals[4]
        return self.name
    
    def gen(self,power_count=6):

        #make a unit for ability work    
        blank = Actor_Unit({"health":0,  "health_regeneration":0, "armour":0,  "attack_speed":0, "attack_damage":0, "movement_speed":0, "critical_chance":0, "critical_damage":0, "dodge_chance":0},name=self.name)

        if(power_count >= 4):
            special_power = random.sample((("lifesteal",[5,1]),
                                           ("overpower",[5,1])#,
                                           #("sleep_5_second",[2.5,0.5]),
                                           #("sleep_2_second",[5,1]),
                                           #("slow_20_percent_5_second",[10,2])
                                           ),1)
            special_power = {special_power[0][0]:special_power[0][1]}
            #print special_power
            i = Ability_Unit_Builder(Effect[self.eff],0,2,stat_limits=[3,5,2.0,2.5],starting_attribs=special_power,force_power=self.force_power).gen()
            b = blank.copy()
            b.merge(i.get())
            #print i.get().output_attribs()
            u = Ability_Unit_Builder(self.name,0,power_count-2).gen()
            blank.merge(u.get())
            blank.merge(b)
        elif(power_count < 0):
            blank.merge(Ability_Unit_Builder(Effect[self.eff],0,-power_count,stat_limits=[-2,-4,-1.5,-2.0]).gen().get())
        else:
            blank.merge(Ability_Unit_Builder(Effect[self.eff],0,power_count,stat_limits=[3,5,2.0,2.5]).gen().get())

        return blank

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
    gen.m_level = 1
    print gen.output_attribs()
    #print gen[0].output_attribs()
    #pygame.image.save(gen[1],"Saved Games/0/Abilities/"+gen[0].m_name+".png")

    # Pickle to store things in files
    #write_file("Saved Games/0/Abilities/"+gen[0].m_name+".pkl",gen[0])
    #print read_file("Saved Games/0/Abilities/"+gen[0].m_name+".pkl")