from rl_control.agent import Agent
from rl_control.environment import Env
import numpy as np
from datetime import datetime

 
my_name = 'andy'

assert my_name != 'andy'
no_episodes = 10000

Hs_range = [1.0, 1.5, 2.0, 2.5]
Tp_range = [8.0] #make global?
sim_time = 60 #make global?


if my_name == 'andy':
   Hs_space = np.concatenate((np.linspace(Hs_range[0],Hs_range[-1],1000),
                        np.ones(no_episodes-1000)*Hs_range[-1]))
   lr = 0.001
   epsilon_decay = 0.98
elif my_name == 'tom':
   #Hs = np.random.choice(Hs_range)
   lr = 0.0005
   epsilon_decay = 0.99
elif my_name == 'ben':
   Hs = Hs_range[-1]
   lr = 0.0001
   epsilon_decay = 0.998
elif my_name == 'jules':
   #Hs = np.random.choice(Hs_range)
   lr = 0.0001
   epsilon_decay = 0.998   
elif my_name == 'julien':
   Hs = Hs_range[-1]
   lr = 0.0005
   epsilon_decay = 0.999

gamma = 0.99
n_actions = 9 #make global?
epsilon = 1.0
batch_size = 64
input_dims = (8,) #make global?
agent = Agent(lr, gamma, n_actions, epsilon, batch_size,
                  input_dims, epsilon_dec=epsilon_decay, 
                  fname=f'run_method_{my_name}')

scores = []
losses = []
for i in range(no_episodes):
   
   if my_name == 'andy':
      Hs = Hs_space[i]
   elif my_name in ['tom', 'jules']:
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
      #if env.frame % 10 == 0 or done:
      loss = agent.learn()

   losses.append(loss)       
   scores.append(score)
   
   avg_score = np.mean(scores[-100:])
   avg_loss = np.mean(losses[-100:])
   print('episode ', i, 'score %.1f' % score,
         'avg_score %.1f' % avg_score,
         'avg_loss %.1f' % avg_loss,
         'epsilon %.2f' % agent.epsilon)  
   agent.update_epsilon()
   
   if i % 250 == 0:
      env.get_media('simple_run',i)
      agent.save_model()
      
   if avg_score < np.mean(scores[-200:100]):
      env.get_media('simple_run',i)
      agent.save_model()
      break

agent.save_model()