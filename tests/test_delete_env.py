from rl_control.environment import Env
import bpy

env = Env()

env.delete_all_objs()

result = bpy.ops.object.select_all(action='SELECT')

if result == {'PASS_THROUGH'}:
    print('All objects have been successfully deleted.')
else:
    print('Unsuccessful in deleting the environment objects.')
