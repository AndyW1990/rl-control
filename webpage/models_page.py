import streamlit as st
import numpy as np
import os


def page2():

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

    abs_path = os.path.dirname(__file__)
    vid_path = f"{abs_path}/../assets/Example_Video_{st.session_state['height']}_{st.session_state['period']}"
    st.subheader(f"Wave of Height {st.session_state['height']} and Period {st.session_state['period']}")
    st.video(vid_path, format = 'video/mp4', start_time=0)
