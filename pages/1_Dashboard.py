import streamlit as st

# Page config
st.set_page_config(page_title="Dashboard - OSCE App", page_icon="🩺", layout="wide")

# Check if logged in
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access this page.")
    st.switch_page("Main Page.py")

# Display header and welcome
st.title("OSCE Practice Dashboard")
st.write(f"Welcome, {st.session_state.get('username', 'User')}! 👋")

# Main dashboard content
st.markdown("## Practice Options")

# Create two columns for the options
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### Start Practice
    Practice with specific OSCE stations
    """)
    if st.button("Start Practice", key="practice_btn"):
        st.switch_page("pages/2_Practice.py")

with col2:
    st.markdown("""
    ### My History
    View your past practice results
    """)
    if st.button("View History", key="history_btn", disabled=True):
        st.info("Coming soon!")

with col3:
    st.markdown("""
    ### Mock Exam
    Take a full mock OSCE exam
    """)
    if st.button("Start Mock Exam", key="mock_btn", disabled=True):
        st.info("Coming soon!")

# Add separator
st.markdown("---")

# Add Log Out button at the bottom of the page
if st.button("Log Out 🔒", key="logout_btn"):
    # Clear session state except for registered users
    for key in list(st.session_state.keys()):
        if key != "registered_users":  # Keep the registered users data
            del st.session_state[key]
    st.success("You've been logged out.")
    st.switch_page("Main Page.py")

# Display version
st.markdown("""
<div style="text-align: center; color: #888; margin-top: 50px;">
    <small>OSCE Practice App v1.0</small>
</div>
""", unsafe_allow_html=True)
