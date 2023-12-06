from rl_control.rl_agent.agent import Agent
from rl_control.rl_environment.environment import Env
from rl_control.params import * 
import numpy as np

def predict_model(sim_time, ramp_time, Hs, Tp, seed, 
                  floc, episode='last', epsilon=0.0):

    lr = 0.0001
    gamma = 0.999
    batch_size = 1
    n_actions = 9 #make global?
    input_dims = (8,) #make global?   
    
    agent = Agent(lr, gamma, n_actions, epsilon, 
                  batch_size, input_dims, floc)
    agent.model_load(episode, predict=True)

    env = Env(sim_time, Hs, Tp, seed, 
              ramp_time=ramp_time, rand_start=False)

    observation = env.state
    score = 0
    done = False
    while not done:
        action = agent.choose_action(observation)
        action_value = agent.get_action_values(action)
        observation_, reward, done = env.step(action_value)
        score += reward
        observation = observation_

    #env.get_media(agent.model_dir, episode)
    average_score = -score/sim_time*TIME_STEP
    print(f'Hs:{Hs}m Tp:{Tp}s Seed:{seed} Avg.Dist.:{round(average_score,2)}m')  
    return average_score
    
if __name__ == '__main__':
    model_folder = 'working_model'
    
    sim_time = 20
    ramp_time = 2
    Hs_range = [1.5, 2.5, 3.5]
    Tp_range = [5.0, 7.5, 10.0]
    seed = 19
    epsilon = 0
    episode = 1300
    
    scores = []
    for Hs in Hs_range:
        for Tp in Tp_range:
            score = predict_model(sim_time, ramp_time, Hs, Tp, seed, 
                                model_folder, episode=episode, epsilon=epsilon)
            scores.append(score)
    
    i = 0
    for Hs in Hs_range:
        for Tp in Tp_range:
            print(f'Hs:{Hs}m Tp:{Tp}s Seed:{seed} Avg.Dist.:{round(scores[i],2)}m') 
            i += 1 