import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="OSCE Practice App", page_icon="🩺", layout="centered")

# --- Title Area ---
st.markdown("""
    <style>
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

# --- Login Box ---
with st.container():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.subheader("Sign In")

    auth_method = st.radio("Sign in with:", ["Google", "Apple", "Phone Number"], horizontal=True)

    if auth_method == "Phone Number":
        phone = st.text_input("Enter your phone number")
    elif auth_method == "Google":
        st.button("Sign in with Google")
    elif auth_method == "Apple":
        st.button("Sign in with Apple")

    st.markdown("---")
    if st.button("Continue"):
        st.success("(Simulation) Logged in successfully!")
        # switch_page("1_Dashboard")  # uncomment when dashboard is ready

    st.markdown("""
        <p style='font-size: 0.9em; color: #555;'>
        First time here? <a href='#' style='color:#19527c;'>Create an account</a>
        </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
