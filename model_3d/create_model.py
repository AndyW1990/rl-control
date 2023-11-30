# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:03:32 2023

@author: user
"""


import bpy
import numpy as np


def instantiate_model():
    def delete_object(name):
        # try to find the object by name
        if name in bpy.data.objects:
            # if it exists, select it and delete it
            obj = bpy.data.objects[name]
            obj.select_set(True)
            bpy.ops.object.delete(use_global=False)


    def create_animated_cube(l, b, t, x, y, z, obj_name):
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x, y, z),
            rotation=(0, 0, 0),
            scale=(l, b, t)
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
        # return the object reference
        return bpy.context.object

    def create_sphere(r, x, y, z, obj_name):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r,
                                             enter_editmode=False,
                                             align='WORLD',
                                             location=(x, y, z))
        # rename the object
        bpy.context.object.name = obj_name
        # return the object reference
        return bpy.context.object

    def create_circle(r, x, y, z, obj_name):
        bpy.ops.mesh.primitive_circle_add(radius=r,
                                          enter_editmode=False,
                                          align='WORLD',
                                          location=(x, y, z),
                                          rotation=(np.pi/2,0,0))

        # rename the object
        bpy.context.object.name = obj_name
        # return the object reference
        return bpy.context.object

    def create_empty(x, y, z, rx, ry, rz, obj_name):

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


    def create_contraint(obj, con_type, from_name, to_name):

        bpy.ops.rigidbody.constraint_add()
        bpy.context.object.rigid_body_constraint.type = con_type
        bpy.context.object.rigid_body_constraint.object1 = bpy.data.objects[from_name]
        bpy.context.object.rigid_body_constraint.object2 = bpy.data.objects[to_name]

        return bpy.context.object

    #delete default bodies
    #delete_object('Camera')
    delete_object('Cube')
    delete_object('Light')

    #create body coordinate systems
    pedestal_empty = create_empty(0, 0, 6.5, 0, 0, 0, 'Pedestal Empty')
    boom_empty = create_empty(5, 0, 0, 0, 0, 0, 'Boom Empty')
    extension_empty = create_empty(5, 0, 0, 0, 0, 0, 'Extension Empty')
    payload_empty = create_empty(5, 0, 0, 0, 0, 0, 'Payload Empty')

    #create bodies
    vessel = create_animated_cube(25, 10, 3, 0, 0, 0, 'Vessel')
    pedestal = create_animated_cube(2, 2, 10, 0, 0, 0, 'Pedestal')
    boom = create_animated_cube(12, 2, 2, 0, 0, 0, 'Boom')
    extension = create_animated_cube(10, 2, 2, 0, 0, 0, 'Extension')
    payload = create_sphere(1.25, 0, 0, 0, 'Payload')
    target = create_circle(2, 15, 0, 12.5, 'Target')

    #create constraints
    temp_vessel_empty = create_empty(0, 0, 0, 0, 0, 0, 'Vessel Driver')
    vessel_driver = create_contraint(temp_vessel_empty, 'FIXED', 'Pedestal', 'Vessel')

    temp_rot_empty = create_empty(0, 0, 6, 0, 0, 0, 'Rotation Hinge')
    rot_hinge = create_contraint(temp_rot_empty, 'HINGE', 'Boom', 'Pedestal')

    temp_ext_empty = create_empty(0, 0, 0, 0, 0, 0, 'Extension Slider')
    ext_slider = create_contraint(temp_ext_empty, 'SLIDER', 'Extension', 'Boom')


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

    vessel_obj = bpy.data.objects['Vessel Driver']
    rot_obj = bpy.data.objects['Rotation Hinge']
    ext_obj = bpy.data.objects['Extension Slider']
    payload_obj =bpy.data.objects['Payload']
    target_obj =bpy.data.objects['Target']
    scene = bpy.context.scene


    return vessel_obj,rot_obj,ext_obj,payload_obj,target_obj,scene
