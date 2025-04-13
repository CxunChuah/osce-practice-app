import streamlit as st
import re
import random
import smtplib
from email.mime.text import MIMEText
import time

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

# Debug registered users - uncomment this to see what's in the session state
# if "registered_users" in st.session_state:
#     st.write("Debug - Registered Users:", st.session_state.registered_users)

# 📬 Email-sending function using Gmail SMTP
def send_verification_email(to_email, code):
    try:
        sender_email = st.secrets["GMAIL_USER"]
        sender_password = st.secrets["GMAIL_PASS"]
        subject = "Your OSCE Signup Code (Check Inbox)"
        body = f"""
        Hi there 👋,

        Thanks for signing up with OSCE Practice App.

        Your verification code is: {code}

        If you didn't request this, you can safely ignore this message.

        Cheers,
        The OSCE Team 🩺
        """

        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print("SMTP Error:", e)
        return False

# Password strength checker
def is_password_strong(pw):
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", pw))

# Initialize registered users with some test accounts for development
if "registered_users" not in st.session_state:
    st.session_state.registered_users = {
        # Add a test account for easy login during development
        "test@example.com": {
            "password": "Test1234",
            "username": "testuser",
            "created_at": "2023-01-01"
        }
    }

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
                # For testing purposes - skip email verification if needed
                if "skip_verification" in st.secrets and st.secrets["skip_verification"]:
                    # Create account directly
                    st.session_state.registered_users[new_email] = {
                        "password": new_password,
                        "created_at": time.strftime("%Y-%m-%d"),
                        "username": new_email.split("@")[0]
                    }
                    st.session_state.username = new_email.split("@")[0]
                    st.session_state.logged_in = True
                    st.session_state.shown_welcome = False
                    st.success("✅ Account created successfully!")
                    st.switch_page("pages/1_Dashboard.py")
                else:
                    # Regular email verification flow
                    code = str(random.randint(100000, 999999))
                    st.session_state.generated_code = code
                    st.session_state.current_signup_email = new_email
                    st.session_state.current_signup_password = new_password
                    
                    # For development, show the code in the UI
                    if "debug_mode" in st.secrets and st.secrets["debug_mode"]:
                        st.info(f"Debug: Verification code is {code}")
                        st.session_state.show_verification = True
                    else:
                        if send_verification_email(new_email, code):
                            st.success("📬 A verification code has been sent to your email!")
                            st.session_state.show_verification = True
                        else:
                            st.error("❌ Failed to send email. Please try signing up again.")

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
    
    with st.form(key="login_form"):
        login_email = st.text_input("Email address")
        login_password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if not login_email or not login_password:
                st.warning("Please enter both email and password.")
            else:
                # Debug output - can be removed in production
                # st.write("Email exists in registry:", login_email in st.session_state.registered_users)
                # st.write("Registered users:", list(st.session_state.registered_users.keys()))
                
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
                    st.error(f"❌ Email '{login_email}' is not registered. Please sign up first.")
                    
                    # Development option - enable easy account creation for testing
                    if "easy_signup" in st.secrets and st.secrets["easy_signup"]:
                        if st.button("Create test account with this email"):
                            st.session_state.registered_users[login_email] = {
                                "password": login_password,
                                "created_at": time.strftime("%Y-%m-%d"),
                                "username": login_email.split("@")[0]
                            }
                            st.success(f"Test account created for {login_email}!")
                            st.experimental_rerun()

    st.markdown("Don't have an account? [Sign up here](?nav=signup)", unsafe_allow_html=True)

# Demo credentials note
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
    <small>OSCE Practice App for Physiotherapy Students</small>
    </div>
    """, unsafe_allow_html=True)

# For development only - Add button to view registered users 
if "debug_mode" in st.secrets and st.secrets["debug_mode"]:
    if st.button("Debug: Show Registered Users"):
        st.write("Registered Users:", st.session_state.registered_users)

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

# Only show dashboard if logged in
if st.session_state.get("logged_in", False):
    # Main dashboard content
    st.markdown("<h1 style='text-align:center; color:#19527c;'>Welcome to OSCE Practice App 🩺</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#19527c;'>👋 Hello, {st.session_state.get('username', 'User')}!</h3>", unsafe_allow_html=True)
    
    # Quick navigation buttons
    st.markdown("### Quick Navigation")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Practice OSCE Stations 🏥"):
            st.switch_page("pages/2_Practice.py")
    with col2:
        # If you have this page, uncomment the following code
        #if st.button("View Your Progress 📊"):
        #    st.switch_page("pages/3_Progress.py")
        st.button("View Your Progress 📊", disabled=True)
    
    # Log Out button
    if st.button("Log Out 🔒"):
        for key in list(st.session_state.keys()):
            if key != "registered_users":  # Keep the registered users data
                del st.session_state[key]
        st.success("You've been logged out.")
        st.rerun()
