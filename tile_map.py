import sys
import cStringIO
import gc
import time
import math
import sys
import random
from collections import defaultdict

import numpy
import scipy
from scipy.misc import imsave
import scipy.ndimage
import pygame
from pygame.locals import *
import pygame.time
import pygame.font
import gaussian_blur
from util import *
from sprite_sheet import *
import globals
import map_generation

class Tile(object):

    def __init__(self, index, surface):

        self.i = index
        self.m_surface = surface

    def get(self):

        return self.m_surface

class Tile_Map(object):

    def __init__(self, height_map, water_map, wood_map, tileset_image, masks_image, width, height, tile_size, tree_threshhold=0.75, road_threshhold=0.08):

        self.m_width = width
        self.m_height = height
        self.m_tile_size = tile_size
        self.m_tree_threshhold = tree_threshhold
        self.m_road_threshhold = road_threshhold
        self.m_sprite_sheet = Sprite_Sheet(tileset_image)
        self.m_masks = Sprite_Sheet(masks_image)
        self.m_height_map = map_generation.matrix_scale(height_map,0,100)
        self.m_water_map = numpy.array(water_map)
        self.m_collision_map = numpy.zeros((width,height))+1
        
        print self.m_height_map.shape,"/",self.m_water_map.shape
        self.m_height_map = scipy.ndimage.zoom(self.m_height_map, (max(width+1.4,height+1.4)**2/self.m_height_map.size)**0.5, order=4)
        print  (max(width+1.0,height+1.0)**2/self.m_height_map.size)**0.5
        self.m_water_map = scipy.ndimage.zoom(self.m_water_map, (max(width+1.4,height+1.4)**2/self.m_water_map.size)**0.5, order=4)
        self.m_water_map = gaussian_blur.gaussian_blur(self.m_water_map,1)
        print self.m_height_map.shape,"/",self.m_water_map.shape

        self.march()

        #woods time
        maxX = 0
        maxY = 0

        for xy, tile in wood_map.iteritems():

            #we need these for calulating size
            maxX = max(maxX,xy[0])
            maxY = max(maxY,xy[1])
            

        self.m_wood_map = numpy.zeros((maxX+1,maxY+1))

        for xy, tile in wood_map.iteritems():

            if(tile == "#"):

                self.m_wood_map[xy[0]][xy[1]] = 1

            else:

                self.m_wood_map[xy[0]][xy[1]] = 0

        self.m_wood_map = scipy.ndimage.zoom(self.m_wood_map, (max(width+1.0,height+1.0)**2/self.m_wood_map.size)**0.5, order=4)
        self.m_wood_map_blurry = matrix_scale(gaussian_blur.gaussian_blur( self.m_wood_map, 1 ),0,1)
        
        #let's erode a bit
        newmap = numpy.zeros((self.m_width+1,self.m_height+1))
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                if(self.m_wood_map[x][y] > self.m_tree_threshhold):

                            for x1, y1 in ((0, -1), (-1, 0), (1, 0), (0, 1)):

                                if(self.m_wood_map[x+x1][y+y1] < self.m_tree_threshhold):

                                    newmap[x][y]=self.m_tree_threshhold/2
                                    break
        
        self.m_wood_map -= newmap

        #trees do not grow on gravel, or in the water
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                x1 = min(x+1,self.m_width)
                y1 = min(y+1,self.m_height)
                if(self.m_typemap[x][y] == 8 or 
                   self.m_typemap[x][y] == 9 or 
                   self.m_typemap[x][y] == 1 or
                   self.m_typemap[x1][y] == 8 or
                   self.m_typemap[x1][y] == 9 or
                   self.m_typemap[x1][y] == 1 or
                   self.m_typemap[x][y1] == 8 or
                   self.m_typemap[x][y1] == 9 or
                   self.m_typemap[x][y1] == 1 or
                   self.m_typemap[x1][y1] == 8 or
                   self.m_typemap[x1][y1] == 9 or
                   self.m_typemap[x1][y1] == 1):

                    self.m_wood_map[x][y] = 0
        
        #let's set up the collision map:
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                if(self.m_height_map[y][x]>5 and self.m_typemap[x][y] != 8 and self.m_height_map[y][x]<=22):
                    if(self.m_height_map[y][x]<=88):
                        self.m_collision_map[x][y] = 0
                    else:
                        self.m_collision_map[x][y] = 0.7

    def march_assist(self,x,y,type):

        index=0

        if(self.m_typemap[x  ][y  ]==type):
            index+=8
        if(self.m_typemap[x+1][y  ]==type):
            index+=4
        if(self.m_typemap[x+1][y+1]==type):
            index+=2
        if(self.m_typemap[x  ][y+1]==type):
            index+=1

        return index

    def march(self):

        self.m_typemap = numpy.zeros((self.m_width+1,self.m_height+1))

        print "Typing..."
        for x in range(0,self.m_width+1):
            for y in range(0,self.m_height+1):

                if(self.m_water_map[x][y] > 1.07 or self.m_height_map[y][x] > 60):

                    if(self.m_height_map[y][x]>88):
                        self.m_typemap[x][y]=3 # light rock

                    elif(self.m_height_map[y][x]>75):
                        self.m_typemap[x][y]=2 # dark rock

                    elif(self.m_height_map[y][x]>65):
                        self.m_typemap[x][y]=5 # jungle

                    elif(self.m_height_map[y][x]>32):
                        self.m_typemap[x][y]=4 # grass

                    elif(self.m_height_map[y][x]>22):
                        self.m_typemap[x][y]=6 # dirt

                    elif(self.m_height_map[y][x]>15):
                        self.m_typemap[x][y]=1 # gravel

                    elif(self.m_height_map[y][x]>5):
                        self.m_typemap[x][y]=7 # beach

                    else:
                        self.m_typemap[x][y]=8 # shallow water

                elif(self.m_water_map[x][y] > 0.8):
                    self.m_typemap[x][y]=8 # shallow water

                else:
                    self.m_typemap[x][y]=9 # deep water

        #bordering the coastlines
        for x in range(1,self.m_width):
            for y in range(1,self.m_height):

                #deep water
                if(self.m_typemap[x][y] == 9):
                    self.m_typemap[x][y] = 8

                #shallow water
                if(self.m_typemap[x][y] == 8):

                    #are we by the sea-shore?
                    near_water = 0
                    for x1 in range(-1,2):
                        for y1 in range(-1,2):
                            if(self.m_typemap[x+x1][y+y1] == 9 or self.m_typemap[x+x1][y+y1] == 8):
                                near_water += 1

                    if(near_water>=9):
                        #make it deep water
                        self.m_typemap[x][y] = 9
                
                #grabbing coast that isn't gravel or beach
                elif(self.m_typemap[x][y] != 7 and self.m_typemap[x][y] != 1):

                    #are we by the sea-shore?
                    near_water = 0
                    for x1 in range(-1,2):
                        for y1 in range(-1,2):
                            if(self.m_typemap[x+x1][y+y1] == 9 or self.m_typemap[x+x1][y+y1] == 8):
                                near_water +=1

                    #make it gravel
                    if(near_water >= 2):
                        self.m_typemap[x][y]=1

        #add the extra layers of shallow water
        for i in range(0,2):
            tempmap = numpy.zeros((self.m_width+1,self.m_height+1))
            for x in range(1,self.m_width):
                for y in range(1,self.m_height):

                    #deep water
                    if(self.m_typemap[x][y] == 9):

                        #are we by the shallows
                        near_shallows = 0
                        for x1 in range(-1,2):
                            for y1 in range(-1,2):
                                if(self.m_typemap[x+x1][y+y1] == 8):
                                    near_shallows += 1
                                    break

                        if(near_shallows>0):
                            #make it more shallow, by applying it later
                            tempmap[x][y] = -1
            #apply the temp map
            self.m_typemap += tempmap

    def make_surface(self,x1,y1,x2,y2):  

        self.m_map = defaultdict(lambda  : defaultdict(list))
        print len(self.m_map),',',len(self.m_map[0])

        for x in range(x1,x2):
            for y in range(y1,y2):
                surf = pygame.Surface((self.m_tile_size,self.m_tile_size))
                surf.fill((255,0,255))
                self.m_map[x][y].append(Tile(-1,surf))

        self.blit(x1,y1,x2,y2)
        self.trees(x1,y1,x2,y2)

    def blit(self,x1,y1,x2,y2):

        print "Caching",
        surf = []
        for i in range(0,10):
            surf.append(self.m_sprite_sheet.image_by_index(750,i).convert_alpha())
            print ".",

        masks = []
        for i in range(0,16):
            masks.append(pygame.transform.scale(self.m_masks.image_by_index(250,i).convert_alpha(),(self.m_tile_size,self.m_tile_size)))
            globals.window_surface.blit(masks[i],(i*32,0))
            print ".",
        print "."

        print "Blitting..."
        for x in range(x1,x2):
            for y in range(y1,y2):
                for tid in range(9, -1, -1):

                    #this tells us which index of the mask we need
                    ma = self.march_assist(x,y,tid)

                    if(ma != 0):

                        #setting up the temporary surface for blitting
                        mask_surface = pygame.Surface((self.m_tile_size,self.m_tile_size)).convert_alpha()
                        posn = [(x*self.m_tile_size)%750,(y*self.m_tile_size)%750,self.m_tile_size,self.m_tile_size]
                        mask_surface.blit(masks[ma],(0,0), None, pygame.BLEND_ADD)

                        if( self.m_typemap[x][y] != -1):

                            posn2=posn[:]
                            mask_surface.blit(surf[tid],(0, 0),area = posn2, special_flags = pygame.BLEND_ADD)

                            #covers the edge cases where it needs to tile
                            if(posn[0] + posn[2] >= 750):
                                posn2[0]=0
                                mask_surface.blit(surf[tid],(750-posn[0], 0),area = posn2, special_flags = pygame.BLEND_ADD)

                                if(posn[1] + posn[3] >= 750):
                                    posn2[1]=0
                                    mask_surface.blit(surf[tid],(750-posn[0],750-posn[1]),area = posn2, special_flags = pygame.BLEND_ADD)

                            if(posn[1] + posn[3] >= 750):
                                posn2=posn[:]
                                posn2[1]=0
                                mask_surface.blit(surf[tid],(0,750-posn[1]),area = posn2, special_flags = pygame.BLEND_ADD)

                            rec = masks[ma].get_rect()
                            #rec.move(x*self.m_tile_size,y*self.m_tile_size)
                            self.m_map[x][y][0].get().blit(mask_surface,rec)

    def trees(self,x1,y1,x2,y2):

        huge_tree = pygame.transform.scale(globals.sprite_tree,(self.m_tile_size*3,self.m_tile_size*3))
        big_tree = pygame.transform.scale(globals.sprite_tree,(self.m_tile_size*2,self.m_tile_size*2))
        big_road = pygame.transform.scale(globals.sprite_road,(self.m_tile_size*2,self.m_tile_size*2))
        tree = pygame.transform.scale(globals.sprite_tree,(self.m_tile_size,self.m_tile_size))
        road = pygame.transform.scale(globals.sprite_road,(self.m_tile_size,self.m_tile_size))

        tobe = numpy.zeros((self.m_width,self.m_height))-10

        #populate the data in the matrices
        for x in range(x1,x2):
            for y in range(y1,y2):
                if(self.m_typemap[x][y] != 8 
                   and self.m_typemap[x][y] != 9
                   and self.m_height_map[y][x]<88
                   and self.m_height_map[y][x]>5):

                    if(self.m_wood_map[x][y] > self.m_tree_threshhold and self.m_height_map[y][x]>20):

                        tobe[x][y] = 1
                        self.m_collision_map[x][y] = 1

                    elif(self.m_wood_map_blurry[x][y] < self.m_road_threshhold):

                        tobe[x][y] = 2
                        self.m_collision_map[x][y] = -0.5
        
        #fill in the big ones
        for x in range(max(x1,2),min(x2,self.m_width-1)):
            for y in range(max(y1,2),min(y2,self.m_height-1)):

                count_huge_tree = 0
                count_tree = 0
                count_road = 0
                
                for x1 in range(-1,2):

                    for y1 in range(-1,2):

                        if(tobe[x+x1][y+y1]==1):
                            count_huge_tree +=1
                        else:
                            break

                for x1 in range(-1,1):

                    for y1 in range(-1,1):

                        if(tobe[x+x1][y+y1]==1):
                            count_tree +=1
                        elif(tobe[x+x1][y+y1]==2):
                            count_road +=1

                if(count_huge_tree == 9):
                    for x1 in range(-1,2):
                        for y1 in range(-1,2):
                            tobe[x+x1][y+y1]=0
                            self.m_map[x+x1][y+y1][0].get().blit(huge_tree,(0,0),(self.m_tile_size*(1+x1),self.m_tile_size*(1+y1),self.m_tile_size,self.m_tile_size))

                elif(count_tree == 4):
                    for x1 in range(-1,1):
                        for y1 in range(-1,1):
                            tobe[x+x1][y+y1]=0
                            self.m_map[x+x1][y+y1][0].get().blit(big_tree,(0,0),(self.m_tile_size*(1+x1),self.m_tile_size*(1+y1),self.m_tile_size,self.m_tile_size))

                elif(count_road == 4):
                    for x1 in range(-1,1):
                        for y1 in range(-1,1):
                            tobe[x+x1][y+y1]=0
                            self.m_map[x+x1][y+y1][0].get().blit(big_road,(0,0),(self.m_tile_size*(1+x1),self.m_tile_size*(1+y1),self.m_tile_size,self.m_tile_size))

        
        #finish off with the little ones
        for x in range(x1,x2):
            for y in range(y1,y2):
                for tile in self.m_map[x][y]:

                    if(tobe[x][y]==1):
                        tile.get().blit(tree,(0,0))

                    elif(tobe[x][y]==2):
                        tile.get().blit(road,(0,0))

    def draw(self):

        surf = pygame.Surface((self.m_tile_size*self.m_width,self.m_tile_size*self.m_height))
        
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                for tile in self.m_map[x][y]:
                    surf.blit(tile.get(), (x*self.m_tile_size,y*self.m_tile_size))

        return surf

    def clear_surface(self):

        self.m_map = None
        gc.collect()

    def draw_chunk(self,x1,y1,x2,y2):

        self.make_surface(x1,y1,x2,y2)
        surf = pygame.Surface((self.m_tile_size*(x2-x1),self.m_tile_size*(y2-y1)))
        
        for x in range(x1,min(x2,self.m_width)):
            for y in range(y1,min(y2,self.m_height)):
                for tile in self.m_map[x][y]:
                    surf.blit(tile.get(), ((x-x1)*self.m_tile_size,(y-y1)*self.m_tile_size))

        self.clear_surface()
        return surf

class Game_Map(object):

    def __init__(self):
        pass

    def init(self,size=4096, tiles=256, chunk_size=16, height_dist_list=(0,8,13,20,27,34,40,47,56,67,100), textures="Assets/Textures.png",masks="Assets/Texture Masks.png"):

        self.m_size = size
        self.m_tiles = tiles
        self.m_textures = textures
        self.m_masks = masks
        self.m_chunk_size = chunk_size
        self.m_surface_array =[([0]*(self.m_tiles/self.m_chunk_size)) for t in [0]*(self.m_tiles/self.m_chunk_size)]

        #mute the output of this
        save_stdout = sys.stdout
        sys.stdout = cStringIO.StringIO()

        #begin mapping
        water = map_generation.WeightedCaveFactory(int(12*math.log(tiles)-40),int(12*math.log(tiles)-40), 0.45).gen_map()

        height = map_generation.perlin_main(tiles, 180*tiles/256, 14, 10)
        dist = matrix_scale(stats_percentile(height),0,100).astype(int)
        height = matrix_redist(height,height_dist_list)

        woods = map_generation.dungeon_make(int(36*tiles/256.0/2)*2,int(36*tiles/256.0/2)*2,9,roundedness=10)

        tile_map = Tile_Map(height, water, woods, textures, masks, tiles, tiles, size/tiles)
        
        #self.m_surface = tile_map.draw()

        self.m_collision = tile_map.m_collision_map

        #unmute the output
        sys.stdout = save_stdout

        #stats time
        #print "Water Dist:",stats_percentile(tile_map.m_water_map).astype(int)
        #print "Wood Dist:",(stats_percentile(tile_map.m_wood_map)*100).astype(int)/100.0
        #print "Height Dist:",dist,"->",stats_percentile(height).astype(int)
        #print "Net Time:",time.time()-wall

        return tile_map

    def gen_chunk(self,tile_map, row, col):

        #mute the output of this
        save_stdout = sys.stdout
        sys.stdout = cStringIO.StringIO()

        x1=row*self.m_chunk_size
        x2=x1+self.m_chunk_size

        y1=col*self.m_chunk_size
        y2=y1+self.m_chunk_size

        self.m_surface_array[row][col]=tile_map.draw_chunk(x1,y1,x2,y2)

        #unmute the output
        sys.stdout = save_stdout

        return self.m_surface_array[row][col]

    def get_chunk(self,row,col):

        return self.m_surface_array[row][col]

    def gen_chunks(self,tile_map):

        for row in range(0,self.m_tiles/self.m_chunk_size):
            for col in range(0,self.m_tiles/self.m_chunk_size):

                x1=row*self.m_chunk_size
                x2=x1+self.m_chunk_size

                y1=col*self.m_chunk_size
                y2=y1+self.m_chunk_size

                self.m_surface_array[row][col]=tile_map.draw_chunk(x1,y1,x2,y2)

        return self

    def get_surface(self):

        return self.m_surface

    def get_collision(self):

        return self.m_collision

if __name__ == '__main__':

    pygame.init()
    pygame.font.init()
    random.seed()
    globals.window_surface = pygame.display.set_mode((512,512), 0, 32)
    globals.window_surface.fill((0,0,100))
    globals.sprite_tree = pygame.image.load('Assets/Tree.png').convert_alpha()
    globals.sprite_road = pygame.image.load('Assets/Brown_Road.png').convert_alpha()
    pygame.display.set_caption("Tile Test")
    pygame.display.update()
    mp = None

    for i in range(128,513,128):

        wall = time.time()

        mp = Game_Map()
        tm = mp.init(i*96,i)
        for x in range(0,i/16):
            for y in range(0,i/16):

                mp.gen_chunk(tm,x,y)
                surf = mp.get_chunk(x,y)
                gc.collect()
                pygame.image.save(surf,str(i)+"_("+str(x)+","+str(y)+")_chunk.png")
        gc.collect()

        globals.window_surface.blit(pygame.transform.scale(surf,(512,512)),(0,0))
        pygame.display.update()

        print i,":",time.time()-wall

    clock = pygame.time.Clock()
    while(True):
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 
                sys.exit()
            elif event.type == KEYDOWN:
                if(event.key == K_ESCAPE):
                    pygame.quit() 
                    sys.exit()
