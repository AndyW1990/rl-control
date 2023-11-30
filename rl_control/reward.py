
def generate_euclidean_reward(target_loc, payload_loc):

    x = payload_loc[0] - target_loc[0]
    y = payload_loc[1] - target_loc[1]
    z = payload_loc[2] - target_loc[2]

    euclidean_dist = (x**2 + y**2 + z**2)**0.5

    reward = -euclidean_dist

    return reward
