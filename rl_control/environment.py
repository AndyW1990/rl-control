import numpy as np
import pandas as pd
import os
import bpy
from rl_control.wave_gen import generate_wave_train
from model_3d.create_model import instantiate_model
from rl_control.reward import generate_reward
from rl_control.params import *

class Env():
    def __init__(self, sim_time):
        #delete any object in current scene
        self.delete_all_objs()
        #rebuilt model for 
        self.vessel,self.rot,self.ext,self.scene = instantiate_model()
        
        self.frame = 0
        
        self.sim_time = sim_time
        self.time_step = TIME_STEP
        state = self.set_initial_state()


        
        
    # Generate the wave
    def generate_wave(self, Hs, Tp, seed, N=100, r_min=0.5, r_max=10,
                        ramp_time=15, time_step=TIME_STEP):
        return generate_wave_train(Hs, Tp, seed, N=N, r_min=r_min, r_max=r_max,
                        sim_time=self.sim_time, ramp_time=ramp_time, time_step=time_step)
    
    def set_initial_state(self):
        vessel_x,_,vessel_z = self.vessel.location
        _,vessel_ry,_ = self.vessel.rotation_euler
        vessel_vx, vessel_vz = 0.0, 0.0
        vessel_vry = 0.0
        
        ext_x = self.vessel.location[0]
        
        rot_ry = self.vessel.rotation_euler[0]
        return vessel_x, vessel_z, vessel_ry, vessel_vx, vessel_vz, ext_x, rot_ry
            
    def get_new_state(self, state):
        vessel_x,_,vessel_z = self.vessel.location
        _,vessel_ry,_ = self.vessel.rotation_euler
        vessel_vx = (vessel_x - state[0])*self.time_step
        vessel_vz = (vessel_z - state[1])*self.time_step
        vessel_vry = (vessel_ry - state[3])*self.time_step
        
        ext_x = self.vessel.location[0]
        
        rot_ry = self.vessel.rotation_euler[0]
        return vessel_x, vessel_z, vessel_ry, vessel_vx, vessel_vz, ext_x, rot_ry

# Make a function to take one time step.
    def time_step(self):
        self.frame +=1
        self.scene.frame_set(self.frame)
# Function for apply actions
# Function to set the initial position
# Function to move the vessel
# Function that saves the screenshot.
# Apply an action (agent will choose action for rotation/translation to the model in the environment)
# Generate a reward (Basic Euclidean can add more)
    def reward(target_loc, payload_loc):
        generate_reward(target_loc, payload_loc)
# Reset the environment and delete the objects for new episode
    def delete_all_objs(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)