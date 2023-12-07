import streamlit as st
import numpy as np
import os


def page3():
    st.markdown("<h1 style='text-align: center;'>Model Demo</h1>", unsafe_allow_html=True)
    st.write('---')
    st.write('Choose a wave height (Hs) and period (Tp) to show the response to a randomly generated (irregular) wave.')
    if 'height' not in st.session_state:
        st.session_state['height'] = '1.5m'
    if 'period' not in st.session_state:
        st.session_state['period'] = '5.0s'


    st.sidebar.subheader('Choose Wave Height')
    h1, h2, h3 = st.sidebar.columns(3)
    b1 = h1.button('1.5m')
    b2 = h2.button('2.5m')
    b3 = h3.button('3.5m')

    if b1:
        st.session_state['height'] = '1.5m'
    elif b2:
        st.session_state['height'] = '2.5m'
    elif b3:
        st.session_state['height'] = '3.5m'

    st.sidebar.subheader('Choose Wave Period')
    p1, p2, p3 = st.sidebar.columns(3)
    b4 = p1.button('5.0s')
    b5 = p2.button('7.5s')
    b6 = p3.button('10.0s')

    if b4:
        st.session_state['period'] = '5.0s'
    elif b5:
        st.session_state['period'] = '7.5s'
    elif b6:
        st.session_state['period'] = '10.0s'


    st.sidebar.title('Parameters for the model:')
    h,p = st.sidebar.columns(2)
    h.subheader('Wave Height:')
    h.write(st.session_state.height)
    p.subheader('Wave Period:')
    p.write(st.session_state.period)

    abs_path = os.path.dirname(__file__)
    vid_path = f"{abs_path}/for_web/Sim_Vid_ep={st.session_state['height']}_{st.session_state['period']}.mp4"
    st.subheader(f"Wave of Height {st.session_state['height']} and Period {st.session_state['period']}")
    st.video(vid_path, format = 'video/mp4', start_time=0)
