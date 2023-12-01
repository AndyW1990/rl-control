from model_3d.create_model import instantiate_model
from tensorflow import keras
from replaybuffer import ReplayBuffer
from network import create_dqn_model
import numpy as np
from keras.models import load_model

class Agent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size,
                  input_dims, epsilon_dec=0.9, epsilon_end=0.01,
                  mem_size=10000, replace_target=100, fname='rl_control_model.h5'):

    #Dont train both networks
    #Only train the target network that you use to choose actions,
    #replace the weights of the target network every 100 episodes.

        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_end
        self.batch_size = batch_size
        self.replace_target = replace_target
        self.model_file = f'models/{fname}'
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = create_dqn_model(lr, 64, 128, 64, n_actions, input_dims)
        self.q_targ = create_dqn_model(lr, 64, 128, 64, n_actions, input_dims)

    #Stores the the ​state-action-reward
    def store_transition(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    #Choose an action, i.e. a policy, chooses an action based on its current state
    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation])
            action_vals = self.q_eval.predict(state, verbose=0)
            action = np.argmax(action_vals)
        return action
    
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

        #When do we perform learning? Once the max_size is reach and memory is full?
        #If the number of memories saved is less than the batch size you will end up
        #sampling a single memory batch size times (single memory 64 times), you will
        #end up sampling the same batch 64 times - not good for training.

        #Double Q = q-value of a q-value

        if self.memory.mem_cntr > self.batch_size:

            state, actions, rewards, state_, done = \
                                self.memory.sample_buffer(self.batch_size)

            #action_values = np.array(self.action_space, dtype=np.int8)
            #action_indices = np.dot(actions, action_values)

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

    def update_epsilon(self):
        self.epsilon = self.epsilon*self.epsilon_dec if self.epsilon > \
            self.epsilon_min else self.epsilon_min

    def update_network(self):
            self.q_targ.set_weights(self.q_eval.get_weights())


    def save_model(self):
        self.q_eval.save(self.model_file)

    def load_model(self):
        self.q_eval = load_model(self.model_file)

        if self.epsilon <= self.epsilon_min:
            self.update_network()

