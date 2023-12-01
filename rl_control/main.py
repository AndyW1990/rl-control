from rl_control.agent import Agent
from rl_control.environment import Env
import numpy as np
from datetime import datetime

   
no_episodes = 101

Hs = 1.0
Tp_range = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0] #make global?
sim_time = 60 #make global?

lr = 0.001
gamma = 0.99
n_actions = 9 #make global?
epsilon = 1.0
batch_size = 32
input_dims = (8,) #make global?
agent = Agent(lr, gamma, n_actions, epsilon, batch_size,
                  input_dims, fname=datetime.now())

scores = []
losses = []
for i in range(no_episodes):
   
   
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
      loss = agent.learn()

   losses.append(loss)       
   scores.append(score)
   
   avg_score = np.mean(scores[-10:])
   avg_loss = np.mean(losses[-10:])
   #avg_loss = 0
   print('episode ', i, 'score %.1f' % score,
         'avg_score %.1f' % avg_score,
         'avg_loss %.1f' % avg_loss,
         'epsilon %.2f' % agent.epsilon)  
   agent.update_epsilon()
   
   if i % 10 == 0:
      #env.get_media('run_1',i)
      agent.save_model()

agent.save_model()