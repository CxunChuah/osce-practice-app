import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📋 OSCE Dashboard")
st.subheader("Welcome to your OSCE Practice Panel")

st.markdown("### What would you like to do today?")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧪 Start OSCE Station"):
        st.success("Loading station... (will link to case later)")

with col2:
    if st.button("📊 My History"):
        st.info("No practice attempts yet.")

with col3:
    if st.button("📘 Resources"):
        st.info("Coming soon: guides, cheat sheets, and tips.")
