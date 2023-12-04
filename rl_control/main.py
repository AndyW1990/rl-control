from rl_control.agent import Agent
from rl_control.environment import Env
import numpy as np
from datetime import datetime

 
run_name = 'cloud_run_andy'

no_episodes = 10000

Hs_range = [2.0]
Tp_range = [5.0, 6.0, 7.0, 8.0, 9.0] #make global?
sim_time = 60 #make global?



lr = 0.001
epsilon_decay = 0.999

gamma = 0.99
n_actions = 9 #make global?
epsilon = 1.0
batch_size = 128
input_dims = (8,) #make global?
agent = Agent(lr, gamma, n_actions, epsilon, batch_size,
                  input_dims, epsilon_dec=epsilon_decay, 
                  fname=f'run_method_{run_name}')
#agent.load_model()

scores = []
losses = []
for i in range(no_episodes):
      
   Hs = np.random.choice(Hs_range)
   Tp = np.random.choice(Tp_range)
   seed = np.random.randint(0,1e6)
   
   
   env = Env(sim_time, Hs, Tp, seed)
   
   observation = env.state
   score = 0
   done = False
   while not done:
      action = agent.choose_action(observation)
      action_value = agent.get_action_values(action)
      observation_, reward, done = env.step(action_value)
      score += reward
      agent.store_transition(observation, action, reward, observation_, done)
      observation = observation_
      if env.frame % 10 == 0 or done:
         loss = agent.learn()

   losses.append(loss)       
   scores.append(score)
   
   avg_score = np.mean(scores[-100:])
   avg_loss = np.mean(losses[-100:])
   print('episode ', i, 'score %.1f' % score,
         'avg_score %.1f' % avg_score,
         'avg_loss %.1f' % avg_loss,
         'epsilon %.2f' % agent.epsilon)  
   if i > 1000:
      agent.update_epsilon()
   
   if i % 100 == 0:
      #env.get_media('random_init',i)
      agent.save_model()
      
   # if avg_score < np.mean(scores[-200:100]):
   #    env.get_media('simple_run',i)
   #    agent.save_model()
   #    break

agent.save_model()