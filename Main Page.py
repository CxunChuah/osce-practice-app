import streamlit as st

st.set_page_config(page_title="OSCE Practice App", page_icon="🩺", layout="centered")

# --- Hide Sidebar for Login Page ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    .main-title {
        font-size: 2.2em;
        font-weight: bold;
        text-align: center;
        margin-top: 1em;
        color: #19527c;
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
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Welcome to OSCE Practice App 🩺</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Practice. Reflect. Improve.</div>", unsafe_allow_html=True)

# --- Email Auth Box ---
with st.container():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    
    auth_mode = st.radio("Choose an option:", ["Sign In", "Sign Up"], horizontal=True)
    email = st.text_input("Email address")
    password = st.text_input("Password", type="password")

    if auth_mode == "Sign Up":
        confirm_password = st.text_input("Confirm password", type="password")
        if st.button("Create Account"):
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif not email or not password:
                st.warning("Please enter all fields.")
            else:
                st.success("Verification email sent. Please confirm to continue.")
                verified = st.checkbox("I have verified my email")
                if verified:
                    st.success("Account created and verified!")
                    st.session_state["logged_in"] = True
    else:
        if st.button("Login"):
            if email and password:
                st.success("Welcome back! Redirecting to dashboard...")
                st.session_state["logged_in"] = True
            else:
                st.warning("Please enter your credentials.")

    st.markdown("</div>", unsafe_allow_html=True)

# Redirect simulation
if st.session_state.get("logged_in"):
    st.switch_page("pages/1_Dashboard.py")
