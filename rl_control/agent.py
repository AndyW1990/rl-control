import numpy as np

class Agent():
    def __init__(self, n_actions):
        self.n_actions = n_actions
        self.epsilon = 1.0
        
    def generate_action(self, observation):
        action_1 = np.random.choice([-1,0,1])
        action_2 = np.random.choice([-1,0,1])
        
        return [action_1,action_2]
    
    