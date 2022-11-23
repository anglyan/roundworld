from roundworld import RWorld

import numpy as np

from PIL import Image


colordict = {
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "purple" : (127,0,255),
    "yellow" :(255, 255, 0),
    "cyan" : (0, 255, 255),
    "darkred" : (125,0,0)
}



#data = np.zeros((10000,84*84*3),dtype=np.uint8)


world = RWorld()

for i in range(10000):

    size = 0.2 + 0.4*np.random.random(5)
    height = 0.5 + 1.5*np.random.random(5)
    reward = [0]*5
    assets = []
    for i in range(5):
        d = {
            'obid' : i+1,
            'size' : size[i],
            'height' : height[i],
            'reward' : reward[i]
        }
        assets.append(d)

    X = 1 + 4*np.random.random(5)
    Y = -2 + 4*np.random.random(5)

    objects = {
        'obid' : [1, 2, 3, 4, 5],
        'X' : X,
        'Y' : Y,
    }

    il = 0.2+0.8*np.random.random()
    cmax = int(256*il)

    palette = {
        'depthfade' : 0.01,
        'type' : 'rgb',
        'sky': (int(il*184), int(il*227), int(il*256)),
        'ground': (int(il*243), int(il*164), int(il*19)),
        1 : (np.random.randint(cmax),np.random.randint(cmax),np.random.randint(cmax)),
        2 : (np.random.randint(cmax),np.random.randint(cmax),np.random.randint(cmax)),
        3 : (np.random.randint(cmax),np.random.randint(cmax),np.random.randint(cmax)),
        4 : (np.random.randint(cmax),np.random.randint(cmax),np.random.randint(cmax)),
        5 : (np.random.randint(cmax),np.random.randint(cmax),np.random.randint(cmax)),
    }

    conf = {
        "objects" : objects,
        "palette" : palette,
        "assets" : assets
    }

    world.reset(conf)
    world.get_visual()

#np.save("batch7.npy", data)





