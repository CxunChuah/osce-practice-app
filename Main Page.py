import streamlit as st
import re
import random
import smtplib
from email.mime.text import MIMEText
import time

# 📬 Email-sending function using Gmail SMTP
def send_verification_email(to_email, code):
    sender_email = st.secrets["GMAIL_USER"]
    sender_password = st.secrets["GMAIL_PASS"]
    subject = "Your OSCE Signup Code (Check Inbox)"
    body = f"""
    Hi there 👋,

    Thanks for signing up with OSCE Practice App.

    Your verification code is: {code}

    If you didn’t request this, you can safely ignore this message.

    Cheers,
    The OSCE Team 🩺
    """

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print("SMTP Error:", e)
        return False

st.set_page_config(page_title="OSCE Practice App", page_icon="🩺", layout="centered")

# ✅ Handle ?nav=signup or ?nav=login in URL
query_params = st.query_params
if query_params.get("nav") == "signup":
    st.session_state.auth_mode = "Sign Up"
elif query_params.get("nav") == "login":
    st.session_state.auth_mode = "Sign In"

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Sign In"

st.markdown("<h1 style='text-align:center; color:#19527c;'>Welcome to OSCE Practice App 🩺</h1>", unsafe_allow_html=True)

if st.session_state.auth_mode == "Sign Up":
    st.subheader("📝 Create Your Account")
    new_email = st.text_input("Email address")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    def is_password_strong(pw):
        return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", pw))

    if st.button("Sign Up"):
        if new_password != confirm_password:
            st.error("❌ Passwords do not match")
        elif not is_password_strong(new_password):
            st.warning("⚠️ Password must be at least 8 characters and include uppercase, lowercase, and a number.")
        elif new_email:
            code = str(random.randint(100000, 999999))
            st.session_state.generated_code = code
            if send_verification_email(new_email, code):
                st.success("📬 A verification code has been sent to your email!")
                st.session_state.show_verification = True
            else:
                st.error("❌ Failed to send email.")
        else:
            st.warning("Please complete all fields.")

    if st.session_state.get("show_verification"):
        user_code = st.text_input("Enter the verification code")
        if user_code == st.session_state.get("generated_code"):
            st.session_state.logged_in = True
            st.session_state.auth_mode = "Dashboard"
            st.session_state.shown_welcome = False
            st.success("✅ Email verified and account created!")

    st.markdown("Already have an account? [Log in here](?nav=login)", unsafe_allow_html=True)

elif st.session_state.auth_mode == "Sign In":
    st.subheader("🔑 Sign In")
    login_email = st.text_input("Email address")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_email and login_password:
            st.session_state.logged_in = True
            st.session_state.auth_mode = "Dashboard"
            st.session_state.shown_welcome = False
        else:
            st.warning("Please enter both email and password.")

    st.markdown("Don’t have an account? [Sign up here](?nav=signup)", unsafe_allow_html=True)

# ✅ Welcome Pop-up After Login
if st.session_state.get("logged_in") and not st.session_state.get("shown_welcome"):
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
            <p style='font-size: 16px;'>You’ve successfully signed in to your OSCE Dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.session_state.shown_welcome = True
    time.sleep(2.5)  # pause to allow user to see the pop-up
    st.switch_page("pages/1_Dashboard.py")

# ✅ Dashboard View with Log Out button
if st.session_state.get("auth_mode") == "Dashboard" and st.session_state.get("logged_in"):
    st.markdown("<h3 style='color:#19527c;'>👋 Hello, and welcome to your dashboard</h3>", unsafe_allow_html=True)

    if st.button("Log Out 🔒"):
        st.session_state.clear()
        st.success("You’ve been logged out.")
        st.stop()
