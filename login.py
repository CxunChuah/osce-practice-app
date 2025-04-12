import streamlit as st
import re
import random
import smtplib
from email.mime.text import MIMEText

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

# Simulate a registry of users
if "registered_users" not in st.session_state:
    st.session_state.registered_users = {}

# Check if user is already logged in
if st.session_state.get("logged_in", False):
    st.switch_page("Main Page.py")

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
                st.warning("This email is already registered. Please log in instead.")
            else:
                code = str(random.randint(100000, 999999))
                st.session_state.generated_code = code
                st.session_state.current_signup_email = new_email
                st.session_state.current_signup_password = new_password  # Store password for account creation
                if send_verification_email(new_email, code):
                    st.success("📬 A verification code has been sent to your email!")
                    st.session_state.show_verification = True
                else:
                    st.error("❌ Failed to send email.")

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
                        st.session_state.registered_users[email] = {
                            "password": password,
                            "created_at": st.session_state.get("current_time"),
                            "username": email.split("@")[0]  # Default username from email
                        }
                        st.session_state.username = email.split("@")[0]
                        st.session_state.logged_in = True
                        st.session_state.shown_welcome = False
                        st.success("✅ Email verified and account created!")
                        st.switch_page("Main Page.py")
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
                # In a real app, you would verify credentials here
                # For demo, we'll just check if email exists and accept any password
                if login_email in st.session_state.registered_users:
                    user_data = st.session_state.registered_users[login_email]
                    if login_password == user_data.get("password"):
                        st.session_state.logged_in = True
                        st.session_state.shown_welcome = False
                        st.session_state.username = user_data.get("username", login_email.split("@")[0])
                        st.success("✅ Login successful!")
                        st.switch_page("Main Page.py")
                    else:
                        st.error("❌ Incorrect password")
                else:
                    # For testing, allow any email/password
                    st.session_state.logged_in = True
                    st.session_state.shown_welcome = False
                    st.session_state.username = login_email.split("@")[0]
                    st.success("✅ Login successful!")
                    st.switch_page("Main Page.py")

    st.markdown("Don't have an account? [Sign up here](?nav=signup)", unsafe_allow_html=True)

# Demo credentials note
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
    <small>For testing, you can use any email and password</small>
    </div>
    """, unsafe_allow_html=True)
