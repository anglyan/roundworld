from roundworld.rlbug import Target1in5


env = Target1in5((2,3,4))
print(env.observation_state.shape)

state = env.reset()
