
from rl_control.agent import Agent
from rl_control.environment import Env
from rl_control.params import * 
import numpy as np

def predict_model(sim_time, Hs, Tp, seed, floc, episode='last'):

    n_actions = 9 #make global?
    input_dims = (8,) #make global?   
    
    agent = Agent(0.0001, 0.999, n_actions, 0.0, 1, input_dims, floc)
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
    return (average_score)
    
if __name__ == '__main__':
    model_folder = 'working_model'
    
    sim_time = 60
    Hs = 2.5
    Tp_range = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0] #make global?
    scores = []
    Tps = []
    seeds = []
    for i in range(100,1001,100):
        Tp = np.random.choice(Tp_range)
        seed = np.random.randint(0,1e6)
        score = predict_model(sim_time, Hs, Tp, seed, model_folder, episode=i)
        scores.append(score)
        Tps.append(Tp)
        seeds.append(seed)
    
    for i in range(10):
        print(f'Episode:{(i+1)*100} Hs:{Hs}m Tp:{Tps[i]}s Seed:{seeds[i]} Avg.Dist.:{round(scores[i],2)}m')  