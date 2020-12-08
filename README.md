# openrave-gym
Testing OpeanAI gym interface with Openrave 0.9 

ecroEnv.py implementes the gym interface using openravepy API


# Dependencies

* Python 2.7

* OpenRave 0.9

* OpenAI gym

# Usage

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

## Acknowledgement

* [Openrave-tools](https://github.com/roboticslab-uc3m/openrave-tools) Used to generate maps
* [Q-Learning](https://github.com/satwikkansal/q-learning-taxi-v3) implementation used 



