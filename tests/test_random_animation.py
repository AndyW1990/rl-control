
import bpy
import numpy as np
from model_3d.create_model import instantiate_model

instantiate_model()


vessel = bpy.data.objects['Vessel Driver']
rot = bpy.data.objects['Rotation Hinge']
ext = bpy.data.objects['Extension Slider']


for i in range(0,250):
    
    bpy.context.scene.frame_set(i)
    
    x = np.sin(np.radians(i*1))
    y = 0 
    z = np.sin(np.radians(i*3))
    rx = 0
    ry = np.radians(5*np.sin(np.radians(i*2)))
    rz = 0
    vessel.location = (x,y,z)
    print(vessel.location)
    vessel.rotation_euler  = (rx,ry,rz)
    print(vessel.rotation_euler)
    vessel.keyframe_insert(data_path="location",index=-1)
    vessel.keyframe_insert(data_path="rotation_euler")

    rx = np.radians(90)
    ry = np.radians(20*np.sin(np.radians(i*5+2))) 
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
    