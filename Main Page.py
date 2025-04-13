import streamlit as st
import re
import random
import smtplib
from email.mime.text import MIMEText
import time
import json
import os

# Set page configuration
st.set_page_config(page_title="Login - OSCE App", page_icon="🩺", layout="centered")

# Hide sidebar on login page
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# File path for storing user data (for development/testing)
USER_DATA_FILE = "user_data.json"

# Function to load user data from file
def load_user_data():
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading user data: {e}")
    return {}

# Function to save user data to file
def save_user_data(user_data):
    try:
        with open(USER_DATA_FILE, "w") as f:
            json.dump(user_data, f)
    except Exception as e:
        st.error(f"Error saving user data: {e}")

# 📬 Email-sending function using Gmail SMTP
def send_verification_email(to_email, code):
    try:
        # For testing, we'll just show the code instead of sending email
        st.info(f"📧 Your verification code is: {code}")
        return True
        
        # Uncomment below to use actual email sending
        """
        sender_email = st.secrets["GMAIL_USER"]
        sender_password = st.secrets["GMAIL_PASS"]
        subject = "Your OSCE Signup Code (Check Inbox)"
        body = f'''
        Hi there 👋,

        Thanks for signing up with OSCE Practice App.

        Your verification code is: {code}

        If you didn't request this, you can safely ignore this message.

        Cheers,
        The OSCE Team 🩺
        '''

        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
        """
    except Exception as e:
        print("SMTP Error:", e)
        return False

# Password strength checker
def is_password_strong(pw):
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", pw))

# Initialize registered users
if "registered_users" not in st.session_state:
    # Load existing users from file
    loaded_users = load_user_data()
    
    # Add test account if there are no users yet
    if not loaded_users:
        loaded_users = {
            "test@example.com": {
                "password": "Test1234",
                "username": "testuser",
                "created_at": "2023-01-01"
            }
        }
        save_user_data(loaded_users)
    
    st.session_state.registered_users = loaded_users

# Debug - Show registered users (comment this out in production)
# st.write("Current registered users:", st.session_state.registered_users)

# Check if user is already logged in
if st.session_state.get("logged_in", False):
    # Navigate to dashboard directly
    st.switch_page("pages/1_Dashboard.py")

# ✅ Handle ?nav=signup or ?nav=login in URL
query_params = st.query_params
if query_params.get("nav") == "signup":
    st.session_state.auth_mode = "Sign Up"
elif query_params.get("nav") == "login":
    st.session_state.auth_mode = "Sign In"

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Sign In"

st.markdown("<h1 style='text-align:center; color:#19527c;'>OSCE Practice App 🩺</h1>", unsafe_allow_html=True)

# Sign Up Form
if st.session_state.auth_mode == "Sign Up":
    st.subheader("📝 Create Your Account")
    
    with st.form(key="signup_form"):
        new_email = st.text_input("Email address")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm password", type="password")
        submit_button = st.form_submit_button("Sign Up")

        if submit_button:
            if not new_email or not new_password or not confirm_password:
                st.warning("Please complete all fields.")
            elif new_password != confirm_password:
                st.error("❌ Passwords do not match")
            elif not is_password_strong(new_password):
                st.warning("⚠️ Password must be at least 8 characters and include uppercase, lowercase, and a number.")
            elif new_email in st.session_state.registered_users:
                st.error(f"❌ The email '{new_email}' is already registered. Please use a different email or log in instead.")
            else:
                # Generate verification code
                code = str(random.randint(100000, 999999))
                st.session_state.generated_code = code
                st.session_state.current_signup_email = new_email
                st.session_state.current_signup_password = new_password
                
                # Send code (or simulate sending)
                if send_verification_email(new_email, code):
                    st.success("📬 A verification code has been sent. Check above for the code! (In production, this would go to your email)")
                    st.session_state.show_verification = True
                else:
                    st.error("❌ Failed to send verification code. Please try again.")

    # Verification form
    if st.session_state.get("show_verification"):
        with st.form(key="verification_form"):
            user_code = st.text_input("Enter the verification code")
            verify_button = st.form_submit_button("Verify")
            
            if verify_button:
                if user_code == st.session_state.get("generated_code"):
                    email = st.session_state.get("current_signup_email")
                    password = st.session_state.get("current_signup_password")
                    if email and password:
                        # Store new user
                        st.session_state.registered_users[email] = {
                            "password": password,
                            "created_at": time.strftime("%Y-%m-%d"),
                            "username": email.split("@")[0]
                        }
                        
                        # Save to file for persistence
                        save_user_data(st.session_state.registered_users)
                        
                        # Set session state
                        st.session_state.username = email.split("@")[0]
                        st.session_state.logged_in = True
                        st.session_state.shown_welcome = False
                        
                        st.success("✅ Email verified and account created!")
                        st.switch_page("pages/1_Dashboard.py")
                else:
                    st.error("❌ Invalid verification code")

    st.markdown("Already have an account? [Log in here](?nav=login)", unsafe_allow_html=True)

# Sign In Form
elif st.session_state.auth_mode == "Sign In":
    st.subheader("🔑 Sign In")
    
    # Debug display - uncomment if needed
    # st.write("Available emails:", list(st.session_state.registered_users.keys()))
    
    with st.form(key="login_form"):
        login_email = st.text_input("Email address")
        login_password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if not login_email or not login_password:
                st.warning("Please enter both email and password.")
            else:
                # Check if the email exists in our registered users
                if login_email in st.session_state.registered_users:
                    user_data = st.session_state.registered_users[login_email]
                    # Verify the password matches
                    if login_password == user_data.get("password"):
                        st.session_state.logged_in = True
                        st.session_state.shown_welcome = False
                        st.session_state.username = user_data.get("username", login_email.split("@")[0])
                        st.success("✅ Login successful!")
                        st.switch_page("pages/1_Dashboard.py")
                    else:
                        st.error("❌ Incorrect password")
                else:
                    # Reload user data from disk in case it was updated
                    loaded_users = load_user_data()
                    st.session_state.registered_users = loaded_users
                    
                    # Check again after reload
                    if login_email in st.session_state.registered_users:
                        user_data = st.session_state.registered_users[login_email]
                        if login_password == user_data.get("password"):
                            st.session_state.logged_in = True
                            st.session_state.shown_welcome = False
                            st.session_state.username = user_data.get("username", login_email.split("@")[0])
                            st.success("✅ Login successful!")
                            st.switch_page("pages/1_Dashboard.py")
                        else:
                            st.error("❌ Incorrect password")
                    else:
                        st.error(f"❌ Email '{login_email}' is not registered. Please sign up first.")

    st.markdown("Don't have an account? [Sign up here](?nav=signup)", unsafe_allow_html=True)

# Add "Use Test Account" button for easy testing
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Use Test Account"):
        st.session_state.logged_in = True
        st.session_state.username = "testuser"
        st.session_state.shown_welcome = False
        st.success("✅ Logged in with test account!")
        st.switch_page("pages/1_Dashboard.py")

# Demo credentials note
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
    <small>OSCE Practice App for Physiotherapy Students</small>
    </div>
    """, unsafe_allow_html=True)

# Force reload registered users
if st.button("🔄 Refresh Login System", help="Click this if you're having login issues"):
    # Reload user data from disk
    loaded_users = load_user_data()
    st.session_state.registered_users = loaded_users
    st.success("Login system refreshed!")
    st.experimental_rerun()

# Welcome Pop-up After Login
if not st.session_state.get("shown_welcome", False) and st.session_state.get("logged_in", False):
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
