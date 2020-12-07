#!/usr/bin/env python

from openravepy import *
import gym
import ecroEnv
import time
import pickle
import random
import click
from collections import defaultdict
from utils import select_optimal_action

# The hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

NUM_EPISODES = 100

'''
Q- learning implementation taken from:
https://github.com/satwikkansal/q-learning-taxi-v3
'''

def update(q_table, env, state):
    if random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()
    else:
        action = select_optimal_action(q_table, state, env.action_space)

    next_state, reward, _, _ = env.step(action)
    old_q_value = q_table[state][action]

    # Check if next_state has q values already
    if not q_table[next_state]:
        q_table[next_state] = {action: 0 for action in range(env.action_space.n)}

    # Maximum q_value for the actions in next state
    next_max = max(q_table[next_state].values())

    # Calculate the new q_value
    new_q_value = (1 - alpha) * old_q_value + alpha * (reward + gamma * next_max)

    # Finally, update the q_value
    q_table[state][action] = new_q_value

    return next_state, reward


def train_agent(q_table, env, num_episodes):
    for i in range(num_episodes):
        state = env.reset()
        if not q_table[state]:
            q_table[state] = {
                action: 0 for action in range(env.action_space.n)}

        epochs = 0
        num_penalties, reward, total_reward = 0, 0, 0
        while reward != 20:
            state, reward = update(q_table, env, state)
            total_reward += reward

            if reward == -10:
                num_penalties += 1

            epochs += 1
        print("\nTraining episode {}".format(i + 1))
        print("Time steps: {}, Penalties: {}, Reward: {}".format(epochs,
                                                                 num_penalties,
                                                                 total_reward))

    print("Training finished.\n")

    return q_table

@click.command()
@click.option('--num-episodes', default=NUM_EPISODES, help='Number of episodes to train on', show_default=True)
@click.option('--save-path', default="q_table.pickle", help='Path to save the Q-table dump', show_default=True)
@click.option('--render', default=2, help='Set viwer, 0 means no viwer, 1 for qtosq, 2 for qtcoin', show_default=True)
def main(num_episodes, save_path, render):

    orenv = Environment() # create openrave environment
    #env.SetViewer('qtosg') # attach viewer (optional)
    orenv.SetViewer('qtcoin') # attach viewer (optional)

    env = ecroEnv.EcroEnv(orenv=orenv)

    #obs = env.reset()
    #print(str(obs))
    #while True:
    '''
    for i in range(5):
        #action, _states = model.predict(obs)
        obs, rewards, dones, _ = env.step(0)
        #obs, reward, done, _ = env.step([10.0, 0.0, 10.0, 10.0])
        print(str(obs))
        #time.sleep(1)
    '''

    q_table = defaultdict(int, {})
    q_table = train_agent(q_table, env, num_episodes)
    # save the table for future use
    with open(save_path, "wb") as f:
        pickle.dump(dict(q_table), f)

    env.Destroy()

if __name__ == "__main__":
    main()
