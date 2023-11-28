import numpy as np


def generate_wave_train(Hs, Tp, seed, N=100, r_min=0.5, r_max=10,
                        sim_time=60, time_step=0.05):
    
    np.random.seed(seed)
    
    fp = 1/Tp
    
    f_min = r_min/Tp
    f_max = r_max/Tp
    f_step = (f_max - f_min)/N
    
    freqs = np.arange(f_min+f_step/2,f_max,f_step)
    spectrum = 5/16 * Hs**2 * fp**4 * freqs**-5 * np.exp(-5/4 * (fp/freqs)**4)
    wave_amps = (2 * spectrum * (freqs[0:] - np.concatenate(([0],freqs))[0:-1]))**0.5
    wave_phases = np.random.rand(N) * 2*np.pi
    
    
    #decide how to load in raos and periods
    #pass to function? nerrrr
    #load in numpy arrays? not sure
    #load in lis file? need seperate function, might be messy
    #do i have numpy arrays for all those vessels saved? this?
        #use global variable for location and name?
    
    surge_amp, surge_ph = interpolarte_raos(1/periods, surge_raw_amp, surge_raw_ph, freqs)
    heave_amp, heave_ph = interpolarte_raos(1/periods, heave_raw_amp, heave_raw_ph, freqs)
    pitch_amp, pitch_ph = interpolarte_raos(1/periods, pitch_raw_amp, pitch_raw_ph, freqs)
    
    wave_train = []
    surge = [] 
    heave = []
    pitch = []
    for t in np.arange(0,sim_time, time_step):
        if t < 15:
            ramp = t/15
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

def interpolarte_raos(in_freqs, raw_amp, raw_phase, out_freq):
    
    return amplitude, phase
    
    
    