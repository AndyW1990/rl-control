import streamlit as st
import os

def page5():

    abs_path = os.path.dirname(__file__)
    img_path = os.path.join(abs_path, 'for_web', 'crane.png')

    st.markdown("<h1 style='text-align: center;'>Limitations and Improvements</h1>", unsafe_allow_html=True)

    st.write('---')
    st.markdown("""
            <div style='margin-top: 50px; text-align: center;'>
                <ul style='list-style-position: inside;'>
                    <li style='font-size: 18px;'>Upgrade to a continuous action space, with an algorithm such as PPO or DDPG</li>
                    <li style='font-size: 18px;'>Expand to 6 degrees of freedom and include more wave directions</li>
                     <li style='font-size: 18px;'>Requires aditional degree of freedom for the crane (Slewing)</li>
                    <li style='font-size: 18px;'>Displacements are currently imposed, used force based approach by creating cylinders</li>
                    <li style='font-size: 18px;'>Include other external factors such as vessel drift and wind</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
