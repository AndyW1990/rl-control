import numpy as np
import pandas as pd
import os

class Env():
    None

# __init__ : Generate the 3D model with a class (Pure python code).

# Generate the wave

# Make a function to take one time step.

# Function that saves the screenshot.

# Apply an action (agent will choose action for rotation/translation to the model in the environment)

# Generate a reward

# Reset the environment for new episode


def generate_wave_train(Hs, Tp, seed, N=100, r_min=0.5, r_max=10,
                        sim_time=60, ramp_time=15, time_step=0.1):
    '''Function to generate random wave train and derive 3DoF motion for vessel
        Hs = Significant Wave Height (the average height of the highest one-third waves in a wave spectrum)
        Tp = Peak Spectral Wave Period (wave period associated with the most energetic waves in the total wave spectrum)
        seed = seed number for random phase generation
        N = number of frequency components in wave composition
        r_min/r_max = min/max  relative frequency determine the range of frequencies considered
        sim_time = simulation time
        ramp_time = ramp up dynamics at start of simulation
        time_step = discrete time step for simulation
    '''


    #convert peak period to peak frequency
    fp = 1/Tp

    #derive min and max frequency components
    f_min = r_min/Tp
    f_max = r_max/Tp
    f_step = (f_max - f_min)/N

    #generate N frequency componets and calculate the wave spectrum
    freqs = np.arange(f_min+f_step/2,f_max,f_step)
    spectrum = 5/16 * Hs**2 * fp**4 * freqs**-5 * np.exp(-5/4 * (fp/freqs)**4)

    #derive the wave amplitudes for each frequency component
    wave_amps = (2 * spectrum * (freqs[0:] - np.concatenate(([0],freqs))[0:-1]))**0.5

    #Set random seed and generate phase offsets for each component
    np.random.seed(seed)
    wave_phases = np.random.rand(N) * 2*np.pi

    #get vessel motions for our frequencies
    raos = interpolate_raos(freqs)
    surge_amp, surge_ph = raos[0], raos[1]/180*np.pi
    heave_amp, heave_ph = raos[4], raos[5]/180*np.pi
    pitch_amp, pitch_ph = raos[8], raos[9]/180*np.pi

    #loop through simulation time and superimpose the wave and motion componets
    #to create the wave train and 3DoF motions of the vessel
    wave_train = []
    surge = []
    heave = []
    pitch = []
    for t in np.arange(0,sim_time, time_step):
        if t < ramp_time:
            ramp = t/ramp_time
        else:
            ramp = 1.0

        surge_components = ramp * wave_amps * surge_amp * np.cos((surge_ph - wave_phases) - 2*np.pi*freqs*t)
        heave_components = ramp * wave_amps * heave_amp * np.cos((heave_ph - wave_phases) - 2*np.pi*freqs*t)
        pitch_components = ramp * wave_amps * pitch_amp * np.cos((pitch_ph - wave_phases) - 2*np.pi*freqs*t)

        wave_components = ramp * wave_amps * np.cos(2*np.pi*freqs*t - wave_phases)
        wave_train.append(sum(wave_components))
        surge.append(sum(surge_components))
        heave.append(sum(heave_components))
        pitch.append(sum(pitch_components))


    return wave_train, surge, heave, pitch

def interpolate_raos(target_freqs):
    ''' Function to load RAOs (Response Amplitudue Operators - how the vessel moves (amplitude) in 6DoF for each frequency and any phase lags)
        Then use the RAO frequencies to interpolate the motions for our target frequency components
    '''
    abs_path = os.path.dirname(__file__)
    rel_path = os.path.join(abs_path, '../raw_data/RAO.csv')

    #load the RAOs from csv
    df = pd.read_csv(rel_path)

    #convert period to frequency
    rao_freq = np.flip(1/df['Period'].to_numpy())

    df = df.set_index(['Period'])

    #loop through columns 6DoF amplitudes and phases and perform interpolation
    raos = []
    for col_name, col_vals in df.items():
        raos.append(np.interp(target_freqs, rao_freq, col_vals))

    return raos


if __name__ == '__main__':
    wave_train, surge, heave, pitch = generate_wave_train(2.5, 5, 1)

    plt.plot(wave_train)
