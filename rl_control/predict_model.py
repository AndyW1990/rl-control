
from rl_control.agent import Agent
from rl_control.environment import Env
from rl_control.params import * 
import numpy as np

def predict_model(sim_time, Hs, Tp, seed, floc, episode='last', epsilon=0.0):

    lr = 0.0001
    gamma = 0.999
    batch_size = 1
    n_actions = 9 #make global?
    input_dims = (8,) #make global?   
    
    agent = Agent(lr, gamma, n_actions, epsilon, batch_size, input_dims, floc)
    agent.model_load(episode)

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

    env.get_media(agent.model_dir, episode)
    average_score = -score/sim_time*TIME_STEP
    print(f'Hs:{Hs}m Tp:{Tp}s Seed:{seed} Avg.Dist.:{round(average_score,2)}m')  
    return average_score
    
if __name__ == '__main__':
    model_folder = 'working_model'
    
    sim_time = 20
    Hs = 2.5
    Tp = 6.0
    seed = 18
    epsilon = 0.0
    episodes = [0, 100, 500, 1000]
    
    scores = []
    for i in episodes:
        
        # if i == 0:
        #     epsilon = 1.0
        # else:
        #     epsilon = 0.0
    
        score = predict_model(sim_time, Hs, Tp, seed, model_folder, 
                              episode=i, epsilon=epsilon)
        scores.append(score)
    
    for i,ep in enumerate(episodes):
         print(f'Episode:{ep} Hs:{Hs}m Tp:{Tp}s Seed:{seed} Avg.Dist.:{round(scores[i],2)}m')  