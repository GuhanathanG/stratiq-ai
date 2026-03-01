import streamlit as st
from auth import init_auth_db, register_user, login_user, logout

st.set_page_config(
    page_title="STRATIQ AI",
    page_icon="🚀",
    layout="wide"
)

# ===== INIT AUTH DB =====
init_auth_db()

# ===== SESSION STATE =====
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

# ===== LOGIN / REGISTER UI =====

st.markdown("# 🚀 STRATIQ AI")
st.markdown("### Secure Financial Intelligence Platform")
st.markdown("---")

if not st.session_state.authenticated:

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ----- LOGIN -----
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # ----- REGISTER -----
    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists")

else:
    st.success(f"Welcome, {st.session_state.username} 👋")

    if st.button("Logout"):
        logout()
        st.rerun()

    st.markdown("""
    ## Access your tools from the sidebar:

    • 📊 Financial Dashboard  
    • 🤖 AI Co-Pilot  
    • 📄 Executive Report  
    • 📊 Scenario Comparison  
    """)