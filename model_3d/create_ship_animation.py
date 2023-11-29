
import bpy
import numpy as np

def animate_ship():
    def delete_object(name):
        # try to find the object by name
        if name in bpy.data.objects:
            # if it exists, select it and delete it
            obj = bpy.data.objects[name]
            obj.select_set(True)
            bpy.ops.object.delete(use_global=False)


    def create_dyn_cube(l, b, t, x, y, z, obj_name):
        obj = bpy.ops.mesh.primitive_cube_add(
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
        bpy.context.object.rigid_body.enabled = True
        bpy.context.object.rigid_body.kinematic = False
        bpy.context.object.rigid_body.linear_damping = 0
        bpy.context.object.rigid_body.angular_damping = 0
        bpy.context.object.rigid_body.friction = 0
        # return the object reference
        return bpy.context.object

    def create_vessel(l, b, t, x, y, z, obj_name):
        #make dynamic body
        vessel = create_dyn_cube(l, b, t, x, y, z, obj_name)

        vessel.rigid_body.type = 'ACTIVE'
        vessel.rigid_body.enabled = False
        vessel.rigid_body.kinematic = True
        return vessel


    delete_object('Vessel')

    vessel = create_vessel(10, 5, 1, 0, 0, 0, 'Vessel')

