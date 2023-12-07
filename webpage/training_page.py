import streamlit as st
import os

def page3():
    st.markdown("<h1 style='text-align: center;'>The Evolution of Our Model</h1>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("<h3 style='text-align: center;'>Our Baseline Model:<h3>", unsafe_allow_html=True)

    abs_path = os.path.dirname(__file__)
    gif_b = f"{abs_path}/for_web/Baseline.gif"
    st.image(gif_b)
    # st.markdown(f'<img src="{gif_b}"/>', unsafe_allow_html=True)

    st.write("As can be seen in the baseline video, the tip of the crane doesn't manage to\
        reach the inside of the target at any point during the video. This means that the\
            crane would be unstable during the lowering of a container. This is where the training began.")

    st.write('---')
    st.markdown("<h3 style= 'text-align: center;'>The Step by Step Improvements</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h5 style= 'text-align: center;'> After 0 Episodes:</h5>", unsafe_allow_html=True)
        gif_0 = f"{abs_path}/for_web/ep=0.gif"
        st.image(gif_0)
        st.write('---')

        st.markdown("<h5 style= 'text-align: center;'>After 50 Episodes:</h5>", unsafe_allow_html=True)
        gif_50 = f"{abs_path}/for_web/ep=50.gif"
        st.image(gif_50)

    with col2:
        st.markdown("<h5 style= 'text-align: center;'> After 100 Episodes:</h5>", unsafe_allow_html=True)
        gif_100 = f"{abs_path}/for_web/ep=100.gif"
        st.image(gif_100)
        st.write('---')

        st.markdown("<h5 style= 'text-align: center;'>After 600 Episodes:</h5>", unsafe_allow_html=True)
        gif_600 = f"{abs_path}/for_web/ep=600.gif"
        st.image(gif_600)
