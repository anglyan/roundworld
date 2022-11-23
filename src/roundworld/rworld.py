"""
A minimal, pure Python engine for a first person POV agent
"""

import numpy as np
from collections import namedtuple

from .raycast import raycast, Screen, get_rectangles
from .renderer import  Renderer, Palette
from .objects import Objects


class RWorld:
    """
    A first person POV environment with round objects. 

    RWorld implements a simple environment where an agent is embedded
    in a world with round objects.


    """

    def __init__(self, conf={}, imsize=84):

        self.imwidth = imsize
        self.screen = Screen(self.imwidth)
        self.imheight = imsize

        self.dl = 0.2
        self.agent_size = 0.5
        self.agent_height = 0.5
        self.dangle = 5

        self.cangles = {i:np.cos(i/180*np.pi) for i in range(360)}
        self.sangles = {i:np.sin(i/180*np.pi) for i in range(360)}

        self.dnxm = self.cangles[self.dangle]
        self.dnxp = self.dnxm
        self.dnyp = self.sangles[self.dangle]
        self.dnym = - self.dnyp
        self.reset(conf, init=True)


    def reset(self, conf, init=True):
        """Reset the configuration and optionally the
        palette used for rendering"""

        self.conf = conf.get("objects", None)
        palette = conf.get("palette", "default")
        self.assets = conf.get("assets", [])

        self.palette = Palette(palette)
        self.renderer = Renderer(self.screen, self.palette)

        self.objs = Objects(self.conf, self.assets)

        if self.conf is not None:
            self.visible = self.conf.get("visible", np.ones(len(self.objs)))
            if init:
                self.init()


    def init(self):
        """Initializes the environment, setting the agent at the origin"""

        self.x = 0
        self.y = 0
        self.angle = 0
        self.objs.init()


    def get_visual(self, saliency=False):

        recs = self.get_segmentation(color=False)
        return self.renderer.render(recs, saliency)

    def get_segmentation(self, color=True):
        cols = raycast(self.screen, self.objs)
        self.has_objects_in_view = (max([len(c) for c in cols]) > 0)
        seg_list = get_rectangles(cols, self.objs.height, self.objs.obid, self.agent_height)
        if color:
            seg_list = self.renderer.colorize_rectangles(seg_list)
        return seg_list


    def get_saliency(self):
        recs = self.get_segmentation(color=False)
        return self.renderer.render_saliency(recs)


    def step(self, action):
        """
        Execute an action

        If as a result of the movement the agent collides with one or more objects, returns the 
        object id, and the list of rewards, and ignores the request to move. 
        """

        dx = 0
        if action == 0:
            self.angle += self.dangle
            if self.angle >= 360:
                self.angle = self.angle - 360
        elif action == 2:
            self.angle -= self.dangle
            if self.angle < 0:
                self.angle = 360+self.angle
        elif action == 1:
            dx = self.dl
        elif action == 3:
            dx = -self.dl
        else:
            raise ValueError("action not known")

        xt = self.objs.xl-dx
        yt = self.objs.yl.copy()
        if action == 1 or action == 3:
            d = np.sqrt(xt*xt+yt*yt)-self.agent_size
            d[self.objs.visible == 0] = 1000
            col_list = np.where(d<self.objs.size)[0]
            if len(col_list) > 0:
                return dx, col_list, [self.objs.obreward[i] for i in col_list]
            else:
                self.objs.xl = xt
                self.objs.yl = yt
                self.x += dx*self.cangles[self.angle]
                self.y += dx*self.sangles[self.angle]
        elif action == 0:
            self.objs.xl = xt*self.dnxp + yt*self.dnyp
            self.objs.yl = -xt*self.dnyp + yt*self.dnxp
        elif action == 2:
            self.objs.xl = xt*self.dnxm + yt*self.dnym
            self.objs.yl = -xt*self.dnym + yt*self.dnxm
        return dx, [], []

