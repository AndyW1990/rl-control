import streamlit as st
import os

def page3():
    st.markdown("<h1 style='text-align: center;'>The Evolution of Our Model</h1>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("<h3 style='text-align: center;'>Our Baseline Model:<h3>", unsafe_allow_html=True)

    abs_path = os.path.dirname(__file__)
    vid_path = f"{abs_path}/../models/working_model/episode=0/renderings/Sim_Vid_ep=0.mp4"
    st.video(vid_path, format = 'video/mp4', start_time=0)
    st.write("As can be seen in the baseline video, the tip of the crane doesn't manage to\
        reach the inside of the target at any point during the video. This means that the\
            crane would be unstable during the lowering of a container. This is where the training began.")

    st.write('---')
    st.markdown("<h3 style= 'text-align: center;'>The Step by Step Improvements</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h5 style= 'text-align: center;'> After 100 Episodes:</h5>", unsafe_allow_html=True)
        st.video(vid_path, format = 'video/mp4', start_time=0)
        st.write('---')

        st.markdown("<h5 style= 'text-align: center;'>After 800 Episodes:</h5>", unsafe_allow_html=True)
        st.video(vid_path, format = 'video/mp4', start_time=0)

    with col2:
        st.markdown("<h5 style= 'text-align: center;'> After 500 Episodes:</h5>", unsafe_allow_html=True)
        st.video(vid_path, format = 'video/mp4', start_time=0)
        st.write('---')

        st.markdown("<h5 style= 'text-align: center;'>After 1200 Episodes:</h5>", unsafe_allow_html=True)
        st.video(vid_path, format = 'video/mp4', start_time=0)
