
from rl_control.agent import Agent
from rl_control.environment import Env
from rl_control.params import * 


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
        
        
    env.get_media(agent.model_dir,'predict')
    average_score = -score/sim_time*TIME_STEP
    print(f'Hs:{Hs}m Tp:{Tp}s Seed:{seed} Score:{round(average_score,2)}m')  


if __name__ == '__main__':
    predict_model(60, 3.0, 7.5, 19, 'test_run_andy_v5', episode=600)