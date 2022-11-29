# RoundWorld repository

This repository describes a lightweight first person point of view environment
called `roundworld` and the reinforcement learning environment `rlbug`, which
implements a series of lightweight tasks designed to explore
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

`rlbug` was used as a testbed for the general policy algorithm inspired
on the architecture of the insect brain. This work was presented at the
*Offline Reinforcement Learning Workshop* at the
Neural Information Processing Systems Conference (NeurIPS) 2022.

## Tasks

There are currently three tasks in `rlbug`:

- `SingleTarget` is a task where the agent has to reach an object. The object's
  position and size is randomly generated during each episode. The task can
  be initialized with a number between 1 and 27 representing the type of object.
  If a number is used the same type of object is used in all episodes. Otherwise,
  a random object is selected for each episode.

- `Target1in5` is a task where the agent need to reach one target among five
  objects. Each task is initialized by a tuple of three numbers, corresponding
  to the target, a decoy, and background objects. The position of the objects
  is chosen randomly at the start of each episode to prevent the agent from
  learning to move in a predetermined trajectory.

- `SaliencyTarget` is a task where the agent needs to reach an object using a
  saliency input. This can be used as a baseline example.

Check the `examples` folder for some trivial examples.

## Copyright and license

Copyright © 2020, UChicago Argonne, LLC

roundworld is distributed under the terms of BSD License. See [LICENSE](https://github.com/anglyan/roundworld/blob/main/LICENSE)


