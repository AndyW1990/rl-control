import streamlit as st
import os

def page1():

    abs_path = os.path.dirname(__file__)
    img_path = os.path.join(abs_path, 'for_web', 'crane.png')

    st.markdown("<h1 style='text-align: center;'>Reinforcement Learning Control</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Motion Compensated Crane Aboard a Ship</h2>", unsafe_allow_html=True)

    st.write('---')
    st.markdown("<h3 style='text-align: center;'>What is our project?</h3>", unsafe_allow_html=True)

    bul,img = st.columns(2)
    with bul:
        st.markdown("""
        <div style='margin-top: 0px; text-align: left;'>
            <ul style='list-style-position: inside;'>
                <li style='font-size: 18px;'>Proof of concept for machine learning in<br><pre>engineering control tasks</li>
                <li style='font-size: 18px;'>Simulating wave induced vessel motion<br><pre>in 3 degrees of freedom</li>
                <li style='font-size: 18px;'>Environment created in Python with Blender<pre></li>
                <li style='font-size: 18px;'>Using Reinforcement Learning to control<br><pre>a crane with 2 degeres of freedom</li>
                <li style='font-size: 18px;'>A Double DQN is used to train the Agent</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with img:
        st.image(f'{img_path}', width=500)

    st.write('---')
