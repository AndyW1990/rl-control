
import bpy

def generate_reward(target_loc, payload_loc):
    
    x = payload_loc[0] - target_loc[0]
    y = payload_loc[1] - target_loc[1]
    z = payload_loc[2] - target_loc[2]
    
    euclidian_dist = (x**2 + y**2 + z**2)**0.5
    
    reward = -euclidian_dist
    
    return reward
    