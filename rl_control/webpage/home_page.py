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

    # st.markdown("""
    #             <div style="display: flex; justify-content: center; align-items: start;">
    #                 <div style="margin-right: 20px;">
    #                     <ul>
    #                         <li>Proving that machine learning can be used<br> for engineering control tasks</li>
    #                         <li>Simulating true vessel motion on waves</li>
    #                         <li>Creating a motion compensating crane</li>
    #                         <li>Using a DQN to train the agent</li>
    #                     </ul>
    #                 </div>
    #                 <div>
    #                     <img src="{img_path}" width = "300px">
    #                 </div>
    #             </div>
    #             """, unsafe_allow_html=True)

    # st.write('---')

    st.markdown("<h3 style='text-align: center;'>Limitations and Improvements</h3>", unsafe_allow_html=True)
