#!/usr/bin/env python

from openravepy import *
import time

env = Environment() # create openrave environment
#env.SetViewer('qtosg') # attach viewer (optional)
env.SetViewer('qtcoin') # attach viewer (optional)

try:
    env.Load('/home/francisco/Documents/Robot_Sim/openrave-gym/map.env.xml') # load a simple scene
    robot = env.GetRobots()[0] # get the first robot
    print("Using robot: ", robot.GetName())
    robot.SetController(RaveCreateController(env,'idealvelocitycontroller'),range(robot.GetDOF()),0)
    control = robot.GetController()

    env.StartSimulation(timestep=0.001)

    for i in range(20):
        velocities = [10.0, 10.0, 10.0, 10.0]
        control.SetDesired(velocities)

        time.sleep(0.5)

        H_0_robot = robot.GetTransform()
        print("Shape of H: " + str(H_0_robot.shape()))
        print(H_0_robot)

    time.sleep(1)

finally:
    env.Destroy()
