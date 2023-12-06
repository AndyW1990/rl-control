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
        <div style='margin-top: 50px; text-align: left;'>
            <ul style='list-style-position: inside;'>
                <li style='font-size: 18px;'>Proving that machine learning can be used<br>for engineering control tasks</li>
                <li style='font-size: 18px;'>Simulating true vessel motion on waves</li>
                <li style='font-size: 18px;'>Creating a motion compensating crane</li>
                <li style='font-size: 18px;'>Using a DQN to train the agent</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with img:
        st.image(f'{img_path}', width=500)

    st.write('---')
    st.markdown("<h3 style='text-align: center;'>Limitations and Improvements</h3>", unsafe_allow_html=True)

    st.markdown("""
            <div style='margin-top: 50px; text-align: center;'>
                <ul style='list-style-position: inside;'>
                    <li style='font-size: 18px;'>Attempt to use a continuous action space</li>
                    <li style='font-size: 18px;'>Increase the degrees of freedom from 3 to 6</li>
                    <li style='font-size: 18px;'>Use a force based approach</li>
                    <li style='font-size: 18px;'>Include other external factors such as wind</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
