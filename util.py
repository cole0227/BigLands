import random
import sys
import copy
import pygame
import pygame.time
import pygame.image

import globals
from sprite_sheet import *

def clamp(l,m,g):
    
    return max(l,min(g,m))


def random_icon(num=None):
    if(num == None):
        return "Assets/Game-Icons/"+globals.icon_list[random.randint(0,len(globals.icon_list)-1)]
    else:
        return "Assets/Game-Icons/"+globals.icon_list[num]

def save_icon(u=-1,t=-1,ox=-1,oy=-1,name=None,ico=None):

    if(u == -1):
        u = random.randint(0,17)

    if(t == -1):
        t = random.randint(0,17)

    if(ox == -1):
        ox = random.randint(0,5)

    if(oy == -1):
        oy = random.randint(0,2)

    if(ico == None):
        ico = random.randint(0,len(globals.icon_list)-1)

    #loading the images
    icon_under =    globals.icons_iu.image_by_index(512,u)
    under_texture = globals.icons_ut.image_by_index(512,t)
    icon = pygame.image.load(random_icon(ico))
    icon.convert_alpha()

    icon.blit(icon_under,(0,0),None,pygame.BLEND_ADD)

    under_texture.blit(icon,(0,0))
    under_texture.blit(globals.icons_overtest,(512*-ox,512*-oy))
    if(name == None):
        pygame.image.save(under_texture,str(u)+" "+str(t)+" "+str(ox)+" "+str(oy)+" "+str(ico)+".png")
    else:
        pygame.image.save(under_texture,name)

    #Reset all our variables for the next iteration
    u,t,ox,oy,name,ico=-1,-1,-1,-1,None,None

#print pygame.font.get_fonts()