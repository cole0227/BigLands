import random
import copy

import pygame
import pygame.time
from pygame.locals import *
import pygame.mouse

import globals
from timer import *
from util import *

class Attribute(object):
    
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
                self.m_attribs[attrib]=Attribute(self,self.m_attribs[attrib])
            elif(type(self.m_attribs[attrib]) is Attribute):
                self.m_attribs[attrib].m_owner = self
            else:
                self.m_attribs[attrib]=Attribute(self,self.m_attribs[attrib][0],self.m_attribs[attrib][1])

    def set(self, attrib, value):

        self.m_attribs[attrib]=value

    def get(self, attrib):

        value = self.m_attribs.get(attrib)
        
        if(value == None):
            return 0
            
        return value.get()

    def merge_attrib(self,attrib,value):

        curr = self.m_attribs.get(attrib)
        
        if(curr == None):
            
            self.m_attribs[attrib]=value

        else:

            self.m_attribs[attrib].merge(value)

    def copy(self):

        otr = copy.deepcopy(self)

        for attrib in otr.m_attribs.keys():

            otr.m_attribs[attrib].m_owner = otr

        return otr

    def output_attribs(self):

        string = "Level: "+str(self.m_level)
        for key in self.m_attribs.keys():
            if(str(self.m_attribs[key]) != "0"):
                string +="\n"+str(key)+": "+str(self.m_attribs[key])+" (+"+str(int(self.m_attribs[key].m_growth*10)/10.0)+")"

        return string

    def __str__(self):

        string = "Level:"+str(self.m_level)
        string += "\t\tHP: "+str(self.m_attribs["health"])
        string += " "+str(self.m_attribs["armour"])+"A "+str(self.m_attribs["dodge_chance"])+"D "+str(self.m_attribs["health_regeneration"])+"R"
        string += "\t\tSpeed: "+str(self.m_attribs["movement_speed"])+"%"
        string += "\t\tAttack: "+str(self.m_attribs["attack_damage"])+"/"+str(self.m_attribs["attack_speed"])+"%"
        string += "\t\tCrits: "+str(100+self.m_attribs["critical_damage"].get())+"/"+str(self.m_attribs["critical_chance"])+"%"
        string += "\t\tHeroic Stats{"
        if("toughness" in self.m_attribs):
            string += "T:"+str(self.m_attribs["toughness"])+" "
        if("agility" in self.m_attribs):
            string += "A:"+str(self.m_attribs["agility"])+" "
        if("constitution" in self.m_attribs):
            string += "C:"+str(self.m_attribs["constitution"])+" "
        if("finesse" in self.m_attribs):
            string += "F:"+str(self.m_attribs["finesse"])+" "
        if("might" in self.m_attribs):
            string += "M:"+str(self.m_attribs["might"])+" "
        if("precision" in self.m_attribs):
            string += "P:"+str(self.m_attribs["precision"])+" "
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

    def __init__(self, attribs, level=0, name="Monster"):

        Unit.__init__(self, attribs, level)

        self.m_bonus = []
        self.m_current_health = self.get("health")
        self.m_name=name

    def append(self, unit):

        self.m_bonus.append(unit)
        self.recalc_bonus()

    def reset(self):

        self.m_bonus = []
        self.recalc_bonus()

    def recalc_bonus(self):

        oldHP = 0
        if(int(self.get("health")) != 0):
            oldHP = self.m_current_health/float(self.get("health"))

        for attrib in self.m_attribs.keys():

            self.m_attribs[attrib].reset()

            for bonus in self.m_bonus:

                self.m_attribs[attrib].add(bonus.get(attrib))

        if "toughness" in self.m_attribs:

            self.m_attribs["health"].add(self.get("toughness")*4)
            self.m_attribs["armour"].add(self.get("toughness")*0.1)

        if "agility" in self.m_attribs:

            self.m_attribs["attack_speed"].add(self.get("agility")*0.8)
            self.m_attribs["movement_speed"].add(self.get("agility"))

        if "constitution" in self.m_attribs:

            self.m_attribs["health"].add(self.get("constitution")*9)
            self.m_attribs["health_regeneration"].add(self.get("constitution")*0.05)

        if "finesse" in self.m_attribs:

            self.m_attribs["attack_speed"].add(self.get("finesse")*0.4)
            self.m_attribs["dodge_chance"].add(self.get("finesse")*0.3)

        if "might" in self.m_attribs:

            self.m_attribs["attack_damage"].add(0.5*self.get("might"))
            self.m_attribs["health_regeneration"].add(self.get("might")*0.02)

        if "precision" in self.m_attribs:

            self.m_attribs["critical_chance"].add(self.get("precision")*0.5)
            self.m_attribs["critical_damage"].add(self.get("precision")*0.4)

        if(oldHP != 0):
            self.m_current_health = float(self.get("health"))*float(oldHP)
        else:
            self.m_current_health = float(self.get("health"))

    def merge(self,unit):

        oldHP = 0
        if(int(self.get("health")) != 0):
            oldHP = self.m_current_health/float(self.get("health"))

        for attrib in unit.m_attribs.keys():
            if attrib in self.m_attribs:
                self.m_attribs[attrib].merge(unit.m_attribs[attrib])
            else:
                self.m_attribs[attrib]=unit.m_attribs[attrib]
                self.m_attribs[attrib].m_owner=self
            #print "Merge Attrib:"+attrib

        if(oldHP != 0):
            self.m_current_health = float(self.get("health"))*float(oldHP)
        else:
            self.m_current_health = float(self.get("health"))

    def level_up(self,level=1):

        oldHP = 0
        if(int(self.get("health")) != 0):
            oldHP = self.m_current_health/float(self.get("health"))

        self.m_level += level
        self.recalc_bonus()

        if(oldHP != 0):
            self.m_current_health = float(self.get("health"))*float(oldHP)
        else:
            self.m_current_health = float(self.get("health"))

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

        #this list contains all the heroic stats 3 times
        stat = random.choice(("health","health_regeneration","armour","attack_speed","attack_damage","movement_speed","critical_chance","critical_damage","dodge_chance","toughness","agility","constitution","finesse","might","precision","toughness","agility","constitution","finesse","might","precision","toughness","agility","constitution","finesse","might","precision"))

        if(stat == "health"):
            u.merge(Unit({stat:(random.randint(mini*3,maxi*3),0)}))
        elif(stat == "health_regeneration"):
            u.merge(Unit({stat:(random.randint(mini/20.0,maxi/20.0),0)}))
        elif("chance" in stat):
            u.merge(Unit({stat:(random.randint(mini/5.0,maxi/5.0),0)}))
        else:
            u.merge(Unit({stat:(random.randint(mini,maxi),0)}))
    return u

def random_bonus_combat(mini,maxi,count):
    u = Unit({})
    for i in range(0,count):

        #this list contains no heroic stats
        stat = random.choice(("health","health_regeneration","armour","attack_speed","attack_damage","movement_speed","critical_chance","critical_damage","dodge_chance"))

        if(stat == "health"):
            u.merge(Unit({stat:(random.randint(mini*3,maxi*3),0)}))
        elif(stat == "health_regeneration"):
            u.merge(Unit({stat:(random.randint(mini/20.0,maxi/20.0),0)}))
        elif("chance" in stat):
            u.merge(Unit({stat:(random.randint(mini/5.0,maxi/5.0),0)}))
        else:
            u.merge(Unit({stat:(random.randint(mini,maxi),0)}))
    return u

def random_bonus_heroic(mini,maxi,count):
    u = Unit({})
    for i in range(0,count):
        u.merge(Unit({random.choice(("toughness","agility","constitution","finesse","might","precision")):(random.randint(mini,maxi),0)}))
    return u

def random_armour_piece(armour,bonus_count=0,level=0,mini=20,maxi=30):
    u = Unit({"armour":(random.randint(armour*0.8,armour*1.2),10)},level)

    u.merge(random_bonus(mini,maxi,bonus_count))

    for k in u.m_attribs.keys():
        u.m_attribs[k].merge(Attribute(u,0,1,0))

    return u

if __name__ == '__main__':

    blank                    = Actor_Unit({"health":0,  "health_regeneration":0, "armour":0,  "attack_speed":0, "attack_damage":0, "movement_speed":0, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_nme          = Actor_Unit({"health":(80,1),  "health_regeneration":(1,0.05), "armour":(8,0.1),  "attack_speed":100, "attack_damage":(40,1), "movement_speed":100, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_knight       = Actor_Unit({"health":(115,1), "health_regeneration":(1,0.05), "armour":(20,0.1), "attack_speed":70,  "attack_damage":(40,1), "movement_speed":80 , "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_warden       = Actor_Unit({"health":(100,1), "health_regeneration":(1,0.05), "armour":(12,0.1), "attack_speed":90,  "attack_damage":(40,1), "movement_speed":100, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_zealot       = Actor_Unit({"health":(90,1),  "health_regeneration":(1,0.05), "armour":(8,0.1),  "attack_speed":90,  "attack_damage":(44,1), "movement_speed":110, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_savage       = Actor_Unit({"health":(100,1), "health_regeneration":(1,0.05), "armour":(8,0.1),  "attack_speed":90,  "attack_damage":(40,1), "movement_speed":120, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_friar        = Actor_Unit({"health":(150,1), "health_regeneration":(1,0.05), "armour":(4,0.1),  "attack_speed":70,  "attack_damage":(28,1), "movement_speed":120, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_warlock      = Actor_Unit({"health":(100,1), "health_regeneration":(1,0.05), "armour":(4,0.1),  "attack_speed":80,  "attack_damage":(61,1), "movement_speed":80 , "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_ranger       = Actor_Unit({"health":(80,1),  "health_regeneration":(1,0.05), "armour":(8,0.1),  "attack_speed":110, "attack_damage":(40,1), "movement_speed":110, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    source_unit_scout        = Actor_Unit({"health":(100,1), "health_regeneration":(1,0.05), "armour":(4,0.1),  "attack_speed":115, "attack_damage":(47,1), "movement_speed":130, "critical_chance":0, "critical_damage":0, "dodge_chance":0})
    #source_unit_scout.append(Unit({"armour":8}))

    source_class_shepherd   = Unit({"toughness":(1,1.0), "agility":(1,1.0), "constitution":(1,1.0), "finesse":(1,1.0), "might":(3,1.8), "precision":(3,1.8)})
    source_class_brigand    = Unit({"toughness":(3,2.2), "agility":(1,1.0), "constitution":(3,2.2), "finesse":(1,1.0), "might":(1,1.0), "precision":(1,1.0)})
    source_class_moonbrain  = Unit({"toughness":(1,1.2), "agility":(1,1.4), "constitution":(1,1.2), "finesse":(3,1.7), "might":(3,1.7), "precision":(1,1.2)})
    source_class_veteran    = Unit({"toughness":(1,1.0), "agility":(1,1.0), "constitution":(3,1.8), "finesse":(1,1.0), "might":(1,1.0), "precision":(3,1.8)})
    source_class_monk_river = Unit({"toughness":(1,1.0), "agility":(3,1.7), "constitution":(1,1.2), "finesse":(3,1.7), "might":(1,1.0), "precision":(1,1.0)})
    source_class_monk_wind  = Unit({"toughness":(1,0.9), "agility":(3,1.8), "constitution":(1,1.3), "finesse":(1,0.9), "might":(3,1.8), "precision":(1,0.9)})
    source_class_monk_leaf  = Unit({"toughness":(1,1.0), "agility":(3,1.8), "constitution":(3,2.2), "finesse":(1,1.0), "might":(1,1.0), "precision":(1,1.0)})
    source_class_settler    = Unit({"toughness":(1,1.0), "agility":(1,1.0), "constitution":(3,1.8), "finesse":(1,1.0), "might":(3,1.8), "precision":(1,1.0)})
    source_class_reaver     = Unit({"toughness":(3,1.8), "agility":(3,1.8), "constitution":(1,1.0), "finesse":(1,1.0), "might":(1,1.0), "precision":(1,1.0)})
    source_class_agent      = Unit({"toughness":(1,0.9), "agility":(1,0.9), "constitution":(1,0.9), "finesse":(5,2.9), "might":(1,0.9), "precision":(1,0.9)})
    source_class_ambassador = Unit({"toughness":(1,0.9), "agility":(1,0.9), "constitution":(1,0.9), "finesse":(1,0.9), "might":(1,0.9), "precision":(5,2.9)})

    monster_race_beast = Unit({"toughness":(5,3.3), "agility":(3,1.5), "constitution":(5,2.9), "critical_chance":20, "critical_damage":50})
    monster_race_cultist = Unit({"toughness":(1,1.1), "agility":(0,0.4), "constitution":(1,1.2), "finesse":(3,1.4), "might":(2,1.4), "precision":(9,3.0)})
    monster_race_demon = Unit({"toughness":(3,1.7), "agility":(0,0.4), "constitution":(3,1.8), "finesse":(3,2.1), "might":(8,2.0), "precision":(9,3.0)})
    monster_race_giant = Unit({"toughness":(9,2.8), "agility":(1,1.0), "constitution":(7,1.9), "finesse":(6,0.4), "might":(1,0.8), "precision":(1,0.4), "attack_damage":30, "attack_speed":-30,})
    monster_race_frost_giant = Unit({"armour":15, "health":50}).merge(monster_race_giant)
    monster_race_fire_giant = Unit({"attack_damage":15, "health":80}).merge(monster_race_giant)
    monster_race_golem = Unit({"toughness":(1,1.8), "constitution":(3,1.8), "might":(3,1.8)})
    monster_race_lizard = Unit({"toughness":(1,0.7), "agility":(4,2.4), "constitution":(1,0.8), "finesse":(3,2.1), "might":(7,2.6), "dodge_chance":15})
    monster_race_lizard_dragon = Unit({"dodge_chance":(5,0.34)}).merge(monster_race_lizard)
    monster_race_undead = Unit({"toughness":(13,1.9), "agility":(1,1.0), "constitution":(2,1.5), "finesse":(1,1.0)})
    monster_race_ghost = Unit({"finesse":(4,2.5)}).merge(monster_race_undead)
    monster_race_zombie = Unit({"toughness":(4,2.5),"constitution":(14,4.0)}).merge(monster_race_undead)
    monster_race_skeleton = Unit({"agility":(2,2.0),"armour":20}).merge(monster_race_undead)    

    source_unit_knight.merge(source_class_monk_river)
    source_unit_warlock.merge(source_class_brigand)
    source_unit_nme.merge(source_class_settler)
    source_unit_scout.merge(source_class_moonbrain)

    #print source_unit_ranger
    #source_unit_ranger.merge(source_class_brigand)
    #source_unit_ranger.merge(monster_race_demon)
    #source_unit_ranger.merge(monster_race_lizard)
    #source_unit_ranger.merge(monster_race_undead)
    #source_unit_ranger.recalc_bonus()
    #print source_unit_ranger
    #source_unit_ranger.level_up()
    #source_unit_ranger.recalc_bonus()
    #print source_unit_ranger
    #source_unit_ranger.level_up(98)
    #source_unit_ranger.recalc_bonus()
    #print source_unit_ranger
    #print source_unit_ranger.output_attribs()
    #print


    #what's a suit of armour worth?
    item_armour = random_armour_piece(100,1,0)
    print item_armour.output_attribs()
    source_unit_knight.append(item_armour)

    # add the fatty to see very long battles
    #unit_fatty = Unit({"health":10000})
    #source_unit_nme.merge(unit_fatty)
    #source_unit_scout.merge(unit_fatty)

    source_unit_nme.recalc_bonus()
    source_unit_scout.recalc_bonus()
    source_unit_knight.recalc_bonus()
    source_unit_warlock.recalc_bonus()
    source_unit_ranger.recalc_bonus()


    print

    player1 = source_unit_knight.copy()
    player2 = source_unit_warlock.copy()

    for i in range(0,1):
        player1.level_up(250)
        player2.level_up(250)
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
