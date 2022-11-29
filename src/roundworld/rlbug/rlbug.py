""""
A openAI gym environment for navigation with an embodied agent
"""

import numpy as np
from roundworld.rworld import RWorld
from collections import namedtuple

State = namedtuple("State", ["shape"])


class RLBug:
    """
    Description:

        Base class 

    Observation:
        Type: 84x84x3 np.uint8 numpy array with input field

    Actions:
        Type: Discrete(5)
        Num   Action
        0     Turn left 5 degrees
        1     Turn right 5 degrees
        2     Turn left 5 degrees and move forward
        3     Move Forward
        4     Turn right 5 degrees and move foreward


    Reward:
        The agent receives feedback based on collisions with the right objects

    Starting State:
        Agent starts from the origin looking towards the positive x direction.
        The collection of objects is passed through the parameter conf.

    Episode Termination:
        When the agent reaches a reward object or after a maximum number of steps


    Parameters
    ----------

    conf : a configuration dictionary.

    max_steps : maximum number of steps. Default is 200.

    fast_ending : task ends prematurely if no objects are within the
        agent's visual field. Default is False.

    """

    def __init__(self, conf, max_steps=200, fast_ending=False):
        self.max_steps = max_steps
        self.conf = conf
        self.world = RWorld(conf)
        self.fast_ending = fast_ending
        if self.world.palette.type == "rgb":
            self.observation_state = State(shape=(3,84,84))
        else:
            self.observation_state = State(shape=(84,84))
        self.action_state = State(5)

    def reset(self, conf=None):

        if conf != None:
            self.conf = conf

        self.world.reset(self.conf)
        self.nsteps = 0
        self.done = False
        self.state = self.get_visual()
        return self.state


    def get_visual(self):
        v = self.world.get_visual()
        if self.world.palette.type == "rgb":
            return np.transpose(v, (0,2,1))
        else:
            return np.expand_dims(np.transpose(v,(1,0)), 0)


    def step(self, action):
        self.nsteps += 1
        reward = 0
        done = False

        if action == 0 or action == 2:
            _, _, _ = self.world.step(0)
        elif action == 1 or action == 4:
            _, _, _ = self.world.step(2)
        
        if action in [2,3,4]:
            dx, col_ids, col_rewards = self.world.step(1)
            if len(col_ids) > 0:
                done = True
                reward += col_rewards[0]

        self.state = self.get_visual()
        if self.fast_ending and (not self.world.has_objects_in_view):
            done = True
 
        if self.nsteps == self.max_steps:
            done = True
        
        return self.state, reward, done, {}

