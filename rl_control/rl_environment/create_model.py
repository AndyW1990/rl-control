# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:03:32 2023

@author: user
"""


import bpy
import numpy as np


def instantiate_model():
    '''
    functions to create blender vessel and crane objects
    returns objects for manipulation by environment
    '''
    def delete_object(name):
        # try to find the object by name
        if name in bpy.data.objects:
            # if it exists, select it and delete it
            obj = bpy.data.objects[name]
            obj.select_set(True)
            bpy.ops.object.delete(use_global=False)


    def create_animated_cube(l, b, d, x, y, z, obj_name):
        #create cube object and make animated true
        #with length, breadth, depth, location and name
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x, y, z),
            rotation=(0, 0, 0),
            scale=(l, b, d)
        )
        # rename the object
        bpy.context.object.name = obj_name
        # make rigid body
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.type = 'ACTIVE'
        bpy.context.object.rigid_body.enabled = False
        bpy.context.object.rigid_body.kinematic = True
        bpy.context.object.rigid_body.linear_damping = 0
        bpy.context.object.rigid_body.angular_damping = 0
        bpy.context.object.rigid_body.friction = 0
        # set a material to change
        bpy.ops.object.material_slot_add()
        bpy.context.object.active_material_index = 0
        bpy.ops.material.new()   
        # return the object reference
        return bpy.context.object

    def create_sphere(r, x, y, z, obj_name):
        #create sphere with radius, location and name
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r,
                                             enter_editmode=False,
                                             align='WORLD',
                                             location=(x, y, z))
        # rename the object
        bpy.context.object.name = obj_name
        # set a material to change
        bpy.ops.object.material_slot_add()
        bpy.context.object.active_material_index = 0
        bpy.ops.material.new()   
        # return the object reference
        return bpy.context.object
    
    def create_torus(r1, r2, x, y, z, obj_name):
        #create torus object with radii, location and name
        bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(x, y, z), 
        rotation=(np.pi/2, 0, 0), major_radius=r1, minor_radius=r1-r2)
        # rename the object
        bpy.context.object.name = obj_name
        # set a material to change
        bpy.ops.object.material_slot_add()
        bpy.context.object.active_material_index = 0
        bpy.ops.material.new()    
        # return the object reference
        return bpy.context.object   


    def create_empty(x, y, z, rx, ry, rz, obj_name):
        # create coord system with location, orientation and name
        rx, ry, rz = np.array([rx, ry, rz])/180*np.pi

        bpy.ops.object.empty_add(type='ARROWS',
                                         align='WORLD',
                                         location=(x, y, z),
                                         rotation=(rx, ry, rz),
                                         scale=(1, 1, 1))

        # rename the empty
        bpy.context.object.name = obj_name
        # return the empty reference
        return bpy.context.object


    def create_constraint(obj, con_type, from_name, to_name):

        bpy.ops.rigidbody.constraint_add()
        bpy.context.object.rigid_body_constraint.type = con_type
        bpy.context.object.rigid_body_constraint.object1 = bpy.data.objects[from_name]
        bpy.context.object.rigid_body_constraint.object2 = bpy.data.objects[to_name]

        return bpy.context.object
    
    def set_material(obj, name, vals):
        # Get material
        mat = bpy.data.materials.get(name)
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
        #set nodes to color
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs[0].default_value = vals
        #command requireed to make it happen
        obj.data.materials[0] = mat
        nodes["Principled BSDF"].inputs[0].keyframe_insert('default_value')


    #create body coordinate systems
    pedestal_empty = create_empty(0, 0, 6.5, 0, 0, 0, 'Pedestal Empty')
    boom_empty = create_empty(5, 0, 0, 0, 0, 0, 'Boom Empty')
    extension_empty = create_empty(5, 0, 0, 0, 0, 0, 'Extension Empty')
    payload_empty = create_empty(5, 0, 0, 0, 0, 0, 'Payload Empty')

    #create bodies
    vessel = create_animated_cube(25, 10, 3, 0, 0, 0, 'Vessel')
    pedestal = create_animated_cube(1.5, 1.5, 10, 0, 0, 0, 'Pedestal')
    boom = create_animated_cube(12, 1.5, 1.5, 0, 0, 0, 'Boom')
    extension = create_animated_cube(10, 1, 1, 0, 0, 0, 'Extension')
    payload = create_sphere(1.25, 0, 0, 0, 'Payload')
    target = create_torus(2, 1.25, 15, 0, 12.5, 'Target')

    #create constraints
    temp_vessel_empty = create_empty(0, 0, 0, 0, 0, 0, 'Vessel Driver')
    vessel_driver = create_constraint(temp_vessel_empty, 'FIXED', 'Pedestal', 'Vessel')

    temp_rot_empty = create_empty(0, 0, 6, 0, 0, 0, 'Rotation Hinge')
    rot_hinge = create_constraint(temp_rot_empty, 'HINGE', 'Boom', 'Pedestal')

    temp_ext_empty = create_empty(0, 0, 0, 0, 0, 0, 'Extension Slider')
    ext_slider = create_constraint(temp_ext_empty, 'SLIDER', 'Extension', 'Boom')


    #connect bodies to coordinate systems
    vessel.parent = vessel_driver
    pedestal.parent = pedestal_empty
    boom.parent = boom_empty
    extension.parent = extension_empty
    payload.parent = payload_empty

    #connect coordinate systems and constraints
    pedestal_empty.parent = vessel_driver
    boom_empty.parent = rot_hinge
    extension_empty.parent = ext_slider
    payload_empty.parent = extension_empty
    rot_hinge.parent = pedestal_empty
    ext_slider.parent = boom_empty
    
    #save objects to return to env for operation in episode
    vessel_obj = bpy.data.objects['Vessel Driver']
    rot_obj = bpy.data.objects['Rotation Hinge']
    ext_obj = bpy.data.objects['Extension Slider']
    payload_obj =bpy.data.objects['Payload']
    target_obj =bpy.data.objects['Target']
    scene = bpy.context.scene
    
    #set colors via materials for visuals
    set_material(vessel, 'Vessel Material', (0.80, 0.0, 0.0, 1))
    set_material(pedestal, 'Pedestal Material', (0.8, 0.5, 0.0, 1.0))
    set_material(boom, 'Boom Material', (0.8, 0.5, 0.0, 1.0))
    set_material(extension, 'Extension Material', (0.8, 0.5, 0.0, 1.0))
    set_material(payload_obj, 'Payload Material', (0.0, 0.0, 0.0, 1.0))
    set_material(target_obj, 'Target Material', (0.8, 0.8, 0.8, 1.0))

    #set background blue
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0.4, 0.8, 1)

    #create camera and light for renderings
    bpy.ops.object.camera_add()
    bpy.context.object.name = 'Camera'   
    bpy.ops.object.light_add()
    bpy.context.object.name = 'Light'    

    return vessel_obj,rot_obj,ext_obj,payload_obj,target_obj,scene
