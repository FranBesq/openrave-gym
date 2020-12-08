# openrave-gym
Testing OpeanAI gym interface with Openrave 0.9 

ecroEnv.py implementes the gym interface using openravepy API


## Dependencies

* Python 2.7

* OpenRave 0.9

* OpenAI gym

## Usage

Train an agent to get out of the maze:

```
python trainEcroEnv.py --num-episodes 1000 --save-path q_table.pickle --render True
```

 Try `python trainEcroEnv.py --help` to get the following help message
```
python trainEcroEnv.py --help
Usage: trainEcroEnv.py [OPTIONS]

Options:
  --num-episodes INTEGER  Number of episodes to train on  [default: 4]
  --save-path TEXT        Path to save the Q-table dump  [default:
                          q_table.pickle]
  --render INTEGER        Set viwer, 0 means no viwer, 1 for qtosq, 2 for
                          qtcoin  [default: 2]
  --help                  Show this message and exit.
```

Evaluate the agent you just trained

```
python evaluate.py --num-episodes 100 --q-path q_table.pickle
```

## Action and Observation space

By default both are discrete to work with Q-Learning, but can be switched to continuous normalized spaces when creating the env.

* Action space: move UP, RIGHT, LEFT, DOWN. Each move is an abstraction of the wheel speed of the ecro robot. See ecroEnv.py function `_get_vel_from_action(self, action)`

* Observation space: OR provides a transformation matrix. Positions `[0][3]` and `[1][3]` of this array are *x* and *y* coordinates of the robot. The integer part of these are taken to discretize the space into cells.

## Reward

Reward is defined in the `step()` function in ecroEnv.py

```
    if (obs[0] == GOAL_X) and (obs[1] == GOAL_Y):
      reward = 20
      done = True
    
    # This means an obstacle is found
    elif prev_obs == obs:
      reward = -10

    # Reward is Manhattan Distance
    else:
      reward = 1/((GOAL_X - obs[0]) + (GOAL_Y - obs[1]) + 1) 
```
* First if goal is reached set reward to 20 (this tells q-learning to stop epoch) and set *done* to *True*

* We dont use robot sensor to know if an obstacle is found, so if after moving, the same position as previously is reached, punish with negative reward.

* To guide the training with a simple euristic Manhattan distance is used. This can be deleted to augment reward sparsity.


## Acknowledgement

* [Openrave-tools](https://github.com/roboticslab-uc3m/openrave-tools) Used to generate maps
* [Q-Learning](https://github.com/satwikkansal/q-learning-taxi-v3) implementation used 



