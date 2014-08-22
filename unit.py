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

        return int(self.m_base+self.m_bonus+self.m_growth*self.m_owner.m_level);

    def merge(self,attrib):

        self.m_base += attrib.m_base;
        self.m_growth += attrib.m_growth;
        self.m_bonus += attrib.m_bonus;

    def add(self, bonus):
        
        self.m_bonus += int(bonus);

    def reset(self):

        self.m_bonus = 0;

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

    def output_attribs(self):

        string = "Level:"+str(self.m_level)
        for key in self.m_attribs.keys():
            string +="\n"+str(key)+": "+str(self.m_attribs[key])

        return string


    def __str__(self):

        string = "Level:"+str(self.m_level)
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

        oldHP = self.get("health")

        for attrib in self.m_attribs.keys():

            self.m_attribs[attrib].reset()

            for bonus in self.m_bonus:

                self.m_attribs[attrib].add(bonus.get(attrib))

        if "strength" in self.m_attribs:

            self.m_attribs["health"].add(self.get("strength"))
            self.m_attribs["armour"].add(self.get("strength"))

        if "dexterity" in self.m_attribs:

            self.m_attribs["attack_speed"].add(2*self.get("dexterity"))
            self.m_attribs["movement_speed"].add(2*self.get("dexterity"))

        if "constitution" in self.m_attribs:

            self.m_attribs["health"].add(3*self.get("constitution"))

        if "intelligence" in self.m_attribs:

            self.m_attribs["attack_speed"].add(self.get("intelligence"))
            self.m_attribs["dodge_chance"].add(self.get("intelligence"))

        if "wisdom" in self.m_attribs:

            self.m_attribs["attack_damage"].add(3*self.get("wisdom"))

        if "charisma" in self.m_attribs:

            self.m_attribs["critical_chance"].add(self.get("charisma"))
            self.m_attribs["critical_damage"].add(2*self.get("charisma"))

        self.m_current_health *= float(self.get("health"))/oldHP

    def merge(self,unit):

        oldHP = self.get("health")

        for attrib in unit.m_attribs.keys():
            if attrib in self.m_attribs:
                self.m_attribs[attrib].merge(unit.m_attribs[attrib])
            else:
                self.m_attribs[attrib]=unit.m_attribs[attrib]

        self.m_current_health *= float(self.get("health"))/oldHP

    def level_up(self):

        oldHP = self.get("health")

        self.m_level += 1

        self.m_current_health *= float(self.get("health"))/oldHP

    def attack(self, target_unit, mult=1.0):

        if(self.m_current_health > 0):
            base_damage = self.get("attack_damage")
            damage = random.uniform(base_damage*18.0,base_damage*22.0)/20
            damage *= mult

            if(self.get("critical_chance") > 100):
                    damage *= (self.get("critical_damage")+self.get("critical_chance"))/100
            elif( random.random() < self.get("critical_chance")/100.0):
                damage *= (100+self.get("critical_damage"))/100

            if( random.random() < target_unit.get("dodge_chance")/100.0):

                target_unit.m_current_health -= 1
                return 1

            damage = int(max( damage - target_unit.get("armour"), 1))
            target_unit.m_current_health = max(target_unit.m_current_health-damage,0)
            return damage

        else:
            return 0

if __name__ == '__main__':

    source_unit_nme          = Actor_Unit({"health":(80,1),  "armour":(8,0.4),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_knight       = Actor_Unit({"health":(115,1), "armour":(20,0.4), "attack_speed":70,  "attack_damage":(40,1), "movement_speed":80 , "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_warden       = Actor_Unit({"health":(100,1), "armour":(12,0.4), "attack_speed":90,  "attack_damage":(40,1), "movement_speed":100, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_zealot       = Actor_Unit({"health":(90,1),  "armour":(8,0.4),  "attack_speed":90,  "attack_damage":(44,1), "movement_speed":110, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_savage       = Actor_Unit({"health":(100,1), "armour":(8,0.4),  "attack_speed":90,  "attack_damage":(40,1), "movement_speed":120, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_friar        = Actor_Unit({"health":(150,1), "armour":(4,0.4),  "attack_speed":70,  "attack_damage":(28,1), "movement_speed":120, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_warlock      = Actor_Unit({"health":(100,1), "armour":(4,0.4),  "attack_speed":80,  "attack_damage":(61,1), "movement_speed":80 , "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_ranger       = Actor_Unit({"health":(80,1),  "armour":(8,0.4),  "attack_speed":110, "attack_damage":(40,1), "movement_speed":110, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_scout        = Actor_Unit({"health":(100,1), "armour":(4,0.4),  "attack_speed":115, "attack_damage":(47,1), "movement_speed":130, "critical_chance":50, "critical_damage":150, "dodge_chance":0})
    #source_unit_scout.append(Unit({"armour":8}))

    source_class_shepherd   = Unit({"strength":(1,1.0), "dexterity":(1,1.0), "constitution":(1,1.0), "intelligence":(1,1.0), "wisdom":(3,1.8), "charisma":(3,1.8)})
    source_class_brigand    = Unit({"strength":(3,2.2), "dexterity":(1,1.0), "constitution":(3,2.2), "intelligence":(1,1.0), "wisdom":(1,1.0), "charisma":(1,1.0)})
    source_class_moonbrain  = Unit({"strength":(1,1.2), "dexterity":(1,1.4), "constitution":(1,1.2), "intelligence":(3,1.7), "wisdom":(3,1.7), "charisma":(1,1.2)})
    source_class_veteran    = Unit({"strength":(1,1.0), "dexterity":(1,1.0), "constitution":(3,1.8), "intelligence":(1,1.0), "wisdom":(1,1.0), "charisma":(3,1.8)})
    source_class_monk_river = Unit({"strength":(1,1.0), "dexterity":(3,1.7), "constitution":(1,1.2), "intelligence":(3,1.7), "wisdom":(1,1.0), "charisma":(1,1.0)})
    source_class_monk_wind  = Unit({"strength":(1,0.9), "dexterity":(3,1.8), "constitution":(1,1.3), "intelligence":(1,0.9), "wisdom":(3,1.8), "charisma":(1,0.9)})
    source_class_monk_leaf  = Unit({"strength":(1,1.0), "dexterity":(3,1.8), "constitution":(3,2.2), "intelligence":(1,1.0), "wisdom":(1,1.0), "charisma":(1,1.0)})
    source_class_settler    = Unit({"strength":(1,1.0), "dexterity":(1,1.0), "constitution":(3,1.8), "intelligence":(1,1.0), "wisdom":(3,1.8), "charisma":(1,1.0)})
    source_class_reaver     = Unit({"strength":(3,1.8), "dexterity":(3,1.8), "constitution":(1,1.0), "intelligence":(1,1.0), "wisdom":(1,1.0), "charisma":(1,1.0)})
    source_class_agent      = Unit({"strength":(1,0.9), "dexterity":(1,0.9), "constitution":(1,0.9), "intelligence":(5,2.9), "wisdom":(1,0.9), "charisma":(1,0.9)})
    source_class_ambassador = Unit({"strength":(1,0.9), "dexterity":(1,0.9), "constitution":(1,0.9), "intelligence":(1,0.9), "wisdom":(1,0.9), "charisma":(5,2.9)})
    #source_unit_nme.merge(source_unit_knight)
    source_unit_nme.merge(source_class_reaver)
    print source_unit_nme
    source_unit_nme.recalc_bonus()
    print source_unit_nme
    print

    player1 = source_unit_scout
    player2 = source_unit_nme.copy()
    for i in range(0,10):
        player2.level_up()

    print player1
    print player2,"\n"
    print player2.output_attribs()
    print "\t\t\t\tHP 1:", player1.m_current_health,"\t\t",
    print "\t\t\t\tHP 2:", player2.m_current_health

    for i in range(0,5):
        
        print "2->1:",player2.attack(player1), "\t\tHP 1:", player1.m_current_health,"\t\t",
        print "1->2:",player1.attack(player2), "\t\tHP 2:", player2.m_current_health
