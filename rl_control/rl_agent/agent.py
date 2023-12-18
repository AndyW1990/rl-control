from tensorflow import keras
from rl_control.rl_agent.replaybuffer import ReplayBuffer
from rl_control.rl_agent.network import create_dqn_model
import numpy as np
from keras.models import load_model
import pickle
import os

class Agent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size,
                  input_dims, model_loc, epsilon_dec=0.9, epsilon_end=0.01,
                  mem_size=10000, replace_target=1800):

        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_end
        self.batch_size = batch_size
        self.replace_target = replace_target
        self.model_file = 'rl_control_model'
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = create_dqn_model(lr, 64, 128, 64, n_actions, input_dims)
        self.q_targ = create_dqn_model(lr, 64, 128, 64, n_actions, input_dims)


        abs_path = os.path.dirname(__file__)
        self.model_dir = f'{abs_path}/../../models/{model_loc}/'
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

    #Stores the the ​state-action-reward in replay buffer object
    def store_transition(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    #Choose action, policy is epsilon greedy
    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation])
            action_vals = self.q_eval.predict(state, verbose=0)
            action = np.argmax(action_vals)
        return action

    #get action value, incremental change or no change
    # issue as this fixed action space but its set in initiation
    def get_action_values(self, action_idx):
        actions = [[-1,-1],
                    [-1,0],
                    [-1,1],
                    [0,-1],
                    [0,0],
                    [0,1],
                    [1,-1],
                    [1,0],
                    [1,1]]
        action = actions[action_idx]
        return action

    def learn(self):

        #Double Q network

        if self.memory.mem_cntr > self.batch_size:

            state, actions, rewards, state_, done = \
                                self.memory.sample_buffer(self.batch_size)

            q_next = self.q_targ.predict(state_, verbose=0)
            q_eval = self.q_eval.predict(state_, verbose=0)

            q_pred = self.q_eval.predict(state, verbose=0)

            max_actions = np.argmax(q_eval, axis=1)

            q_target = np.copy(q_pred)

            batch_index = np.arange(self.batch_size, dtype=np.int32)

            q_target[batch_index, actions] = rewards + \
                self.gamma * q_next[batch_index, max_actions.astype(int)]*done

            losses = self.q_eval.train_on_batch(state, q_target)

            if self.memory.mem_cntr % self.replace_target == 0:
                self.update_network()

            return losses

    #update epsilon value when called from outside Class
    def update_epsilon(self):
        self.epsilon = self.epsilon*self.epsilon_dec if self.epsilon > \
            self.epsilon_min else self.epsilon_min

    #update network when training or loading
    def update_network(self):
        self.q_targ.set_weights(self.q_eval.get_weights())

    #save keras model and pickle memory
    def model_save(self, episode='last'):
        self.q_eval.save(f'{self.model_dir}/episode={episode}/{self.model_file}')
        file=open(f'{self.model_dir}/episode={episode}/mem.pkl' ,"wb")
        pickle.dump(self.memory,file)

    #load model and memory from chosen episode folder. predict option skips mem pickle load
    def model_load(self, episode='last', predict=False):
        self.q_eval = load_model(f'{self.model_dir}/episode={episode}/{self.model_file}')
        if not predict:
            file=open(f'{self.model_dir}/episode={episode}/mem.pkl', "rb")
            self.memory = pickle.load(file)

        if self.epsilon <= self.epsilon_min:
             self.q_targ = load_model(f'{self.model_dir}/episode={episode}/{self.model_file}')
