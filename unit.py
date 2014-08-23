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

        string = "Level: "+str(self.m_level)
        for key in self.m_attribs.keys():
            string +="\n"+str(key)+": "+str(self.m_attribs[key])

        return string


    def __str__(self):

        string = "Level:"+str(self.m_level)
        string += "\t\tHP: "+str(self.m_attribs["health"])
        string += " "+str(self.m_attribs["armour"])+"A "+str(self.m_attribs["dodge_chance"])+"D"
        string += "\t\tSpeed: "+str(self.m_attribs["movement_speed"])+"%"
        string += "\t\tAttack: "+str(self.m_attribs["attack_damage"])+"/"+str(self.m_attribs["attack_speed"])+"%"
        string += "\t\tCrits: "+str(100+self.m_attribs["critical_damage"].get())+"/"+str(self.m_attribs["critical_chance"])+"%"
        string += "\t\tHeroic Stats{"
        if("strength" in self.m_attribs):
            string += "S:"+str(self.m_attribs["strength"])+" "
        if("dexterity" in self.m_attribs):
            string += "D:"+str(self.m_attribs["dexterity"])+" "
        if("constitution" in self.m_attribs):
            string += "C:"+str(self.m_attribs["constitution"])+" "
        if("intelligence" in self.m_attribs):
            string += "I:"+str(self.m_attribs["intelligence"])+" "
        if("wisdom" in self.m_attribs):
            string += "W:"+str(self.m_attribs["wisdom"])+" "
        if("charisma" in self.m_attribs):
            string += "H:"+str(self.m_attribs["charisma"])+" "
        string += "}"

        return string

    def merge(self,unit):

        for attrib in unit.m_attribs.keys():
            if attrib in self.m_attribs:
                self.m_attribs[attrib].merge(unit.m_attribs[attrib])
            else:
                self.m_attribs[attrib]=unit.m_attribs[attrib]
                self.m_attribs[attrib].m_owner=self

    def level_up(self,level=1):

        self.m_level += level

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

        oldHP = self.m_current_health/float(self.get("health"))

        for attrib in self.m_attribs.keys():

            self.m_attribs[attrib].reset()

            for bonus in self.m_bonus:

                self.m_attribs[attrib].add(bonus.get(attrib))

        if "strength" in self.m_attribs:

            self.m_attribs["health"].add(self.get("strength")*4)
            self.m_attribs["armour"].add(self.get("strength")*0.1)

        if "dexterity" in self.m_attribs:

            self.m_attribs["attack_speed"].add(self.get("dexterity")*0.8)
            self.m_attribs["movement_speed"].add(self.get("dexterity"))

        if "constitution" in self.m_attribs:

            self.m_attribs["health"].add(self.get("constitution")*9)

        if "intelligence" in self.m_attribs:

            self.m_attribs["attack_speed"].add(self.get("intelligence")*0.4)
            self.m_attribs["dodge_chance"].add(self.get("intelligence")*0.3)

        if "wisdom" in self.m_attribs:

            self.m_attribs["attack_damage"].add(0.5*self.get("wisdom"))

        if "charisma" in self.m_attribs:

            self.m_attribs["critical_chance"].add(self.get("charisma")*0.5)
            self.m_attribs["critical_damage"].add(self.get("charisma")*0.4)

        self.m_current_health = float(self.get("health"))*float(oldHP)

    def merge(self,unit):

        oldHP = self.m_current_health/float(self.get("health"))

        for attrib in unit.m_attribs.keys():
            if attrib in self.m_attribs:
                self.m_attribs[attrib].merge(unit.m_attribs[attrib])
            else:
                self.m_attribs[attrib]=unit.m_attribs[attrib]
                self.m_attribs[attrib].m_owner=self

        self.m_current_health = float(self.get("health"))*float(oldHP)

    def level_up(self,level=1):

        oldHP = self.m_current_health/float(self.get("health"))

        self.m_level += level
        self.recalc_bonus()

        self.m_current_health = float(self.get("health"))*float(oldHP)

    def attack_ignore_armour(self, target_unit, mult=1.0):

        res = self.attack(target_unit, mult)
        target_unit.m_current_health = max(0,target_unit.m_current_health-target_unit.get("armour"))

        return (res[0]+target_unit.get("armour"),res[1])

    def attack(self, target_unit, mult=1.0):

        if(self.m_current_health > 0):
            base_damage = self.get("attack_damage")
            damage = random.uniform(base_damage*18.0,base_damage*22.0)/20
            damage *= mult
            message = "Hit"

            crit_mult=1.0
            if(self.get("critical_chance") > 100):
                    crit_mult += (self.get("critical_damage"))/100.0*self.get("critical_chance")/100
            if( random.random() < self.get("critical_chance")%100/100.0):
                crit_mult += (self.get("critical_damage"))/100.0
                message = "Crit"

            damage *= crit_mult

            if(target_unit.get("dodge_chance") > 100.0):

                damage /= 3.0**(target_unit.get("dodge_chance")/100)

            if( random.random() < target_unit.get("dodge_chance")%100/100.0):

                damage /= 3.0
                message = "Dodged"

            damage = int(max( damage - target_unit.get("armour"), 1))
            target_unit.m_current_health = max(target_unit.m_current_health-damage,0)
            return damage,message

        else:
            return 0,"Dead"

def random_bonus(mini,maxi,count):
    u = Unit({})
    for i in range(0,count):
        u.merge(Unit({random.choice(("health","armour","attack_speed","attack_damage","movement_speed","critical_chance","critical_damage","dodge_chance","strength","dexterity","constitution","intelligence","wisdom","charisma")):(random.randint(mini,maxi),0)}))
    return u

def random_bonus_combat(mini,maxi,count):
    u = Unit({})
    for i in range(0,count):
        u.merge(Unit({random.choice(("health","armour","attack_speed","attack_damage","movement_speed","critical_chance","critical_damage","dodge_chance")):(random.randint(mini,maxi),0)}))
    return u

def random_bonus_heroic(mini,maxi,count):
    u = Unit({})
    for i in range(0,count):
        u.merge(Unit({random.choice(("strength","dexterity","constitution","intelligence","wisdom","charisma")):(random.randint(mini,maxi),0)}))
    return u

def random_armour_piece(armour,bonus_count=0,level=0,mini=20,maxi=30):
    u = Unit({"armour":(random.randint(armour*0.8,armour*1.2),10)},level)
    if(bonus_count > 2):
        u.merge(random_bonus_heroic(mini,maxi,bonus_count-2))
        u.merge(random_bonus_combat(mini,maxi,2))
    else:
        u.merge(random_bonus_combat(mini,maxi,bonus_count))

    for k in u.m_attribs.keys():
        u.m_attribs[k].merge(attribute(u,0,1,0))

    return u

if __name__ == '__main__':

    source_unit_nme          = Actor_Unit({"health":(80,1),  "armour":(8,0.1),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_knight       = Actor_Unit({"health":(115,1), "armour":(20,0.1), "attack_speed":70,  "attack_damage":(40,1), "movement_speed":80 , "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_warden       = Actor_Unit({"health":(100,1), "armour":(12,0.1), "attack_speed":90,  "attack_damage":(40,1), "movement_speed":100, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_zealot       = Actor_Unit({"health":(90,1),  "armour":(8,0.1),  "attack_speed":90,  "attack_damage":(44,1), "movement_speed":110, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_savage       = Actor_Unit({"health":(100,1), "armour":(8,0.1),  "attack_speed":90,  "attack_damage":(40,1), "movement_speed":120, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_friar        = Actor_Unit({"health":(150,1), "armour":(4,0.1),  "attack_speed":70,  "attack_damage":(28,1), "movement_speed":120, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_warlock      = Actor_Unit({"health":(100,1), "armour":(4,0.1),  "attack_speed":80,  "attack_damage":(61,1), "movement_speed":80 , "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_ranger       = Actor_Unit({"health":(80,1),  "armour":(8,0.1),  "attack_speed":110, "attack_damage":(40,1), "movement_speed":110, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_scout        = Actor_Unit({"health":(100,1), "armour":(4,0.1),  "attack_speed":115, "attack_damage":(47,1), "movement_speed":130, "critical_chance":50, "critical_damage":0, "dodge_chance":0})
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

    monster_race_beast = Unit({"strength":(5,3.3), "dexterity":(3,1.5), "constitution":(5,2.9), "critical_chance":20, "critical_damage":50})
    monster_race_demon    = Unit({"strength":(3,1.7), "dexterity":(1,0.4), "constitution":(3,1.8), "intelligence":(3,2.1), "wisdom":(8,2.0), "charisma":(9,3.0)})
    monster_race_giant    = Unit({"strength":(9,2.8), "dexterity":(1,1.0), "constitution":(7,1.9), "intelligence":(6,0.4), "wisdom":(1,0.8), "charisma":(1,0.4), "attack_damage":30, "attack_speed":-30,})
    monster_race_frost_giant = Unit({"armour":15, "health":50}).merge(monster_race_giant)
    monster_race_fire_giant = Unit({"attack_damage":15, "health":80}).merge(monster_race_giant)
    monster_race_golem = Unit({"strength":(1,1.8), "constitution":(3,1.8), "wisdom":(3,1.8)})
    monster_race_lizard    = Unit({"strength":(1,0.7), "dexterity":(4,2.4), "constitution":(1,0.8), "intelligence":(3,2.1), "wisdom":(7,2.6), "dodge_chance":15})
    monster_race_lizard_dragon    = Unit({"dodge_chance":(5,0.34)}).merge(monster_race_lizard)
    monster_race_undead = Unit({"strength":(13,1.9), "dexterity":(1,1.0), "constitution":(2,1.5), "intelligence":(1,1.0)})
    monster_race_ghost = Unit({"intelligence":(4,2.5)}).merge(monster_race_undead)
    monster_race_zombie = Unit({"strength":(4,2.5),"constitution":(14,4.0)}).merge(monster_race_undead)
    monster_race_skeleton = Unit({"dexterity":(2,2.0),"armour":20}).merge(monster_race_undead)

    source_unit_knight.merge(source_class_monk_river)
    source_unit_warlock.merge(source_class_brigand)
    source_unit_nme.merge(source_class_settler)
    source_unit_scout.merge(source_class_moonbrain)

    source_unit_nme.recalc_bonus()

    #what's a suit of armour worth?
    #item_armour = random_armour_piece(300,5,0)
    #item_armour.level_up(2)
    #print item_armour.output_attribs()
    #source_unit_nme.append(item_armour)

    # add the fatty to see very long battles
    #unit_fatty = Unit({"health":10000})
    #source_unit_nme.merge(unit_fatty)
    #source_unit_scout.merge(unit_fatty)

    source_unit_nme.recalc_bonus()
    source_unit_scout.recalc_bonus()
    source_unit_knight.recalc_bonus()
    source_unit_warlock.recalc_bonus()


    print

    player1 = source_unit_knight.copy()
    player2 = source_unit_warlock.copy()

    for i in range(0,1):
        player1.level_up(1)
        player2.level_up(1)
        print player1
        print player2,"\n"

    print "\t\t\t\tHP 1:", player1.m_current_health,"\t\t",
    print "\t\t\t\tHP 2:", player2.m_current_health

    while(True):
        
        second = player2.attack(player1)
        first  = player1.attack(player2)
        print "2->1:",second[0], "\t\tHP 1:", player1.m_current_health,"\t\t",
        print "1->2:",first[0], "\t\tHP 2:", player2.m_current_health,
        print "\t\t"+second[1],"\t\t",first[1]

        if(player1.m_current_health < 1 or player2.m_current_health < 1):
            break
