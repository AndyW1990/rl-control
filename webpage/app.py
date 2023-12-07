import streamlit as st
from home_page import page1
from training_page import page2
from models_page import page3
from demo_page import page4
from limitations_page import page5

st.set_page_config(page_title="Motion Compensated Crane with Machine Learning", layout="wide")


pages = {
    "Home": page1,
    "Training Evolution": page2,    
    "Model Demo": page3,
    "Live Demo": page4,
    "Limitations": page5
}

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page with the session state
page = pages[selection]
page()
