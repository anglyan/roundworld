from roundworld.rlbug import SingleTarget

import numpy as np

env = SingleTarget(1)

state = env.reset()
print(np.max(state))

