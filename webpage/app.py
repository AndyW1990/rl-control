import streamlit as st
from home_page import page1
from models_page import page2
from training_page import page3

st.set_page_config(page_title="Crane Balancing with Machine Learning", layout="wide")


pages = {
    "Home": page1,
    "Models": page2,
    "Training Evolution": page3
}

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page with the session state
page = pages[selection]
page()
