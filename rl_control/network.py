# Define the neural network to be used.
from tensorflow import keras
from keras.optimizers import Adam

"""
Neural network module.

This will define the architecture used by the agent classes
"""

def create_dqn_model(lr, dense_layer_1, dense_layer_2):

# We have 9 potential actions as pairing of translation and rotation (-1,0,1)
    n_actions = 9
# positions: x,z,ry,position of crane rotation and extension,velocity of ship in x,z,ry
# x and z is ship location
    input_dims = 8

    model = keras.Sequential([
            keras.layers.Dense(dense_layer_1, activation='relu',input_dim = input_dims),
            keras.layers.Dense(dense_layer_2, activation='relu'),


            keras.layers.Dense(n_actions, activation='linear')
            ])

    model.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')

    return model
