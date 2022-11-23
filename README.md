# RoundWorld repository

This repository describes a lightweight first person point of view environment
called `roundworld` and the reinforcement learning environment `rlbug`, which
implements a series of lightweight tasks designed to explore to explore
offline and online continual reinforcement learning.

## About

This environment was developed in the context of DARPA's Lifelong Learning
Programs and it is geared to exploring online and continual learning for
agents interacting in an open world environment.

As of 2020 we couldn't find an environment that was 1) lightweight,
2) easily reconfigurable, and 3) could be used to build curricula
or sequences of tasks where we can control which specific information
is reused over the lifetime of a single agent.

This repository contains the following packages:

  - `roundworld`: a lightweight "engine" implementing a first person point of
    view environment.
  - `rlbug`: a RL environment built on top of roundworld. Its interface 
    gym-compatible, though `gymnasium` is not a dependency in order to
    keep the lightweight philosophy. A separate implementation fully
    integrated into `gymnasium` is in the works.


