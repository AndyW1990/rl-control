import numpy as np


def generate_wave_train(Hs, Tp, no_freq, seed):
    
    if Tp/np.sqrt(Hs) <= 3.6: gamma = 5
    elif Tp/np.sqrt(Hs) >= 5: gamma = 1
    else: gamma = np.exp(5.75-1.15*Tp/np.sqrt(Hs))
    
    
    
    start_freq = 0.05 #needs to be funciton of tp
    end_freq = 1. #needs to be funciton of tp
    
    frequencies = np.linspace(start_freq,end_freq,no_freq) #maybe log space?
    amplitudes = 
    
    wave_train = 
    
    return wave_train

def generate_motions(wave_train, rao):
    
    return motion
    
    
    