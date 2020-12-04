import gym
import numpy as np
from gym import spaces
from openravepy import *

#Dimensions of input image
HEIGHT = 416
WIDTH = 416
#Patch size
ACTION_H = 52
ACTION_W = 96

class EcroEnv(gym.Env):
  """Custom Environment to control Ecron robot in openrave using gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self, orenv=None, normActions=True):

    self.orenv = orenv #Openrave env
    self.normActionSpace = True
    if normActions == False:
      self.normActions = False
    else:
      self.normActions = True

    super(AttackEnv, self).__init__()
    # Define action and observation space
    # Action space is velocity of each weel 
    if self.normActionSpace is True:
        self.action_space = spaces.Box(low=0, high=1, shape=
                    (4,), dtype=np.float32)
    else:
      self.action_space = spaces.Box(low=0, high=10, shape=
                    (4,), dtype=np.uint8)
    # ObsSpace shape pending:
    self.observation_space = spaces.Box(low=0, high=255, shape=
                    (HEIGHT, WIDTH, 3), dtype=np.uint8)

  def step(self, action):
        #Quizas hay que formatear la accion de otra forma
        velocities = [i*10 for i in action]
        self.control.SetDesired(action)
        time.sleep(0.5)#Let robot in that direction for sleep time

        H_0_robot = self.robot.GetTransform()
        print("Shape of H: " + str(H_0_robot.shape()))
        print(H_0_robot)
    ...
  def reset(self):
    # Reset the state of the environment to initial position
    self.orenv.Load('/home/francisco/Documents/Robot_Sim/openrave-gym/map.env.xml') # load a simple scene
    self.robot = self.orenv.GetRobots()[0] # get the first robot
    print("Using robot: ", robot.GetName())
    self.robot.SetController(RaveCreateController(self.orenv,'idealvelocitycontroller'),range(robot.GetDOF()),0)
    self.control = control = robot.GetController()

    self.orenv.StartSimulation(timestep=0.001)

    return self._get_obs() # a falta de definir una observacion
    
    ...
  def render(self, mode='human', close=False):
    # Render the environment to the screen
    ...

  def _get_obs(self):
    return self.robot.GetTransform()