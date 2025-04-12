import streamlit as st
from station1 import display_station1

# Page config
st.set_page_config(page_title="Practice - OSCE App", page_icon="🩺", layout="wide")

# Check if logged in
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access this page.")
    st.switch_page("Main Page.py")

# Check if we're in station1 mode
if st.session_state.get("current_station") == "station1":
    display_station1()
    st.stop()

# Practice options page
st.title("Start Practice")
st.markdown("Select a station to practice:")

# Create a grid of station options
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Station 1")
    st.markdown("History Taking + VIVA")
    if st.button("Start Station 1"):
        st.session_state.current_station = "station1"
        st.rerun()
        
    st.markdown("### Station 3")
    st.markdown("Coming soon...")
    st.button("Start Station 3", disabled=True)
    
    st.markdown("### Station 5")
    st.markdown("Coming soon...")
    st.button("Start Station 5", disabled=True)
    
with col2:
    st.markdown("### Station 2")
    st.markdown("Coming soon...")
    st.button("Start Station 2", disabled=True)
    
    st.markdown("### Station 4")
    st.markdown("Coming soon...")
    st.button("Start Station 4", disabled=True)
    
    st.markdown("### Station 6")
    st.markdown("Coming soon...")
    st.button("Start Station 6", disabled=True)
