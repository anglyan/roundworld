from roundworld.rlbug import SaliencyTarget

import numpy as np


env = SaliencyTarget()

state = env.reset()
print(np.max(state))
