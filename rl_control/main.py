from rl_control.agent import Agent
from rl_control.environment import Env
import numpy as np

no_episodes = 5

Hs = 1.0
Tp_range = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
sim_time = 60 #make global?

n_actions = 9 #make global
agent = Agent(n_actions)

scores = []
losses = []
for i in range(no_episodes):
   
   seed = np.random.randint(0,1e6)
   Tp = np.sample(Tp_range)
   env = Env(sim_time, Hs, Tp, seed)
   
   observation = env.state
   score = 0
   done = False
   while not done:
      action = agent.generate_action(observation)
      observation_, reward, done = env.step(action)
      score += reward
      agent.store_transition(observation, action, reward, observation_, 
                                    done)
      observation = observation_
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
   
   if i % 100 == 0:
      agent.save_model()
      env.render_episode()

agent.save_model()
      
'''
Need these funcitons:
   action = agent.generate_action(observation)
   agent.store_transition(observation, action, reward, observation_, 
                                    done)
   loss = agent.learn()
   agent.update_epsilon()
   agent.save_model()
   env.render_episode()
   
Need to update this script with req inputs to classes
   agent = Agent(n_actions)
   env = Env(sim_time)
   
'''