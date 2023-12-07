from rl_control.rl_agent.agent import Agent
from rl_control.rl_environment.environment import Env
import numpy as np

def run_batch(folder_name):


   no_episodes = 501

   Hs_range = [2.5]
   Tp_range = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0] #make global?
   sim_time = 60 #make global?

   lr = 0.001
   epsilon_decay = 0.995

   gamma = 0.99
   n_actions = 9 #make global?
   epsilon = 1.0
   batch_size = 128
   input_dims = (8,) #make global?
   agent = Agent(lr, gamma, n_actions, epsilon, batch_size,
                     input_dims, folder_name, epsilon_dec=epsilon_decay)
   #agent.model_load()

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

      #if i > 500:
      agent.update_epsilon()

      losses.append(loss)
      scores.append(score)
      avg_score = np.mean(scores[-100:])
      avg_loss = np.mean(losses[-100:])

      if i % 25 == 0:
         agent.model_save()

      if i % 25 == 0:
         agent.model_save(episode=i)
         #env.get_media(folder_name,episode=i)


      print('episode ', i, 'score %.1f' % score,
            'avg_score %.1f' % avg_score,
            'avg_loss %.1f' % avg_loss,
            'epsilon %.2f' % agent.epsilon)

   agent.model_save()
   #env.get_media(folder_name)

if __name__ == '__main__':
   run_batch('test_new_dir_tree')
