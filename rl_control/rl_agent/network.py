# Define the neural network to be used.
from tensorflow import keras
from keras.optimizers import Adam

def create_dqn_model(lr, neurons_layer_1, neurons_layer_2, neurons_layer_3, n_actions, input_dims):
    """
    Neural network module.

    This defines the architecture used by the agent class for both
    target and evaluation
    """
    model = keras.Sequential([
            keras.layers.Dense(neurons_layer_1, activation='relu'),
            keras.layers.Dense(neurons_layer_2, activation='relu'),
            keras.layers.Dense(neurons_layer_3, activation='relu'),


            keras.layers.Dense(n_actions, activation='linear')
            ])

    model.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')

    return model
