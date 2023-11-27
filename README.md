# rl-control
##Reinforcement Learning Control - Motion Compensated Crane Aboard a Ship

##training flow:
select number of episodes
select simulation time per episode (60s?)
select timestep (0.1s? to start with)
select hyperparameters for NN
load agent/model if not fresh train
load 3d model
set scores = []
  for each episode:
    select wave parameters
    generate wave train from function
    set score = 0 (score is accumulaiton of rewards)
    set done = False (done = True when sim_time reached or set early stop if score = terrible)
    set initial state
    time = 0
    while not done:
        generate action from state
        take 1 step with wave train and:
          get new_state, reward, done from env
        score += reward
        cache state, new_state, action, reward, done
        set (current) state = new_state
        model.learn (have model update params after each action or every x actions)
        time += timestep
        if time = sim_time: done = True
    scores = append(score)
    print info on episode, score and avarage scores

save model etc after training
    
    
    
