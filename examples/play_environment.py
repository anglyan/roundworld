import pygame
from roundworld import RWorld
from roundworld.objects import Asset

import numpy as np

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    )


TILE_WIDTH = 5
NTILES = 84
SCREEN_SIZE = TILE_WIDTH*NTILES
HALF_TILES = NTILES // 2
HALF_SCREEN = SCREEN_SIZE // 2

def create_configuration():

    a1 = Asset(obid=1, size=0.5, height=1, reward=0)
    a2 = Asset(obid=2, size=0.5, height=1, reward=1)
    a3 = Asset(obid=3, size=0.5, height=1, reward=-1)
    
    X = 8 + 1*np.random.random(5)
    Y = -3 + 1.5*np.arange(5)

    obid = [1, 1, 1, 2, 3]
    np.random.shuffle(obid)

    objects = {
        'obid' : obid,
        'X' : X,
        'Y' : Y,
    }

    assets = [a1.to_dict(), a2.to_dict(), a3.to_dict()]

    il = 0.2+0.8*np.random.random()
    cmax = int(256*il)

    palette = {
        'depthfade' : 0.0,
        'type' : 'rgb',
        'sky': (174, 214, 241),
        'ground': (243, 156, 18),
        1 : (0, 20, 255),
        2 : (255, 20, 0),
        3 : (100, 100, 100),
    }

    conf = {
        "objects" : objects,
        "palette" : palette,
        "assets" : assets
    }
    return conf



def create_background(background_slabs):
    surface = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
    surface.blit(background_slabs[0],(0,0))
    for i in range(HALF_TILES):
        surface.blit(background_slabs[i+1],(0,TILE_WIDTH*(HALF_TILES+i)))
    return surface

def create_background_slabs(world):
    c_sky, blist = world.renderer.get_background()
    background_slabs = []
    sky = pygame.Surface((SCREEN_SIZE, HALF_SCREEN))
    sky.fill(pygame.Color(*c_sky))
    background_slabs.append(sky)
    for i in range(HALF_TILES):
        ground_slab = pygame.Surface((SCREEN_SIZE, TILE_WIDTH))
        ground_slab.fill(pygame.Color(*blist[i]))
        background_slabs.append(ground_slab)
    return background_slabs

def create_objects(surface, world):
    rect_list = world.get_segmentation(color=True)
    for obj in rect_list:
        i, jmin, jmax, color = obj
        tile = pygame.Surface((TILE_WIDTH,(jmax-jmin)*TILE_WIDTH))
        tile.fill(pygame.Color(*color))
        surface.blit(tile, (i*TILE_WIDTH, jmin*TILE_WIDTH))
    return surface

def run(world):
        
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_SIZE,SCREEN_SIZE])
    running = True
    clock = pygame.time.Clock()

    background_slabs = create_background_slabs(world)

    screen.fill((255,255,255))
    surface = create_background(background_slabs)
    surface = create_objects(surface, world)
    screen.blit(surface,(0,0))
    pygame.display.flip()

    redraw = False

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pressed_keys = pygame.key.get_pressed()
        redraw = False
        if pressed_keys[K_LEFT]:
            world.step(0)
            redraw = True
        if pressed_keys[K_RIGHT]:
            world.step(2)
            redraw = True
        if pressed_keys[K_DOWN]:
            world.step(3)
            redraw = True
        if pressed_keys[K_UP]:
            world.step(1)
            redraw = True

        if redraw:
            surface = create_background(background_slabs)
            surface = create_objects(surface, world)
            screen.blit(surface,(0,0))
            pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    
    conf = create_configuration()
    world = RWorld(conf)
    run(world)


