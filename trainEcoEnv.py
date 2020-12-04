#!/usr/bin/env python

from openravepy import *
import gym
import ecroEnv
import time

if __name__ == '__main__':

    orenv = Environment() # create openrave environment
    #env.SetViewer('qtosg') # attach viewer (optional)
    orenv.SetViewer('qtcoin') # attach viewer (optional)

    env.ecroEnv(orenv=orenv)

    obs = env.reset()
    #while True:
    for i in range(5):
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        print(str(obs.shape))
        time.sleep(1)

    env.Destroy()
