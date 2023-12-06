import streamlit as st
import numpy as np
import os


def page2():

    abs_path = os.path.dirname(__file__)
    vid_path = os.path.join(abs_path, 'for_web', 'trimmed.mp4')

    st.title('Baseline Model of the Crane')
    st.write('This is how far a crane is from the target if no machine learning is done first.')
    st.write('As can be seen the tip of the crane is rarely within the target range to drop a container.')
    st.video(vid_path, format = 'video/mp4', start_time=0)
    st.write('---')



    if 'height' not in st.session_state:
        st.session_state['height'] = 'Pick a Height'
    if 'period' not in st.session_state:
        st.session_state['period'] = 'Pick a Period'


    st.sidebar.subheader('Choose Wave Height')
    h1, h2, h3 = st.sidebar.columns(3)
    b1 = h1.button('2m')
    b2 = h2.button('3m')
    b3 = h3.button('4m')

    if b1:
        st.session_state['height'] = '2m'
    elif b2:
        st.session_state['height'] = '3m'
    elif b3:
        st.session_state['height'] = '4m'

    st.sidebar.subheader('Choose Wave Period')
    p1, p2, p3 = st.sidebar.columns(3)
    b4 = p1.button('5s')
    b5 = p2.button('7s')
    b6 = p3.button('10s')

    if b4:
        st.session_state['period'] = '5s'
    elif b5:
        st.session_state['period'] = '7s'
    elif b6:
        st.session_state['period'] = '10s'


    st.sidebar.title('Parameters for the model:')
    h,p = st.sidebar.columns(2)
    h.subheader('Wave Height:')
    h.write(st.session_state.height)
    p.subheader('Wave Period:')
    p.write(st.session_state.period)

    # if st.sidebar.button('Generate Data'):
    #     wave_height = np.random.rand() * 3
    #     wave_speed = np.random.rand() * 5 + 5

    #     height_slider = st.sidebar.slider('Wave Height', min_value = 1.0, max_value = 3.0, value = round(wave_height, 2))
    #     speed_slider = st.sidebar.slider('Wave Speed', min_value = 5.0, max_value = 10.0, value = round(wave_speed,2))

    #     st.write('---')
    #     col4, col5, col6 = st.columns(3)
    #     col4.metric('Wave Period', f'{round(wave_speed, 2)}s')
    #     col5.metric('Wave Height', f'{round(wave_height, 2)}m')
    #     col6.metric('Accuracy', '80%')
