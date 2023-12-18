from rl_control.rl_agent.agent import Agent
from rl_control.rl_environment.environment import Env
from rl_control.params import *
import numpy as np

def predict_model(sim_time, ramp_time, Hs, Tp, seed,
                  folder_name, episode='last', epsilon=0.0,
                  save_media=False):
    '''
    function to run single episode for demo or testing
    inputs:
    sim_time = simulation time in [s]
    ramp_time = build up dynamics from start time in [s]
    Hs = significant wave height
    Tp = peak wave period
    seed = number for random wave generation
    folder_name = name of directory to save models in model directory
                  and renderings in renderings directory
    episode = further directory of saved model
    epsilon = RL param to set % of time to choose random actions
    '''
    
    #RL params, not relevent for test/predict but required to instantiate agent
    lr = 0.0001
    gamma = 0.999
    batch_size = 1
    n_actions = 9
    input_dims = (8,)

    #instantiate agent and load saved model
    agent = Agent(lr, gamma, n_actions, epsilon,
                  batch_size, input_dims, folder_name)
    agent.model_load(episode, predict=True)

    # instantiate environment for episode
    env = Env(sim_time, Hs, Tp, seed,
              ramp_time=ramp_time, rot=0, ext=-2.5)
    
    ob_reward = []
    observation = env.state
    score = 0
    done = False
    while not done:
        action = agent.choose_action(observation)
        action_value = agent.get_action_values(action)
        observation_, reward, done = env.step(action_value)
        score += reward
        observation = observation_
        
        if reward < -0.5:
            ob_reward.append(reward)
        print(f'frame:{env.frame} reward:{reward}')
        
      #  if env.frame % 100 == 0:
      #      print(f'frame:{env.frame} score:{score}')
    
    #save rendering and calc average distance from target
    if save_media:
        env.get_media(folder_name, episode)
    average_score = -score/sim_time*TIME_STEP
    print(f'Hs:{Hs}m Tp:{Tp}s Seed:{seed} Avg.Dist.:{round(average_score,2)}m')
    print(f'time < 0.5m :{len(ob_reward)*TIME_STEP}')
    return average_score

if __name__ == '__main__':
    
    # params and loop to save renderings of training evolution for demo
    model_folder = 'working_model'

    sim_time = 1000
    ramp_time = 30
    Hs = 2.5
    Tp = 6.0
    seed = 20
    epsilon_decay = 0.995
    episodes = [600]

    scores = []
    for i in episodes:
        if i > 500:
            epsilon = 0.0
        else:
            epsilon = epsilon_decay**i
        score = predict_model(sim_time, ramp_time, Hs, Tp, seed,
                              model_folder, episode=i, epsilon=epsilon)
        scores.append(score)
    
    #print final scores in terminal as renderings are verbose
    for i,ep in enumerate(episodes):
         print(f'Episode:{ep} Hs:{Hs}m Tp:{Tp}s Seed:{seed} Avg.Dist.:{round(scores[i],2)}m')
         