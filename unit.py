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
    
    def __init__(self, owner, base=100, bonus=0):

        self.owner = owner;
        self.m_base = int(base);
        self.m_bonus = int(bonus);

    def get(self):

        return self.m_base+self.m_bonus

    def add(self, bonus):
        
        self.m_bonus += int(bonus)

    def reset(self):

        self.m_bonus = 0

    def __str__(self):

        return str(self.get());


class Unit(object):

    def __init__(self, health = 0, armour = 0, movement_speed = 0, attack_damage = 0, attack_speed = 0):

        self.m_health = attribute(self,health)
        self.m_armour = attribute(self,armour)
        self.m_movement_speed = attribute(self,movement_speed)
        self.m_attack_damage = attribute(self,attack_damage)
        self.m_attack_speed = attribute(self,attack_speed)

    def change(self, health = None, armour = None, movement_speed = None, attack_damage = None, attack_speed = None):

        if(health != None):
            self.m_health = attribute(self,health)

        if(armour != None):
            self.m_armour = attribute(self,armour)

        if(movement_speed != None):
            self.m_movement_speed = attribute(self,movement_speed)

        if(attack_damage != None):
            self.m_attack_damage = attribute(self,attack_damage)

        if(attack_speed != None):
            self.m_attack_speed = attribute(self,attack_speed)

    def get(self, attribute):

        total = 0

        if(attribute == "health"):

            return self.m_health.get()

        elif(attribute == "armour"):

            return self.m_armour.get()

        elif(attribute == "movement_speed"):

            return self.m_movement_speed.get()

        elif(attribute == "attack_damage"):

            return self.m_attack_damage.get()

        elif(attribute == "attack_speed"):

            return self.m_attack_speed.get()
 
    def __str__(self):

        string = "HP: "+str(self.m_health)
        string += "/"+str(self.m_armour)
        string += "\t\tSpeed: "+str(self.m_movement_speed)+"%"
        string += "\t\tAttack: "+str(self.m_attack_damage)+"/"+str(self.m_attack_speed)+"%"
        return string

class Actor_Unit(Unit):

    def __init__(self, health = 100, armour = 8, movement_speed = 100, attack_damage = 39, attack_speed = 100):

        Unit.__init__(self, health, armour, movement_speed, attack_damage, attack_speed)

        self.m_bonus = []
        self.m_current_health = self.get("health")

    def append(self, unit):

        self.m_bonus.append(unit)
        self.recalc_bonus()

    def reset(self):

        self.m_bonus = []
        self.recalc_bonus()

    def recalc_bonus(self):

        self.m_health.reset()
        self.m_armour.reset()
        self.m_movement_speed.reset()
        self.m_attack_damage.reset()
        self.m_attack_speed.reset()

        for bonus in self.m_bonus:
            self.m_health.add(bonus.get("health"))
            self.m_armour.add(bonus.get("armour"))
            self.m_movement_speed.add(bonus.get("movement_speed"))
            self.m_attack_damage.add(bonus.get("attack_damage"))
            self.m_attack_speed.add(bonus.get("attack_speed"))

    def calc_damage(self, source_unit, mult=1.0):

        base_damage = source_unit.get("attack_damage")
        damage = random.uniform(base_damage*19.0,base_damage*21.0)/20
        damage *= mult
        damage = int(max( damage - self.get("armour"), 0))
        self.m_current_health = max(self.m_current_health-damage,0)
        return damage


player = Actor_Unit()
player2 = Actor_Unit(armour = 11)
print player2

generic_nme  = Actor_Unit( 80, 8,100, 40,100)
knight       = Actor_Unit(115,14, 70, 40, 80)
warden       = Actor_Unit(100,10, 90, 40,100)
zealot       = Actor_Unit( 90, 8, 90, 44,110)
savage       = Actor_Unit(100, 4, 90, 49,120)
friar        = Actor_Unit(150, 6, 70, 28,120)
warlock      = Actor_Unit(100, 6, 80, 61, 80)
ranger       = Actor_Unit(80 , 8,110, 40,110)
source_unit  = Actor_Unit(100, 6,115, 47, 80)

for i in range(0,5):

    player1 = knight
    player2 = zealot
    
    print "1->2:",player2.calc_damage(player1), "\t\tHP:", player2.m_current_health,"\t\t",
    print "2->1:",player1.calc_damage(player2), "\t\tHP:", player1.m_current_health