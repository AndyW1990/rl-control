# rl-control
##Reinforcement Learning Control - Motion Compensated Crane Aboard a Ship

##training flow:
select number of episodes\
select simulation time per episode (60s?)\
select timestep (0.1s? to start with)\
select hyperparameters for NN\
load agent/model if not fresh train\
load 3d model\
set scores = []\
  &emsp;for each episode:\
    &emsp;&emsp;select wave parameters\
    &emsp;&emsp;generate wave train from function\
    &emsp;&emsp;set score = 0 (score is accumulaiton of rewards)\
    &emsp;&emsp;set done = False (done = True when sim_time reached or set early stop if score = terrible)\
    &emsp;&emsp;set initial state\
    &emsp;&emsp;time = 0\
    &emsp;&emsp;while not done:\
        &emsp;&emsp;&emsp;generate action from state\
        &emsp;&emsp;&emsp;take 1 step with wave train and:\
          &emsp;&emsp;&emsp;&emsp;get new_state, reward, done from env\
        &emsp;&emsp;&emsp;score += reward\
        &emsp;&emsp;&emsp;cache state, new_state, action, reward, done\
        &emsp;&emsp;&emsp;set (current) state = new_state\
        &emsp;&emsp;&emsp;model.learn (have model update params after each action or every x actions)\
        &emsp;&emsp;&emsp;time += timestep\
        &emsp;&emsp;&emsp;if time = sim_time: done = True\
    &emsp;&emsp;scores = append(score)\
    &emsp;&emsp;print info on episode, score and avarage scores\

save model etc after training
    
    
    
