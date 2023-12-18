from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from rl_control.rl_environment.environment import Env
from rl_control.rl_agent.agent import Agent
from rl_control.predict_model import predict_model
from rl_control.params import *

import bpy
import os

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

### Path variables

api_path = os.path.dirname(__file__)
api_to_model = f"../../"
path_to_models = os.path.join(api_path, api_to_model)

MODEL_FOLDER = "working_model"

###
# Model hyper parameters

sim_time = 20 # seconds
ramp_time = 2
episode = 600

## Instanciate Agent
agent = Agent(
    lr=0.0001,
    gamma=0.999,
    n_actions=9,
    epsilon=0,
    batch_size=128,
    input_dims=(8,),
    model_loc=MODEL_FOLDER)

agent.model_load(episode, predict=True)

### Environment hard coded params for posterity
Hs = 2.5
Tp = 7.5
seed = 42

### Instanciate Environment
env = Env(sim_time, Hs, Tp, seed,
            ramp_time=ramp_time, ext=-2.5, rot=22.5)


### Setting blender scene stuff
bpy.ops.object.camera_add()
bpy.context.object.name = 'Camera'

bpy.ops.object.light_add()
bpy.context.object.name = 'Light'


@app.get("/predict")
def process_vid(hs_user, tp_user, seed_user):

    # Overwrite hard coded Env attributes with user attributes from the API
    Env.Hs = float(hs_user)
    Env.Tp = float(tp_user)
    Env.seed = int(seed_user)

    # Predict loop
    observation = env.state
    score = 0
    done = False
    while not done:
        action = agent.choose_action(observation)
        action_value = agent.get_action_values(action)
        observation_, reward, done = env.step(action_value)
        score += reward
        observation = observation_

    env.get_media(MODEL_FOLDER, episode)
    average_score = -score/sim_time*TIME_STEP

    # More for debuggin
    print(f'Hs:{Hs}m Tp:{Tp}s Seed:{seed} Avg.Dist.:{round(average_score,2)}m')

    # Path to rendered video
    video = f"{path_to_models}models/{MODEL_FOLDER}/episode={episode}/renderings/Sim_Vid_ep={episode}.mp4"

    return FileResponse(video)
