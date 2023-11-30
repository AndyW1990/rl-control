from model_3d.create_model import instantiate_model
from rl_control.wave_gen import generate_wave_train
from model_3d.render_create_video import render_images
from model_3d.render_create_video import generate_video
import bpy
import numpy as np


### NOTE: The matrix world return is 1 timestep ahead of the location etc as input

Hs = 1.0
Tp = 5.0
seed = 1
sim_time = 60
time_step = 0.1

instantiate_model()

wave, surge, heave, pitch = generate_wave_train(Hs, Tp, seed, sim_time=sim_time, time_step=time_step)

vessel = bpy.data.objects['Vessel Driver']
rot = bpy.data.objects['Rotation Hinge']
ext = bpy.data.objects['Extension Slider']

surge_mw = []
heave_mw = []

no_frames = int(sim_time/time_step)
bpy.context.scene.frame_end = no_frames

for i in range(no_frames):
    
    bpy.context.scene.frame_set(i)

    x = surge[i]
    y = 0 
    z = heave[i]
    rx = 0
    ry = np.radians(pitch[i])
    rz = 0
    vessel.location = (x,y,z)
    vessel.rotation_mode = "XYZ"
    vessel.rotation_euler = (rx,ry,rz)
    vessel.keyframe_insert(data_path="location",index=-1)
    vessel.keyframe_insert(data_path="rotation_euler")

    rx = np.radians(90)
    ry = np.radians(10*np.sin(np.radians(i*5+2))) 
    rz = 0
    rot.rotation_mode = "XYZ"
    rot.rotation_euler  = (rx,ry,rz) 
    rot.keyframe_insert(data_path="rotation_euler")

    x = 4.5 + 1.5*np.sin(np.radians(i*4+1.5))
    y = 0 
    z = 0
    ext.location = (x,y,z)
    ext.keyframe_insert(data_path="location",index=-1)
    
    
    if i % 10 == 0:
        print(bpy.data.objects['Payload'].matrix_world.translation) 
    
    surge_mw.append(bpy.data.objects['Vessel'].matrix_world.translation[0])
    heave_mw.append(bpy.data.objects['Vessel'].matrix_world.translation[2])
        
print('--------------max surge-----------------')
print('location inp: ',np.argmax(np.array(surge)), np.max(np.array(surge)))
print('matrix world: ',np.argmax(np.array(surge_mw)), np.max(np.array(surge_mw)))
print('--------------max heave-----------------')
print('location inp: ',np.argmax(np.array(heave)), np.max(np.array(heave)))
print('matrix world: ',np.argmax(np.array(heave_mw)), np.max(np.array(heave_mw)))


