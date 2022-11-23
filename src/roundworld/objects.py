"""Object lists"""

import numpy as np

class Asset:
    def __init__(self, obid, size, height, reward):
        self.obid = obid
        self.size = size
        self.height = height
        self.reward = reward
        
    def to_dict(self):
        return {
            "obid" : self.obid,
            "size" : self.size,
            "height" : self.height,
            "reward" : self.reward
        }

def dict_to_asset(d):
    return Asset(d["obid"], d["size"], d["height"], d["reward"])

class Objects:

    def __init__(self, obj_dict, asset_list):

        self.asset_dict = {
            asset["obid"] : dict_to_asset(asset) for asset in asset_list
            }

        if obj_dict is not None:
            self.xl0 = np.array(obj_dict["X"])
            self.yl0 = np.array(obj_dict["Y"])
#           self.size = obj_dict["size"]
#           self.height = obj_dict["height"]
            self.obid = obj_dict["obid"]
            self.size = [self.asset_dict[oid].size for oid in self.obid]
            self.obreward = [self.asset_dict[oid].reward for oid in self.obid]
            self.height = [self.asset_dict[oid].height for oid in self.obid]

            self.visible = obj_dict.get("visible", np.ones(len(self.xl0)))
            self.empty = False
        else:
            self.empty = True

    def __len__(self):
        return 0 if self.empty else len(self.obid)

    def init(self):
        if not self.empty:
            self.xl = self.xl0.copy()
            self.yl = self.yl0.copy()

    



    