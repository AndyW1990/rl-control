# Define the neural network to be used.
from tensorflow import keras
from keras.optimizers import Adam

"""
Neural network module.

This will define the architecture used by the agent classes
"""

def create_dqn_model(lr, neurons_layer_1, neurons_layer_2, neurons_layer_3, n_actions, input_dims):

# We have 9 potential actions as pairing of translation and rotation (-1,0,1)
    # n_actions = 9
# input_dims: vessel_x,vessel_z,vessel_ry,crane_x,crane_ry,velocity of vessel in x,z,ry
    # input_dims = 8

    model = keras.Sequential([
            keras.layers.Dense(neurons_layer_1, activation='relu'),
            keras.layers.Dense(neurons_layer_2, activation='relu'),
            #keras.layers.Dense(neurons_layer_3, activation='relu'),


            keras.layers.Dense(n_actions, activation='linear')
            ])

    model.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')

    return model
