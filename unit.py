import random
import copy

import pygame
import pygame.time
from pygame.locals import *
import pygame.mouse

import globals
from timer import *
from util import *

class attribute(object):
    
    def __init__(self, owner, base=100, growth=0, bonus=0):

        self.m_owner = owner;
        self.m_base = int(base);
        self.m_growth = growth;
        self.m_bonus = int(bonus);

    def get(self):

        return int(self.m_base+self.m_bonus+self.m_growth*self.m_owner.m_level)

    def add(self, bonus):
        
        self.m_bonus += int(bonus)

    def reset(self):

        self.m_bonus = 0

    def __str__(self):

        return str(self.get());


class Unit(object):

    def __init__(self, attribs, level=0):

        self.m_attribs=attribs
        self.m_level = level

        for attrib in self.m_attribs.keys():
            if(type(self.m_attribs[attrib]) is int):
                self.m_attribs[attrib]=attribute(self,self.m_attribs[attrib])
            else:
                self.m_attribs[attrib]=attribute(self,self.m_attribs[attrib][0],self.m_attribs[attrib][1])

    def set(self, attrib, value):

        self.m_attribs[attrib]=value

    def get(self, attrib):

        value = self.m_attribs.get(attrib)
        
        if(value == None):
            return 0
            
        return value.get()

    def copy(self):

        otr = copy.deepcopy(self)

        for attrib in otr.m_attribs.keys():

            otr.m_attribs[attrib].m_owner = otr

        return otr

    def __str__(self):

        string = "L:"+self.m_level
        string = "HP: "+str(self.m_attribs["health"])
        string += "/"+str(self.m_attribs["armour"])
        string += "\t\tSpeed: "+str(self.m_attribs["movement_speed"])+"%"
        string += "\t\tAttack: "+str(self.m_attribs["attack_damage"])+"/"+str(self.m_attribs["attack_speed"])+"%"
        return string

class Actor_Unit(Unit):

    def __init__(self, attribs, level=0):

        Unit.__init__(self, attribs, level)

        self.m_bonus = []
        self.m_current_health = self.get("health")

    def append(self, unit):

        self.m_bonus.append(unit)
        self.recalc_bonus()

    def reset(self):

        self.m_bonus = []
        self.recalc_bonus()

    def recalc_bonus(self):

        for attrib in self.m_attribs.keys():

            self.m_attribs[attrib].reset()

            for bonus in self.m_bonus:

                self.m_attribs[attrib].add(bonus.get(attrib))

    def level_up(self):

        oldHP = self.get("health")

        self.m_level += 1

        self.m_current_health *= float(self.get("health"))/oldHP

    def attack(self, target_unit, mult=1.0):

        if(self.m_current_health > 0):
            base_damage = self.get("attack_damage")
            damage = random.uniform(base_damage*18.0,base_damage*22.0)/20
            damage *= mult
            damage = int(max( damage - target_unit.get("armour"), 1))
            target_unit.m_current_health = max(target_unit.m_current_health-damage,0)
            return damage

        else:
            return 0


source_unit_nme          = Actor_Unit({"health":(80,1),  "armour":(8,0.4),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100})
source_unit_knight       = Actor_Unit({"health":(115,1), "armour":(20,0.4), "attack_speed":70,  "attack_damage":(40,1), "movement_speed":80 })
source_unit_warden       = Actor_Unit({"health":(100,1), "armour":(12,0.4), "attack_speed":90,  "attack_damage":(40,1), "movement_speed":100})
source_unit_zealot       = Actor_Unit({"health":(90,1),  "armour":(8,0.4),  "attack_speed":90,  "attack_damage":(44,1), "movement_speed":110})
source_unit_savage       = Actor_Unit({"health":(100,1), "armour":(8,0.4),  "attack_speed":90,  "attack_damage":(40,1), "movement_speed":120})
source_unit_friar        = Actor_Unit({"health":(150,1), "armour":(4,0.4),  "attack_speed":70,  "attack_damage":(28,1), "movement_speed":120})
source_unit_warlock      = Actor_Unit({"health":(100,1), "armour":(4,0.4),  "attack_speed":80,  "attack_damage":(61,1), "movement_speed":80 })
source_unit_ranger       = Actor_Unit({"health":(80,1),  "armour":(8,0.4),  "attack_speed":110, "attack_damage":(40,1), "movement_speed":110})
source_unit_scout        = Actor_Unit({"health":(100,1), "armour":(4,0.4),  "attack_speed":115, "attack_damage":(47,1), "movement_speed":800})
#source_unit_scout.append(Unit({"armour":8}))

player1 = source_unit_nme
player2 = source_unit_nme.copy()
for i in range(0,10):
    player2.level_up()

print player1
print player2,"\n"
print "\t\t\t\tHP 1:", player1.m_current_health,"\t\t",
print "\t\t\t\tHP 2:", player2.m_current_health

for i in range(0,5):
    
    print "2->1:",player2.attack(player1), "\t\tHP 1:", player1.m_current_health,"\t\t",
    print "1->2:",player1.attack(player2), "\t\tHP 2:", player2.m_current_health
