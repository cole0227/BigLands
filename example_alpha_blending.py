import pygame, sys, pygame.time

#init pygame
pygame.init()

#init screen
screen=pygame.display.set_mode((800,600))
screen.fill((255,0,255))

#loading the images
texture=pygame.image.load("Assets/Textures.png").convert_alpha()
mask=pygame.image.load("Assets/Texture Masks.png").convert_alpha()


textured_mask=mask.copy()
textured_rect=textured_mask.get_rect()
textured_rect.center=600,300

textured_mask.blit(texture,(0,-6750),None,pygame.BLEND_ADD)
textured_mask.blit(texture,(750,-3750),None,pygame.BLEND_ADD)

screen.blit(texture,(0,-750))
screen.blit(texture,(750,-750))
screen.blit(textured_mask,textured_rect)

pygame.display.flip()

clock = pygame.time.Clock()
while 1:
    clock.tick(60)
    event=pygame.event.wait()
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_q]):
        sys.exit()
