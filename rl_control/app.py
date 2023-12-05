import streamlit as st
import numpy as np
import os


st.set_page_config(page_title = 'RL Control')

st.title('Crane Balancing with Machine Learning')
st.subheader('What is our idea?')
st.write('The premise of our project is to reduce the movement of a crane located on a boat\
    so that the boat is able to lower a container onto a stationary platform withoutendagering\
        people from the boats movement caused by the waves of the ocean.')

st.write('---')

# video = '/Users/juleslockey/code/AndyW1990/rl-control/model_3d/renderings/test_vid/episode=0/test_vid_0.mp4'

abs_path = os.path.dirname(__file__)
video = f'{abs_path}/../model_3d/renderings/test_vid/episode=0/test_vid_0.mp4'

st.title('Baseline Model of the Crane')
st.write('This is how far a crane is from the target if no machine learning is done first.')
st.write('As can be seen the tip of the crane is rarely within the target range to drop a container.')
st.video(video)
col1, col2, col3 = st.columns(3)
col1.metric('Wave Speed', '5 mph', '0.0%')
col2.metric('Wave Height', '3 m', '0.0%')
col3.metric('Accuracy', '27%', '0.0%')

st.write('---')
st.subheader('How did we teach our model to reduce the distance to the target?')

st.sidebar.title('Parameters for the model')
if st.sidebar.button('Generate Data'):
    wave_height = np.random.rand() * 3
    wave_speed = np.random.rand() * 5 + 5

    height_slider = st.sidebar.slider('Wave Height', min_value = 1.0, max_value = 3.0, value = round(wave_height, 2))
    speed_slider = st.sidebar.slider('Wave Speed', min_value = 5.0, max_value = 10.0, value = round(wave_speed,2))

    st.write('---')
    col4, col5, col6 = st.columns(3)
    col4.metric('Wave Speed', f'{round(wave_speed, 2)}', f'{round((wave_speed/5)*100-100, 2)}%')
    col5.metric('Wave Height', f'{round(wave_height, 2)}', f'{round((wave_height/3)*100-100, 2)}%')
    col6.metric('Accuracy', '80%', f'{round((80/27)*100, 2)}%')
