from .rlbug import RLBug
from .confs import create_1in5_task, create_saliency_task, create_1target_task


class Target1in5(RLBug):
    """RLBug task involving learning to reach one out of five objects.
    
    """

    def __init__(self, ntask, normalize_range=False):
        self.ntask = ntask
        self.normalize_range = normalize_range
        conf = create_1in5_task(*self.ntask)
        super().__init__(conf)

    def transform(self, s):
        if self.normalize_range:
            return s/255.0
        else:
            return s

    def step(self, action):
        state, reward, done, d = super().step(action)
        return self.transform(state), reward, done, d
 
 
    def reset(self):
        conf = create_1in5_task(*self.ntask)
        return self.transform(super().reset(conf))
    

class SaliencyTarget(RLBug):
    """Reach an object using saliency as input
    
    """

    def __init__(self, normalize_range=False):
        self.normalize_range = normalize_range
        conf = create_saliency_task()
        super().__init__(conf)

    def transform(self, s):
        if self.normalize_range:
            return s/255.0
        else:
            return s

    def step(self, action):
        state, reward, done, d = super().step(action)
        return self.transform(state), reward, done, d
 
    def reset(self):
        conf = create_saliency_task()
        return self.transform(super().reset(conf))


class SingleTarget(RLBug):
    """Reach a single object based on visual input.
    
    """

    def __init__(self, ntask, normalize_range=False):
        self.ntask = ntask
        self.normalize_range = normalize_range
        conf = create_1target_task(self.ntask)
        super().__init__(conf)

    def transform(self, s):
        if self.normalize_range:
            return s/255.0
        else:
            return s

    def step(self, action):
        state, reward, done, d = super().step(action)
        return self.transform(state), reward, done, d
 
 
    def reset(self):
        conf = create_1target_task(self.ntask)
        return self.transform(super().reset(conf))
  