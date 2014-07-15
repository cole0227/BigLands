import sys
import cStringIO
import time
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
        self.m_height_map = scipy.ndimage.zoom(self.m_height_map, (max(width+1.0,height+1.0)**2/self.m_height_map.size)**0.5, order=4)

        self.m_water_map = scipy.ndimage.zoom(self.m_water_map, (max(width+1.0,height+1.0)**2/self.m_water_map.size)**0.5, order=4)
        self.m_water_map = gaussian_blur.gaussian_blur(self.m_water_map,1)
        print self.m_height_map.shape,"/",self.m_water_map.shape

        self.m_map = defaultdict(lambda  : defaultdict(list))
        print len(self.m_map),',',len(self.m_map[0])
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
                if(self.m_typemap[x][y] == 8 or self.m_typemap[x][y] == 9 or self.m_typemap[x][y] == 1):
                    self.m_wood_map[x][y] = 0

        self.trees()

        #let's set up the collision map:
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                if(self.m_height_map[y][x]>5 and self.m_typemap[x][y] != 8 and self.m_typemap[x][y] != 9):
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
                
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                surf = pygame.Surface((self.m_tile_size,self.m_tile_size))
                surf.fill((255,0,255))
                self.m_map[x][y].append(Tile(-1,surf))

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
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
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

    def trees(self):

        huge_tree = pygame.transform.scale(globals.sprite_tree,(self.m_tile_size*3,self.m_tile_size*3))
        big_tree = pygame.transform.scale(globals.sprite_tree,(self.m_tile_size*2,self.m_tile_size*2))
        big_road = pygame.transform.scale(globals.sprite_road,(self.m_tile_size*2,self.m_tile_size*2))
        tree = pygame.transform.scale(globals.sprite_tree,(self.m_tile_size,self.m_tile_size))
        road = pygame.transform.scale(globals.sprite_road,(self.m_tile_size,self.m_tile_size))

        tobe = numpy.zeros((self.m_width,self.m_height))

        #populate the data in the matrices
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
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
        for x in range(1,self.m_width-1):
            for y in range(1,self.m_height-1):

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
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                for tile in self.m_map[x][y]:

                    if(tobe[x][y]==1):
                        tile.get().blit(tree,(0,0))

                    elif(tobe[x][y]==2):
                        tile.get().blit(road,(0,0))
                    

    def draw(self):

        surf = pygame.Surface((self.m_tile_size*self.m_width,self.m_tile_size*self.m_height))
        
        surf.blit(self.m_sprite_sheet.image_by_index(750,0),(  0,  0))
        surf.blit(self.m_sprite_sheet.image_by_index(750,0),(750,  0))
        surf.blit(self.m_sprite_sheet.image_by_index(750,0),(  0,750))
        surf.blit(self.m_sprite_sheet.image_by_index(750,0),(750,750))
        
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                for tile in self.m_map[x][y]:
                    surf.blit(tile.get(), (x*self.m_tile_size,y*self.m_tile_size))

        return surf

class Game_Map(object):

    def __init__(self,size=4096,tiles=256,textures="Assets/Textures.png",masks="Assets/Texture Masks.png"):

        self.m_size = size
        self.m_tiles = tiles
        self.m_textures = textures
        self.m_masks = masks

        #mute the output of this, and start counting
        save_stdout = sys.stdout
        sys.stdout = cStringIO.StringIO()

        wall = time.time()

        #begin mapping
        water = map_generation.WeightedCaveFactory(40*tiles/256, 40*tiles/256, 0.45).gen_map()

        height = map_generation.perlin_main(tiles, 180*tiles/256, 14, 10)

        woods = map_generation.dungeon_make(int(36*tiles/256.0),int(36*tiles/256.0),9,roundedness=10)

        tile_map = Tile_Map(height, water, woods, textures, masks, tiles, tiles, size/tiles)
        
        self.m_surface = tile_map.draw()
        self.m_collision = tile_map.m_collision_map

        #unmute the output
        sys.stdout = save_stdout

        print "Net Time:",time.time()-wall

    def get_surface(self):

        return self.m_surface

    def get_collision(self):

        return self.m_collision

if __name__ == '__main__':

    pygame.init()
    pygame.font.init()
    random.seed()
    globals.window_surface = pygame.display.set_mode((1024,1024), 0, 32)
    globals.window_surface.fill((0,0,100))
    globals.sprite_tree = pygame.image.load('Assets/Tree.png').convert_alpha()
    globals.sprite_road = pygame.image.load('Assets/Road.png').convert_alpha()
    pygame.display.set_caption("Tile Test")
    pygame.display.update()

    mp = Game_Map(8192,256).get_surface()
    globals.window_surface.blit(mp,(0,0))
    pygame.image.save(mp,"screen.png")

    pygame.display.update()
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

if __name__ == '__main__' and 0==1:

    #mute the output of this shit
    save_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()

    wall = time.time()

    #core initiation
    pygame.init()
    pygame.font.init()
    random.seed()
    globals.screen_size=1024*5
    globals.window_surface = pygame.display.set_mode((min(globals.screen_size,1024),min(globals.screen_size,1024)), 0, 32)
    globals.window_surface.fill((0,0,100))
    globals.sprite_tree = pygame.image.load('Assets/Tree.png').convert_alpha()
    globals.sprite_road = pygame.image.load('Assets/Road.png').convert_alpha()
    pygame.display.set_caption("Tile Test")
    pygame.display.update()

    #water = map_generation.WeightedCaveFactory(20, 20, 0.45).gen_map()
    water = map_generation.WeightedCaveFactory(40, 40, 0.45).gen_map()

    #height = map_generation.perlin_main(128, 45, 14, 10)
    height = map_generation.perlin_main(256, 180, 14, 10)

    #woods = map_generation.dungeon_make(18,18,9,roundedness=10)
    woods = map_generation.dungeon_make(36,36,9,roundedness=10)

    #t = Tile_Map(height, water, woods, "Assets/Textures.png", "Assets/Texture Masks.png", 128, 128, 8*globals.screen_size/1024)
    t = Tile_Map(height, water, woods, "Assets/Textures.png", "Assets/Texture Masks.png", 256, 256, 4*globals.screen_size/1024)
    
    rm = t.draw()
    pygame.image.save(rm,"screen.png")

    #unmute the output
    sys.stdout = save_stdout

    print "Net Time:",time.time()-wall
    i = 0
    clock = pygame.time.Clock()
    while(True):
        clock.tick(60)
        wall = time.time()
        i+=1

        globals.window_surface.blit(rm,(0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 
                sys.exit()
            elif event.type == KEYDOWN:

                if(event.key == K_ESCAPE):
                    pygame.quit() 
                    sys.exit()
                elif(event.key == K_F2):
                    pygame.image.save(globals.window_surface,"screen.png")
                elif(event.key == K_F1):
                    h = map_generation.perlin_main(128, 20, 10, 6)
                    t = Tile_Map(h, w, "Assets/Huge Tileset.png",64,64, 16)
        if(i>1000):
            print "Delta:",(time.time()-wall)
            i=0
