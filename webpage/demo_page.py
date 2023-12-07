import streamlit as st
import numpy as np
import os
import time


def page4():
    st.markdown("<h1 style='text-align: center;'>Live Demo</h1>", unsafe_allow_html=True)
    st.write('---')
    st.write('Choose a wave height (Hs), period (Tp) and seed number to solve and render a new random wave.')
    if 'height' not in st.session_state:
        st.session_state['height'] = '2.5m'
    if 'period' not in st.session_state:
        st.session_state['period'] = '7.5s'


    st.markdown("<h3 style='text-align: center;'>Choose Wave Height (m):<h3>", unsafe_allow_html=True)
    st.session_state['height'] = st.text_input('', '1.5')
    
    st.markdown("<h3 style='text-align: center;'>Choose Wave Period (s):<h3>", unsafe_allow_html=True)
    st.session_state['period'] = st.text_input('', '5.0')
    

    st.sidebar.title('Parameters for the model:')
    h,p = st.sidebar.columns(2)
    h.subheader('Wave Height:')
    h.write(st.session_state.height)
    b1 = h.button('Generate')
    p.subheader('Wave Period:')
    p.write(st.session_state.period)

    if b1:
        time.sleep(10)
        abs_path = os.path.dirname(__file__)
        vid_path = f"{abs_path}/for_web/Sim_Vid_ep={st.session_state['height']}m_{st.session_state['period']}s.mp4"
        st.subheader(f"Wave of Height {st.session_state['height']}m and Period {st.session_state['period']}s")
        st.video(vid_path, format = 'video/mp4', start_time=0)
