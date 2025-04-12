import streamlit as st
import os
import json
import pandas as pd
from pathlib import Path
from login import login_page
from signup import signup_page
from station1 import display_station1  # New import for Station 1

# Make sure the data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Initialize user database file if it doesn't exist
if not os.path.exists("data/users.json"):
    with open("data/users.json", "w") as f:
        json.dump({}, f)

def display_dashboard():
    # Welcome animation (using CSS)
    st.markdown("""
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .welcome-text {
        animation: fadeIn 1.5s ease-in-out;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="welcome-text">Welcome, {st.session_state.username}!</div>', unsafe_allow_html=True)
    
    # Quick access buttons
    st.markdown("### Quick Access")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Start Practice"):
            st.session_state.page = "practice"
            st.experimental_rerun()
    
    with col2:
        if st.button("My History"):
            st.session_state.page = "history"
            st.experimental_rerun()
    
    with col3:
        if st.button("Mock Exam"):
            st.session_state.page = "mock"
            st.experimental_rerun()
    
    # Recent activity or stats could go here
    st.markdown("### Recent Activity")
    st.info("No recent activity found. Start practicing to see your progress!")

def display_practice_options():
    st.title("Start Practice")
    
    # Create a nice grid of station options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Station 1")
        st.markdown("History Taking + VIVA")
        if st.button("Start Station 1"):
            st.session_state.page = "station1"
            st.experimental_rerun()
            
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

def display_history():
    st.title("My History")
    st.info("This page will show your practice history. Feature coming soon!")

def display_mock_exam():
    st.title("Mock Exam")
    st.info("This page will allow you to take a full mock exam. Feature coming soon!")

def main():
    # Set page config
    st.set_page_config(
        page_title="OSCE Practice App",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "page" not in st.session_state:
        st.session_state.page = "login"
    
    # Navigation logic
    if not st.session_state.logged_in:
        # Show login/signup pages
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Login", "Sign Up"])
        
        if page == "Login":
            st.session_state.page = "login"
        else:
            st.session_state.page = "signup"
    else:
        # Show app navigation for logged-in users
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Dashboard", "Start Practice", "My History", "Mock Exam", "Logout"])
        
        if page == "Dashboard":
            st.session_state.page = "dashboard"
        elif page == "Start Practice":
            st.session_state.page = "practice"
        elif page == "My History":
            st.session_state.page = "history"
        elif page == "Mock Exam":
            st.session_state.page = "mock"
        elif page == "Logout":
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.experimental_rerun()
    
    # Display the selected page
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "dashboard":
        display_dashboard()
    elif st.session_state.page == "practice":
        display_practice_options()
    elif st.session_state.page == "station1":  # New page for Station 1
        display_station1()
    elif st.session_state.page == "history":
        display_history()
    elif st.session_state.page == "mock":
        display_mock_exam()

if __name__ == "__main__":
    main()
