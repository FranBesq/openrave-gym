import gym
import time
import numpy as np
from gym import spaces
from openravepy import *

GOAL_X = 14
GOAL_Y = 10
MAX_X = 11
MAX_Y = 15

class EcroEnv(gym.Env):
  """Custom Environment to control Ecron robot in openrave using gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self, orenv=None, normActions=False, debug=True):

    self.orenv = orenv #Openrave env
    self.debug = debug
    if normActions:
      self.normActions = True
    else:
      self.normActions = False

    super(EcroEnv, self).__init__()

    # Action space is velocity of each weel 
    if self.normActions is True:
        self.action_space = spaces.Box(low=0, high=1, shape=
                    (4,), dtype=float)
        self.observation_space = spaces.Box(low=0, high=100, shape=
                (2,), dtype=np.uint8)
    # Use discrete action space
    else:
      self.action_space = spaces.Discrete(4)
      self.observation_space = spaces.Tuple((
            spaces.Discrete(MAX_X),
            spaces.Discrete(MAX_Y)))

  def step(self, action):

    prev_obs = self._get_obs()

    # In case action is a continuou or a discrete value
    if self.normActions:  
      velocities = [i*10 for i in action]
    else:
      velocities = self._get_vel_from_action(action)

    self.control.SetDesired(velocities)
    time.sleep(0.5)#Let robot in that direction for sleep time

    reward = 0
    done = False
    obs = self._get_obs()

    #Compute reward
    if (obs[0] == GOAL_X) and (obs[1] == GOAL_Y):
      reward = 20
      done = True
    elif prev_obs == obs:
      reward = -10
    #Reward is Manhattan Dist
    else:
      reward = 1/((GOAL_X - obs[0]) + (GOAL_Y - obs[1]) + 1) #+1 to avoid dividing by 0
    
    if self.debug:
      print("Reward: "+str(reward))
      print("Current cell: "+str(obs))
      print("Action taken: "+str(action))

    return obs, reward, done, None

  def reset(self):
    # Reset the state of the environment to initial position
    self.orenv.Load('/home/francisco/Documents/Robot_Sim/openrave-gym/map.env.xml') # load a simple scene
    self.robot = self.orenv.GetRobots()[0] # get the first robot
    print("Using robot: ", self.robot.GetName())
    self.robot.SetController(RaveCreateController(self.orenv,'idealvelocitycontroller'),range(self.robot.GetDOF()),0)
    self.control = self.robot.GetController()

    self.orenv.StartSimulation(timestep=0.001)

    return self._get_obs() # a falta de definir una observacion

    
  def render(self, mode='human', close=False):
    # Render the environment to the screen
    return 0

  #Computes current cell given Transform matrix
  def _get_obs(self):
    transform = self.robot.GetTransform()
    positionX = int(transform[0][3])
    positionY = int(transform[1][3])
    #pos = [positionX, positionY]
    #return pos

    return (positionX, positionY)

  # Given a discrete action returns velocity vector
  def _get_vel_from_action(self, action):
    # Go backwards
    if action == 0:
      return   [-10.0, -10.0, -10.0, -10.0]
    # Turn right
    elif action == 1:
      return [10.0, 0.0, 0.0, 0.0]
    # Turn left
    elif action == 2:
      return [0, 10.0, 0.0, 0.0]
    # Go straight
    else:
      return [10.0, 10.0, 10.0, 10.0]
