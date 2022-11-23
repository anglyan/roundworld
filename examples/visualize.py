import pygame
from roundworld import RWorld
from roundworld.objects import Asset

import numpy as np
import time

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

    a1 = Asset(obid=1, size=0.5, height=2, reward=0)
    a2 = Asset(obid=2, size=0.5, height=4, reward=1)
    a3 = Asset(obid=3, size=0.1, height=3, reward=-1)
    
    X = 5 + 4*np.random.random(5)
    Y = -2 + 4*np.random.random(5)

    objects = {
        'obid' : [1, 2, 2, 3, 3],
        'X' : X,
        'Y' : Y,
    }

    assets = [a1.to_dict(), a2.to_dict(), a3.to_dict()]

    il = 0.2+0.8*np.random.random()
    cmax = int(256*il)

    palette = {
        'depthfade' : 0.01,
        'type' : 'rgb',
        'sky': (int(184), int(227), int(256)),
        'ground': (int(243), int(164), int(19)),
        1 : (np.random.randint(cmax),np.random.randint(cmax),np.random.randint(cmax)),
        2 : (np.random.randint(cmax),np.random.randint(cmax),np.random.randint(cmax)),
        3 : (np.random.randint(cmax),np.random.randint(cmax),np.random.randint(cmax)),
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
    c_sky, blist = world.get_background()
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

def process_visual(visual):
    left = visual[:,0:42,:]/255
    right = visual[:,42:,:]/255
    center = visual[:,21:63,:]/255
    left_bad = np.sum(left[0,:,:])
    left_good = np.sum(left[2,:,:])
    right_bad = np.sum(right[0,:,:])
    right_good = np.sum(right[2,:,:])
    center_bad = np.sum(center[0,:,:])
    center_good = np.sum(center[2,:,:])
    left = left_good-0.1*left_bad
    right = right_good-0.1*right_bad
    center = center_good - 0.1*center_bad
    print(left, center, right)
    return left, center, right


def run():
        
    pygame.init()
    conf = create_configuration()
    world = RWorld(conf)

    screen = pygame.display.set_mode([SCREEN_SIZE,SCREEN_SIZE])
    running = True
    clock = pygame.time.Clock()
    world.init()

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
        time.sleep(0.1)
        visual = world.get_visual()
        vl, vc, vr = process_visual(visual)
        vl += np.random.random()
        vr += np.random.random()
        vc += np.random.random()
        n = np.argmax(np.array([vl,vc,vr]))

        _, colid, colrw = world.step(n)
        if n != 1:
            _, colid, colrw = world.step(1)

        if len(colid) > 0:
            conf, palette, _ = create_configuration()
            world.reset(conf, palette)

        redraw = True

        if redraw:
            surface = create_background(background_slabs)
            surface = create_objects(surface, world)
            screen.blit(surface,(0,0))
            pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    
    run()

