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

        self.m_index = index
        self.m_surface = surface

    def get(self):

        return self.m_surface

class Tile_Map(object):

    def __init__(self, height_map, water_map, tileset_image, width, height, tile_size):

        self.m_width = width
        self.m_height = height
        self.m_tile_size = tile_size
        self.m_sprite_sheet = Sprite_Sheet(tileset_image)
        self.m_height_map = map_generation.matrix_scale(height_map,0,100)
        self.m_water_map = numpy.array(water_map)
        
        self.m_height_map = scipy.ndimage.zoom(self.m_height_map, max(width+1,height+1)/(self.m_height_map.size)**0.5, order=4)
        self.m_water_map = scipy.ndimage.zoom(self.m_water_map, max(width+1,height+1)/(self.m_water_map.size)**0.5, order=4)

        self.m_map = defaultdict(lambda  : defaultdict(list))
        self.fill()

    def fill(self):

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

        for x in range(0,self.m_width):
            for y in range(0,self.m_height):
                for tile in self.m_map[x][y]:
                    globals.window_surface.blit(
                        tile.get(),
                        (x*self.m_tile_size,y*self.m_tile_size))




if __name__ == '__main__':

    #core initiation
    pygame.init()
    pygame.font.init()
    random.seed()
    globals.window_surface = pygame.display.set_mode((1024,1024), 0, 32)
    pygame.display.set_caption("Tile Test")

    w = map_generation.CA_CaveFactory(128, 32, 0.55).gen_map()
    h = map_generation.perlin_main(256, 80, 10, 7)
    #h = map_generation.perlin_main(128, 40, 14, 10)
    #h = map_generation.perlin_main(20, 0, 1, 3)

    #t = Tile_Map(h, w, "Assets/Textures.png", 64, 64, 16)
    #t = Tile_Map(h, w, "Assets/Textures.png", 256, 256, 4)
    t = Tile_Map(h, w, "Assets/Textures.png", 512, 512, 2)

    
    i = 0
    while(True):
        i+=1
        wall = time.time()
        t.draw()
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
