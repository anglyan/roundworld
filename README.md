# RoundWorld repository

This repository describes a lightweight first person point of view environment
called `roundworld` and the reinforcement learning environment `rlbug`, which
implements a series of lightweight tasks designed to explore to explore
offline and online continual reinforcement learning.

## About

This environment was developed in the context of DARPA's Lifelong Learning
Machines program and it is geared to exploring online and continual learning for
agents interacting in an open world environment.

As of 2020 we couldn't find an environment that was 1) lightweight,
2) easily reconfigurable, and 3) could be used to build curricula
or sequences of tasks where we can control which specific information
is reused over the lifetime of a single agent.

This repository contains the following:

  - `roundworld`: a package implementing a lightweight "engine" for a first 
    person point of view environment.
  - `rlbug`: a module within `roundworld` implementing a RL environment
    based on `roundworld`. Its interface is 
    gym-compatible, though `gymnasium` is not a dependency in order to
    keep the lightweight philosophy. A separate implementation fully
    integrated into `gymnasium` is in the works.

## Copyright and license

Copyright © 2020, UChicago Argonne, LLC

roundworld is distributed under the terms of BSD License. See [LICENSE](https://github.com/anglyan/roundworld/main/LICENSE)

## Citing

