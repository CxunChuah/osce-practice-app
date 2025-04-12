import streamlit as st

# Page config
st.set_page_config(page_title="Dashboard - OSCE App", page_icon="🩺", layout="wide")

# Check if logged in
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access this page.")
    st.switch_page("Main Page.py")

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
    color: #19527c;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="welcome-text">Welcome to Your OSCE Practice Dashboard!</div>', unsafe_allow_html=True)

# Quick access buttons
st.markdown("### Quick Access")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Start Practice"):
        st.switch_page("pages/2_Practice.py")

with col2:
    if st.button("My History"):
        st.info("History page coming soon!")

with col3:
    if st.button("Mock Exam"):
        st.info("Mock Exam feature coming soon!")

# Recent activity or stats
st.markdown("### Recent Activity")
st.info("No recent activity found. Start practicing to see your progress!")

# Tips section
st.markdown("### OSCE Tips")
tips = [
    "Always introduce yourself to the patient",
    "Practice active listening during history taking",
    "Maintain eye contact and show empathy",
    "Structure your questions from open to closed",
    "Always check for red flags in any presentation"
]
for tip in tips:
    st.markdown(f"• {tip}")
