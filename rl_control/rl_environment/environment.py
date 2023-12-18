import numpy as np
import bpy
from rl_control.rl_environment.wave_gen import generate_wave_train
from rl_control.rl_environment.create_model import instantiate_model
from rl_control.rl_environment.reward import generate_euclidean_reward
from rl_control.rl_environment.render_create_video import render_images,generate_video
from rl_control.params import *


class Env():
    '''
    Class to create Blender model and handle animating the environmen
    through each step in the episode.
    Typical RL setup in  that you can
    '''
    def __init__(self, sim_time, Hs, Tp, seed, ramp_time=10, 
                 ext=None, rot=None):

        #delete any objects in current scene
        self.delete_all_objs()

        #rebuilt model for
        self.vessel,self.rot,self.ext,self.payload,self.target,self.scene = instantiate_model()
        self.scene.frame_end = int(sim_time/TIME_STEP)
        self.Hs = Hs
        self.Tp = Tp
        self.seed = seed
        self.frame = 0
        self.sim_time = sim_time
        self.time_step = TIME_STEP
        self.wave, self.surge, self.heave, self.pitch = self.generate_wave(ramp_time)
        self.state = self.set_initial_state(ext, rot)
        self.done = False

    # Generate wave with function
    def generate_wave(self, ramp_time):
        return generate_wave_train(self.Hs, self.Tp, self.seed, 
                    sim_time=self.sim_time, ramp_time=ramp_time)

    # Set initial position
    def set_initial_state(self, ext, rot):
        vessel_x,_,vessel_z = self.vessel.location
        _,vessel_ry,_ = self.vessel.rotation_euler
        vessel_vx, vessel_vz = 0.0, 0.0
        vessel_vry = 0.0
        
        if ext:
            ext_x = ext
        else:
            ext_x = (np.random.random()-0.5)*5
            
        if rot:
            rot_ry = rot*np.pi/180
        else:
            rot_ry = (np.random.random()-0.5)*np.pi/4
         
        self.ext.location[0] = ext_x
        self.rot.rotation_euler[1] = rot_ry

        return vessel_x, vessel_z, vessel_ry, vessel_vx, vessel_vz, vessel_vry, ext_x, rot_ry
    
    # Get positions and velocitys of vessel and crane for state indo
    def get_new_state(self):
        vessel_x,_,vessel_z = self.vessel.location
        _,vessel_ry,_ = self.vessel.rotation_euler
        vessel_vx = (vessel_x - self.state[0])*self.time_step
        vessel_vz = (vessel_z - self.state[1])*self.time_step
        vessel_vry = (vessel_ry - self.state[2])*self.time_step

        ext_x = self.ext.location[0]

        rot_ry = self.rot.rotation_euler[1]

        return vessel_x, vessel_z, vessel_ry, vessel_vx, vessel_vz, vessel_vry, ext_x, rot_ry

    # Take one step in envorinment  
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

    # Set next vessel position from generated wave motions
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

    #  Set new crane position with chosen action
    def move_crane(self,action):

        # get and adjust extension
        x = self.state[-2]
        
        x += action[0]*TRANSLATE_INC
        y = 0
        z = 0

        self.ext.location = (x,y,z)
        self.ext.keyframe_insert(data_path="location",index=-1)

        # get and adjust rotation
        ry = self.state[-1]

        rx = np.radians(90)
        ry += np.radians(action[1]*ROTATE_INC)
        rz = 0

        self.rot.rotation_mode = "XYZ"
        self.rot.rotation_euler  = (rx,ry,rz)
        self.rot.keyframe_insert(data_path="rotation_euler")

    # get reward with location of payload and target
    def get_reward(self):
        payload_loc = self.payload.matrix_world.translation
        target_loc = self.target.matrix_world.translation
        reward = generate_euclidean_reward(target_loc, payload_loc)
        return reward

    # Update done parameter when episode over
    def get_done(self):
        if self.frame == (self.sim_time/self.time_step) - 1:
            self.done = True

    # Render photo frames and video
    def get_media(self, render_loc, episode='last'):
        abs_path = os.path.dirname(__file__)
        render_dir = f'{abs_path}/../../renderings/{render_loc}/'
        if not os.path.exists(render_dir):
            os.makedirs(render_dir)
        
        render_images(render_dir, episode)
        generate_video(render_dir, episode, f'Sim_Vid_ep={episode}')

    # Reset the environment and delete the objects for new episode
    def delete_all_objs(self):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)

    # Change color of target based payload accuracy (visual feedback)
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
