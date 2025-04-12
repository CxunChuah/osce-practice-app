import streamlit as st
import time

# Set page configuration
st.set_page_config(page_title="OSCE Practice App", page_icon="🩺", layout="centered")

# Check if logged in, otherwise redirect to login page
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")

# Welcome page after successful login
st.markdown("<h1 style='text-align:center; color:#19527c;'>Welcome to OSCE Practice App 🩺</h1>", unsafe_allow_html=True)

# ✅ Welcome Pop-up After Login
if not st.session_state.get("shown_welcome", False):
    st.markdown(
        """
        <style>
        .fade-popup {
            position: fixed;
            top: 25%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #ffffff;
            padding: 2em 3em;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
            animation: fadeIn 1s ease-in-out forwards;
            z-index: 9999;
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translate(-50%, -60%);}
            to {opacity: 1; transform: translate(-50%, -50%);}
        }
        </style>
        <div class='fade-popup'>
            <h3 style='color:#19527c;'>✅ Welcome!</h3>
            <p style='font-size: 16px;'>You've successfully signed in to your OSCE Dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.session_state.shown_welcome = True
    time.sleep(2.5)
    st.switch_page("pages/1_Dashboard.py")

# Dashboard View
st.markdown("<h3 style='color:#19527c;'>👋 Hello, and welcome to your dashboard</h3>", unsafe_allow_html=True)

# Quick navigation buttons
st.markdown("### Quick Navigation")
col1, col2 = st.columns(2)
with col1:
    if st.button("Practice OSCE Stations 🏥"):
        st.switch_page("pages/2_Practice.py")
with col2:
    if st.button("View Your Progress 📊"):
        st.switch_page("pages/3_Progress.py")  # Assuming you have this page

# Log Out button
if st.button("Log Out 🔒"):
    st.session_state.clear()
    st.success("You've been logged out.")
    st.switch_page("pages/login.py")
