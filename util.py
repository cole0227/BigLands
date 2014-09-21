import random
import sys
import copy
import os

import pygame
import pygame.time
import pygame.image
import numpy
from scipy.misc import imsave

import globals
from sprite_sheet import *

execfile("font_fx.py")

#
# submits cross-thread-message
#
def message(mess=0):

    if(mess == 0):
        fo = open("Saved Games/message.tmp","r")
        new = fo.read()
        fo.close()
        return new
    else:
        fo = open("Saved Games/message.tmp","w+")
        fo.write(mess)
        fo.close()


#
# makes sure that a given dir exists
#
def ensure_dir(f):
    path = os.path.dirname(f)
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

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
# Return values within a certain range
#
def elevation_selection( amatrix, low, high, lowfill, highfill ):

    size = int( amatrix.size ** ( 0.5 ) )
    selection = numpy.zeros(( size, size )) + lowfill

    for x in range( 0, size ):
    
        for y in range( 0, size ):
        
            if( amatrix[x][y] >=  low and amatrix[x][y] <= high ):
            
                selection[x][y] = amatrix[x][y]
                
            elif( amatrix[x][y] >= high ):
            
                selection[x][y] = highfill
            
    return selection

#
# changes a value in a matrix
#
def matrix_fromto(amatrix,start,end):

    size = int( amatrix.size ** ( 0.5 ) )
    for x in range( 0, size ):
    
        for y in range( 0, size ):
    
            if(amatrix[x][y]==start):
                
                amatrix[x][y]=end
            
    
    return amatrix

#
# redistributes according to the given value arrays
#
def matrix_redist(amatrix, vals):

    portions = len(vals)-1

    processed_matrix = matrix_scale(amatrix,vals[0],vals[portions])
    size = int( processed_matrix.size ** ( 0.5 ) )
    flat_matrix = processed_matrix.reshape( -1 )
    final_matrix = numpy.zeros((size,size))
    perc = [0]*(portions+1)
    for i in range(0,portions+1):
        perc[i]=100.0*i/portions
    perc = numpy.percentile(flat_matrix,perc)

    for i in range(1,portions+1):
        
        perc[i]
        if(vals[i]-vals[i-1] != 0 and perc[i-1]-perc[i] != 0):

            final_matrix += matrix_scale(
                elevation_selection(processed_matrix, 
                                    perc[i-1], perc[i], 
                                    perc[i-1], perc[i]),
                0,vals[i]-vals[i-1])

    return final_matrix

#
# Basic value clamping
#
def clamp(l,m,g):
    
    return max(l,min(g,m))

#
# Basic Distance Calculation
#
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

    #Reset all our variables for the next iteration, and return some values
    out = [globals.icon_list[ico],ox+6*oy,u]
    u,t,ox,oy,name,ico=-1,-1,-1,-1,None,None
    return out

def save_icon_double(u=-1,t=-1,ox=-1,oy=-1,name=None,ico=None,ico2=None,ico2_back=-1):

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

    if(ico2 == None):
        ico2 = random.randint(0,len(globals.icon_list)-1)

    if(ico2_back == -1):
        ico2_back = random.randint(0,15)


    #loading the images
    icon_under =    globals.icons_iu.image_by_index(512,u)
    under_texture = globals.icons_ut.image_by_index(512,t)

    icon = pygame.image.load(random_icon(ico))
    icon.convert_alpha()

    icon2 = pygame.image.load(random_icon(ico2))
    icon2.convert_alpha()

    print (512*(ico2_back/4),512*(ico2_back%4),512,512)
    icon2backing = globals.icons_corner_chunk.subsurface(512*(ico2_back/4),512*(ico2_back%4),512,512)
    icon2backing.convert_alpha()

    #begin building the basic image
    icon.blit(icon_under,(0,0),None,pygame.BLEND_ADD)
    icon2.blit(globals.icons_iu.image_by_index(512,random.randint(0,17)),(0,0),None,pygame.BLEND_ADD)

    under_texture.blit(icon,(0,0))
    under_texture.blit(globals.icons_overtest,(512*-ox,512*-oy))

    #manipulating the top-left icon
    icon2 = pygame.transform.scale(icon2,(400,400))
    icon2backing.blit(icon2,(0,0))
    icon2backing = pygame.transform.scale(icon2backing,(160,160))
    under_texture.blit(icon2backing,(0,0))

    if(name == None):
        pygame.image.save(under_texture,str(u)+" "+str(t)+" "+str(ox)+" "+str(oy)+" "+str(ico)+".png")
    else:
        pygame.image.save(under_texture,name)


    #Reset all our variables for the next iteration, and return some values
    out = [globals.icon_list[ico],ox+6*oy,u,globals.icon_list[ico2]]
    u,t,ox,oy,name,ico,ico2,ico2_back=-1,-1,-1,-1,None,None,None,-1
    return out

if __name__ == '__main__':

    #print pygame.font.get_fonts()
    size = 1290
    height = numpy.zeros((size,size))

    for x in range( 0, size ):
        for y in range( 0, size ):
            height[x][y] = (x-size/2)**2+(y-size/2)**2

    imsave("1.png",height)
    height = matrix_redist(height,(0,34,80,90,100))
    imsave("2.png",height)