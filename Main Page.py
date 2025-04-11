import streamlit as st
import re
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# 📬 Email-sending function (HTML version)
def send_verification_email(to_email, code):
    message = Mail(
        from_email='chuahchuahchuah0930@gmail.com',  # replace with your verified sender
        to_emails=to_email,
        subject='Your OSCE App Verification Code',
        html_content=f"""
        <p>Hi there 👋,</p>
        <p>Your verification code is: <strong>{code}</strong></p>
        <p>If you didn’t request this, just ignore it.</p>
        <p>Cheers,<br>The OSCE Team</p>
        """
    )
    try:
        sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
        sg.send(message)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

st.set_page_config(page_title="OSCE Practice App", page_icon="🩺", layout="centered")

# Hide sidebar and enhance styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    .main-title {
        font-size: 2.8em;
        font-weight: 900;
        text-align: center;
        margin-top: 1em;
        color: #0096c7;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .subtitle {
        font-size: 1.2em;
        text-align: center;
        color: #4a4a4a;
        margin-bottom: 2em;
    }
    .login-box {
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 2em;
        background-color: #f9f9f9;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .link-button {
        color: #00f5d4;
        text-decoration: underline;
        cursor: pointer;
        font-size: 0.9em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Welcome to OSCE Practice App 🩺</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Practice. Reflect. Improve.</div>", unsafe_allow_html=True)

# Auth mode toggle
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Sign In"

# Handle query parameter switching without experimental_set_query_params
nav = st.query_params.get("nav", "").lower()
if nav == "signup":
    st.session_state.auth_mode = "Sign Up"
elif nav == "login":
    st.session_state.auth_mode = "Sign In"

# Switch between login/signup/forgot
if st.session_state.auth_mode == "Forgot Password":
    st.subheader("🔐 Forgot Password")
    reset_email = st.text_input("Enter your registered email")
    if st.button("Send Reset Link"):
        if reset_email:
            st.success(f"Password reset link sent to {reset_email} (simulation)")
        else:
            st.warning("Please enter your email.")
    if st.button("Back to Login"):
        st.session_state.auth_mode = "Sign In"

elif st.session_state.auth_mode == "Sign Up":
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
            st.success("✅ Email verified and account created!")
            st.switch_page("pages/1_Dashboard.py")

    st.markdown("""
        <p style='font-size: 0.9em; color: #555;'>
        Already have an account? <a href='?nav=login' class='link-button'>Back to Login</a>
        </p>
    """, unsafe_allow_html=True)

else:
    st.subheader("🔑 Sign In")
    login_email = st.text_input("Email address")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_email and login_password:
            st.session_state.logged_in = True
        else:
            st.warning("Please enter both email and password.")

    if st.button("Forgot Password?"):
        st.session_state.auth_mode = "Forgot Password"

    st.markdown("""
        <p style='font-size: 0.9em; color: #555;'>
        Don’t have an account? <a href='?nav=signup' class='link-button'>Sign up here</a>
        </p>
    """, unsafe_allow_html=True)

# --------------------- FADE-IN ANIMATION ---------------------
if st.session_state.get("logged_in"):
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
            <p style='font-size: 16px;'>You’ve successfully logged in to your OSCE Dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
