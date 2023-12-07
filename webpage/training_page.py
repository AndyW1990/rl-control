import streamlit as st
import os

def page2():
    st.markdown("<h1 style='text-align: center;'>Model Evolution</h1>", unsafe_allow_html=True)
    #st.markdown("")
    st.write('---')
    st.markdown("<h3 style='text-align: center;'>Baseline Model<h3>", unsafe_allow_html=True)
    

    
    abs_path = os.path.dirname(__file__)
    gif_b = f"{abs_path}/for_web/Baseline.gif"
    st.image(gif_b)
    # st.markdown(f'<img src="{gif_b}"/>', unsafe_allow_html=True)

    st.write('---')
    st.markdown("<h3 style= 'text-align: center;'>Progression through Episodes</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h5 style= 'text-align: center;'> After 1 Episode:</h5>", unsafe_allow_html=True)
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
