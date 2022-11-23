from roundworld.objects import Asset
import numpy as np

def create_1in5_task(target_id, decoy_id, background_id):
    """Configuration for a RLBug task involving 1 in 5 target
    selection
    
    """

    a1 = Asset(obid=1, size=0.5, height=1, reward=1)
    a2 = Asset(obid=2, size=0.5, height=1, reward=0)
    a3 = Asset(obid=3, size=0.5, height=1, reward=0)
    
    X = 8 + 1*np.random.random(5)
    Y = 3 - 1.5*np.arange(5)

    obid = [1, 2, 3, 3, 3]
    np.random.shuffle(obid)

    objects = {
        'obid' : obid,
        'X' : X,
        'Y' : Y,
    }

    assets = [a1.to_dict(), a2.to_dict(), a3.to_dict()]

    c_array = [ 0, 128, 255]
    rgb_tasks = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                rgb_tasks.append((c_array[i],c_array[j],c_array[k]))

    r, g, b = rgb_tasks[target_id]    
    r2, g2, b2 = rgb_tasks[decoy_id]    
    r3, g3, b3 = rgb_tasks[background_id]    

    palette = {
        'depthfade' : 0.0,
        'type' : 'rgb',
        'sky': (174, 214, 241),
        'ground': (243, 156, 18),
        1 : (r, g, b),
        2 : (r2, g2, b2),
        3 : (r3, g3, b3),
    }

    conf = {
        "objects" : objects,
        "palette" : palette,
        "assets" : assets
    }
    return conf

def create_1target_task(task_number=None):

    size = 0.3 + 0.4*np.random.random()
    height = 0.5 + np.random.random()
    a1 = Asset(obid=1, size=size, height=height, reward=1)
    
    dx = 6 + 4*np.random.random()
    dy = 0.9*dx*(np.random.random()-0.5)
    X = np.array([dx])
    Y = np.array([dy])

    obid = [1]
    np.random.shuffle(obid)

    objects = {
        'obid' : obid,
        'X' : X,
        'Y' : Y,
    }

    assets = [a1.to_dict()]

    c_array = [ 20, 128, 236]
    rgb_task = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                rgb_task.append([i,j,k])

    if task_number is None:
        task_number = np.random.randint(27)

    i, j, k = rgb_task[task_number]

    r = c_array[i] + np.random.randint(-10,10)
    g = c_array[j] + np.random.randint(-10,10)
    b = c_array[k] + np.random.randint(-10,10)

    palette = {
        'depthfade' : 0.0,
        'type' : 'rgb',
        'sky': (174, 214, 241),
        'ground': (243, 156, 18),
        1 : (r, g, b),
    }

    conf = {
        "objects" : objects,
        "palette" : palette,
        "assets" : assets
    }
    return conf, task_number

def create_saliency_task():

    size = 0.3 + 0.4*np.random.random()
    height = 0.5 + np.random.random()
    a1 = Asset(obid=1, size=size, height=height, reward=1)
    
    dx = 6 + 4*np.random.random()
    dy = 0.9*dx*(np.random.random()-0.5)
    X = np.array([dx])
    Y = np.array([dy])

    obid = [1]
    np.random.shuffle(obid)

    objects = {
        'obid' : obid,
        'X' : X,
        'Y' : Y,
    }

    assets = [a1.to_dict()]


    palette = {
        'depthfade' : 0.0,
        'type' : 'mono',
        'sky': 0,
        'ground': 0,
        1 : 1.0,
    }

    conf = {
        "objects" : objects,
        "palette" : palette,
        "assets" : assets
    }
    return conf

    

