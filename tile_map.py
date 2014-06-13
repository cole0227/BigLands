import time
import sys
import random
from collections import defaultdict

import numpy
import scipy
import scipy.ndimage
import pygame
from pygame.locals import *
import pygame.time
import pygame.font

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

    def __init__(self, height_map, water_map, tileset_image, masks_image, width, height, tile_size):

        self.m_width = width
        self.m_height = height
        self.m_tile_size = tile_size
        self.m_sprite_sheet = Sprite_Sheet(tileset_image)
        self.m_masks = Sprite_Sheet(masks_image)
        self.m_height_map = map_generation.matrix_scale(height_map,0,100)
        self.m_water_map = numpy.array(water_map)
        
        print self.m_height_map.shape,"/",self.m_water_map.shape
        self.m_height_map = scipy.ndimage.zoom(self.m_height_map, (max(width+1.0,height+1.0)**2/self.m_height_map.size)**0.5, order=4)
        self.m_water_map = scipy.ndimage.zoom(self.m_water_map, (max(width+1.0,height+1.0)**2/self.m_water_map.size)**0.5, order=4)
        print self.m_height_map.shape,"/",self.m_water_map.shape

        self.m_map = defaultdict(lambda  : defaultdict(list))
        print len(self.m_map),',',len(self.m_map[0])
        self.march()

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

        self.m_typemap = numpy.zeros((self.m_width,self.m_height))

        print "Typing..."
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):

                if(self.m_water_map[x][y] > 1.0):

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

                    else:
                        self.m_typemap[x][y]=7 # beach

                elif(self.m_water_map[x][y] > 0.95):
                    self.m_typemap[x][y]=8 # shallow water

                else:
                    self.m_typemap[x][y]=9 # deep water

        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                surf = pygame.Surface((self.m_tile_size,self.m_tile_size))
                surf.fill((255,0,255))
                self.m_map[x][y].append(Tile(-1,surf))

        print "Blitting..."
        for x in range(0,self.m_width):
            for y in range(0,self.m_height):

                tid = self.m_typemap[x][y]

                if( self.m_typemap[x][y] != -1):

                    surf = self.m_sprite_sheet.image_by_index(750,tid)
                    posn = [(x*self.m_tile_size)%750,(y*self.m_tile_size)%750,self.m_tile_size,self.m_tile_size]

                    self.m_map[x][y][0].get().blit(surf,(0, 0),area=posn)

                    #covers the edge cases where it needs to tile
                    if(posn[0] + posn[2] >= 750):
                        self.m_map[x][y][0].get().blit(surf,(750-posn[0], 0),area=posn)

                        if(posn[1] + posn[3] >= 750):
                            self.m_map[x][y][0].get().blit(surf,(750-posn[0],750-posn[1]),area=posn)

                    if(posn[1] + posn[3] >= 750):
                        self.m_map[x][y][0].get().blit(surf,(0,750-posn[1]),area=posn)

    def __old_march(self):

        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                if(self.m_water_map[y][x] > 1):
                    tid = 7-int((self.m_height_map[y][x]-5)/14.3)

                    self.m_map[x][y].append(Tile(tid,pygame.transform.scale(self.m_sprite_sheet.image_by_index(750,tid)
                            ,(self.m_tile_size,self.m_tile_size))))

                elif(self.m_water_map[y][x] > 0.9):

                    self.m_map[x][y].append(Tile(8,pygame.transform.scale(self.m_sprite_sheet.image_by_index(750,8)
                            ,(self.m_tile_size,self.m_tile_size))))
                else:
                    self.m_map[x][y].append(Tile(9,pygame.transform.scale(self.m_sprite_sheet.image_by_index(750,9)
                            ,(self.m_tile_size,self.m_tile_size))))

    def draw(self):

        surf = pygame.Surface((1024,1024))

        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                for tile in self.m_map[x][y]:
                    surf.blit(tile.get(), (x*self.m_tile_size,y*self.m_tile_size))

        return surf




if __name__ == '__main__':

    #core initiation
    pygame.init()
    pygame.font.init()
    random.seed()
    globals.window_surface = pygame.display.set_mode((1024,1024), 0, 32)
    pygame.display.set_caption("Tile Test")

    w = map_generation.CA_CaveFactory(32, 32, 0.55).gen_map()
    #h = map_generation.perlin_main(256, 80, 10, 7)
    h = map_generation.perlin_main(128, 40, 14, 10)
    #h = map_generation.perlin_main(32, 0, 1, 3)

    #t = Tile_Map(h, w, "Assets/Textures.png", "Assets/Texture Masks.png", 16, 16, 64)
    t = Tile_Map(h, w, "Assets/Textures.png", "Assets/Texture Masks.png", 64, 64, 16)
    #t = Tile_Map(h, w, "Assets/Textures.png", "Assets/Texture Masks.png", 128, 128, 8)
    #t = Tile_Map(h, w, "Assets/Textures.png", "Assets/Texture Masks.png", 256, 256, 4)
    rm = t.draw()

    
    i = 0
    while(True):
        i+=1
        wall = time.time()

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
                elif(event.key == K_F1):
                    h = map_generation.perlin_main(128, 20, 10, 6)
                    t = Tile_Map(h, w, "Assets/Huge Tileset.png",64,64, 16)
        if(i>100):
            print "Delta:",(time.time()-wall)
            i=0
