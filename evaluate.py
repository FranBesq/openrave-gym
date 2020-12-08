from openravepy import *
import gym
import ecroEnv
import time
import pickle
import random
import click

from utils.utils import select_optimal_action

NUM_EPISODES = 100

'''
Q- learning implementation taken from:
https://github.com/satwikkansal/q-learning-taxi-v3
'''

def evaluate_agent(q_table, env, num_trials):
    total_epochs, total_penalties = 0, 0

    print("Running episodes...")
    for _ in range(num_trials):
        state = env.reset()
        epochs, num_penalties, reward = 0, 0, 0

        while reward != 20:
            next_action = select_optimal_action(q_table,
                                                state,
                                                env.action_space)
            state, reward, _, _ = env.step(next_action)

            if reward == -10:
                num_penalties += 1

            epochs += 1

        total_penalties += num_penalties
        total_epochs += epochs

    average_time = total_epochs / float(num_trials)
    average_penalties = total_penalties / float(num_trials)
    print("Evaluation results after {} trials".format(num_trials))
    print("Average time steps taken: {}".format(average_time))
    print("Average number of penalties incurred: {}".format(average_penalties))


@click.command()
@click.option('--num-episodes', default=NUM_EPISODES, help='Number of episodes to train on', show_default=True)
@click.option('--q-path', default="q_table.pickle", help='Path to load the Q-table dump', show_default=True)
@click.option('--render', default=2, help='Set viwer, 0 means no viwer, 1 for qtosq, 2 for qtcoin', show_default=True)
def main(num_episodes, q_path, render):

    orenv = Environment() # create openrave environment

    if render==1:
        env.SetViewer('qtosg') # attach viewer 
    elif render==2:
        orenv.SetViewer('qtcoin') # attach viewer     

    env = ecroEnv.EcroEnv(orenv=orenv)
    with open(q_path, 'rb') as f:
        q_table = pickle.load(f)
    evaluate_agent(q_table, env, num_episodes)


if __name__ == "__main__":
    main()
