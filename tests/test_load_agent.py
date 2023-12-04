

from rl_control.agent import Agent
from rl_control.environment import Env

import numpy as np


run_name = 'test_run_andy_v4'

sim_time = 60 #make global?
lr = 0.001


gamma = 0.99
n_actions = 9 #make global?
epsilon = 0.0
batch_size = 128
input_dims = (8,) #make global?   
   
agent = Agent(lr, gamma, n_actions, epsilon, batch_size,
                    input_dims, run_name)
agent.load_model()

seed = np.random.randint(0,10)

Hs = 1.5
Tp = 7.5

env = Env(sim_time, Hs, Tp, seed)

observation = env.state
score = 0
done = False
while not done:
    action = agent.choose_action(observation)
    action_value = agent.get_action_values(action)
    observation_, reward, done = env.step(action_value)
    score += reward
    observation = observation_


print('episode ', 1001, 'score %.1f' % score)  
env.get_media(run_name,1001)
