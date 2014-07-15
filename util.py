import random
import sys
import copy
import pygame
import pygame.time
import pygame.image
import numpy

import globals
from sprite_sheet import *

execfile("font_fx.py")

#
# Finds the Largest and smallest element
#
def stats_range(amatrix):

    mymatrix = amatrix.reshape( -1 )
    sort = mymatrix.argsort()
    final = [mymatrix[sort[0]], mymatrix[sort[ amatrix.size - 1 ]]]
    return final

#
# Forces the numbers in a matrix to within set bounds
#
def matrix_scale(amatrix,minimum,maximum):
        
    size = int( amatrix.size ** ( 0.5 ) )
    rs = stats_range( amatrix )
    factor = ( maximum - minimum ) / ( rs[1] - rs[0] )
    amatrix = ( amatrix - rs[0] ) * factor + minimum
    return amatrix

#
# Gives the value for the 9 intermediary 10th-percentile
# elevations, and the highest and lowest points
#
def stats_percentile( amatrix ):
    
    mymatrix = amatrix.reshape( -1 )
    sort = mymatrix.argsort()

    #
    # Returns the element for the matching percent
    #
    def find_percentile( percent ):
        
        return sort[ min( max( int( ( amatrix.size - 1 ) * percent / 100), 0 ), amatrix.size - 1 ) ]

    final = numpy.zeros(( 11 )) 
    for x in range( 0, 11 ):

        final[x] = mymatrix[ find_percentile( x * 10 ) ]

    return final

#
# Basic value clamping
#
def clamp(l,m,g):
    
    return max(l,min(g,m))

def distance(pos1,pos2):

    return ( (pos1[0]-pos2[0]) ** 2 + (pos1[1]-pos2[1]) ** 2 ) ** 0.5

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