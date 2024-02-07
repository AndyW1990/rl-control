# Reinforcement Learning Control
## Motion Compensated Crane Aboard a Ship

![RL Control Crane](/webpage/for_web/crane.png)

### About the Project
- Proof of concept for machine learning in engineering control tasks
- Simulating wave induced vessel motion in 3 degrees of freedom (DoF)
- Environment created in Python with Blender
- Using Reinforcement Learning to control a crane with 2 DoF
- A Double DQN is used to train the Agent
-  [See it in action on Streamlit](https://rl-control-xq2k2a7fzyrowkuptwl6yn.streamlit.app/)


# Model Evolution
## Baseline Model
The baseline model assumes the crane is locked in rotation and extension
![Baseline Model](/webpage/for_web/Baseline.gif)

## Progression through Episodes
### Episode 0:
![Episode 0](/webpage/for_web/ep=0.gif)

### Episode 50:
![Episode 50](/webpage/for_web/ep=50.gif)

### Episode 100:
![Episode 100](/webpage/for_web/ep=100.gif)

### Episode 600:
![BEpisode 600](/webpage/for_web/ep=600.gif)




<!-- Notes
######## INPUTS ##########

- X no. of episodes
    - Each episode is 60s [TBC]

### ACTION SPACE

The actions are relative to the current position of the crane, therefore, a unit of change is actioned on the position at time-step, $t-1$.

We have a discrete action space:

- Translate: -1, 0, 1 units
- Rotation: -1, 0, 1 units

Generating 9 different possible combinations, thus generating 9 different actions.

| Actions | unit_rotation | unit_translate | Q-value |
| --- | --- | --- | --- |
| 1 | -1 | -1 |  |
| 2 | -1 | 0 |  |
| 3 | -1 | 1 |  |
| 4 | 0 | -1 |  |
| 5 | 0 | 0 |  |
| 6 | 0 | 1 |  |
| 7 | 1 | -1 |  |
| 8 | 1 | 0 |  |
| 9 | 1 | 1 |  |

A unit of rotation and translation TBC.

### STATE SPACE

The state space is 2D (X,Z), i.e. environment, is a continuous space which is comprised of:

- The vessels movements;
    - vessel_x
    - vessel_z
    - vessel_ry
- and, the cranes movements;
    - crane_x
    - crane_ry

### WAVE HEIGHT

Storms are classified into 3-hour periods:

- the target seastate is 2.5m Hs - In a storm, of the largest 33% of waves, the mean height is Hs.
- The maximum wave height is 1.7 to 1.8x greater than the mean max height (2.5m). Statistically, we will  only see that impact the vessel once in a 3 hour period.
- Therefore, after 180 x 60s episodes, statistically we should have seen the greatest wave for the specified seas’ locational properties.

### WAVE PERIOD

- The spectrum is used to convert the peak-data from the frequency data to the time domain.
- The peak period is denoted by, Tp, whereby the peak period in the north sea is typically between Tp = 4 to 10s.
    - This describes how often, in time, our vessel is subjected to peak period waves.
    - Peak period wave is where a wave, of random amplitude, energy peaks around that period (i.e. the pressure that will be exerted onto the vessel).
    - Tp is the time between peak waves (i.e. periods).

### SEED

- The seed generates phase offset, creating different components with different wave lengths. Essentially, adding in randomness; preventing the vessel and waves being in-phase.

######## MODEL: DDQN ##########

Action space: Discrete
State space: Continuous
No. of NNs: 2
- Target
- Evaluation

### Epsilon

We will introduce an, $\epsilon$, to introduce randomness into the model, the degree of randomness diminishes the greater amount of training is done.
- This is done to encourage exploration and avoid getting stuck in a local minima.
- Its important to understand that the model knows nothing to start with. If u don’t explore to start it could just continue down an incorrect path with limited ability.
- Thats why ensuring enough episodes is vital otherwise it wont have seen enough data to learn the correct actions. -->
