import numpy as np
import bpy
from rl_control.rl_environment.wave_gen import generate_wave_train
from rl_control.rl_environment.create_model import instantiate_model
from rl_control.rl_environment.reward import generate_euclidean_reward
from rl_control.rl_environment.render_create_video import render_images,generate_video
from rl_control.params import *


class Env():
    def __init__(self, sim_time, Hs, Tp, seed, ramp_time=10, rand_start=True):

        #delete any object in current scene
        self.delete_all_objs()

        #rebuilt model for
        self.vessel,self.rot,self.ext,self.payload,self.target,self.scene = instantiate_model()
        self.scene.frame_end = int(sim_time/TIME_STEP)
        self.Hs = Hs
        self.Tp = Tp
        self.seed = seed
        self.frame = 0
        self.wave, self.surge, self.heave, self.pitch = self.generate_wave(ramp_time)
        self.sim_time = sim_time
        self.time_step = TIME_STEP
        self.state = self.set_initial_state(rand_start)
        self.done = False

    # Generate the wave
    def generate_wave(self, ramp_time):
        return generate_wave_train(self.Hs, self.Tp, self.seed, ramp_time=ramp_time)

    # Set initial zero position
    def set_initial_state(self, rand_start=True):
        vessel_x,_,vessel_z = self.vessel.location
        _,vessel_ry,_ = self.vessel.rotation_euler
        vessel_vx, vessel_vz = 0.0, 0.0
        vessel_vry = 0.0
        if rand_start:
            ext_x = (np.random.random()-0.5)*5
            rot_ry = (np.random.random()-0.5)*np.pi/4
        else:
            ext_x = -2.5
            rot_ry = 22.5*np.pi/180

        self.ext.location[0] = ext_x
        self.rot.rotation_euler[1] = rot_ry

        return vessel_x, vessel_z, vessel_ry, vessel_vx, vessel_vz, vessel_vry, ext_x, rot_ry
    # Get the position after a set time step
    def get_new_state(self):
        vessel_x,_,vessel_z = self.vessel.location
        _,vessel_ry,_ = self.vessel.rotation_euler
        vessel_vx = (vessel_x - self.state[0])*self.time_step
        vessel_vz = (vessel_z - self.state[1])*self.time_step
        vessel_vry = (vessel_ry - self.state[2])*self.time_step

        ext_x = self.ext.location[0]

        rot_ry = self.rot.rotation_euler[1]

        return vessel_x, vessel_z, vessel_ry, vessel_vx, vessel_vz, vessel_vry, ext_x, rot_ry

# Function to change vessel,crane,reward based on this time step and confirmation with get_done()
    def step(self, action):
        self.frame +=1
        self.scene.frame_set(self.frame)
        self.move_vessel()
        self.move_crane(action)
        self.state =  self.get_new_state()
        self.reward = self.get_reward()
        self.update_target()
        self.get_done()

        return self.state,self.reward,self.done

# Function to move the vessel based on the new frame
    def move_vessel(self):

        x = self.surge[self.frame]
        y = 0
        z = self.heave[self.frame]

        rx = 0
        ry = np.radians(self.pitch[self.frame])
        rz = 0

        self.vessel.location = (x,y,z)
        self.vessel.rotation_mode = "XYZ"
        self.vessel.rotation_euler = (rx,ry,rz)
        self.vessel.keyframe_insert(data_path="location",index=-1)
        self.vessel.keyframe_insert(data_path="rotation_euler")

#  Function to move the vessel based on the new frame
    def move_crane(self,action):

        # Set crane extension
        x = self.state[-2]

        x += action[0]*TRANSLATE_INC
        y = 0
        z = 0

        self.ext.location = (x,y,z)
        self.ext.keyframe_insert(data_path="location",index=-1)

        # Set crane rotation
        ry = self.state[-1]

        rx = np.radians(90)
        ry += np.radians(action[1]*ROTATE_INC)
        rz = 0

        self.rot.rotation_mode = "XYZ"
        self.rot.rotation_euler  = (rx,ry,rz)
        self.rot.keyframe_insert(data_path="rotation_euler")

# Generate a reward (Basic Euclidean can add more)
    def get_reward(self):
        payload_loc = self.payload.matrix_world.translation
        target_loc = self.target.matrix_world.translation
        reward = generate_euclidean_reward(target_loc, payload_loc)
        return reward

# Check if the cycle is over
    def get_done(self):
        if self.frame == (self.sim_time/self.time_step) - 1:
            self.done = True

# Generate the rendered picture and video
    def get_media(self, model_dir, episode='last'):
        render_images(model_dir, episode)
        generate_video(model_dir, episode, f'Sim_Vid_ep={episode}')

# Reset the environment and delete the objects for new episode
    def delete_all_objs(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)

    def update_target(self):
        m = bpy.data.materials.get('Target Material')
        nodes = m.node_tree.nodes
        if -self.reward <= 0.5:
            nodes["Principled BSDF"].inputs[0].default_value = (0.0, 0.80, 0.0, 1)
        elif -self.reward > 0.5 and -self.reward <= 2.0:
            nodes["Principled BSDF"].inputs[0].default_value = (0.80, 0.15, 0.0, 1)
        elif -self.reward > 2.0:
            nodes["Principled BSDF"].inputs[0].default_value = (0.80, 0.0, 0.0, 1)
        else:
            nodes["Principled BSDF"].inputs[0].default_value = (0.80, 0.80, 0.80, 1)

        self.target.data.materials[0] = m
        nodes["Principled BSDF"].inputs[0].keyframe_insert('default_value')

if __name__ == '__main__':
    Hs = 2.5
    Tp = 8
    seed = 34
    action = [-1,1]
    sim_time = 60
    env = Env(sim_time,Hs,Tp,seed)
