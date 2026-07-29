"""
ShieldEDR Authentication & User Account Component
===============================================
Manages login, registration, session state, and user subscription profiles.
"""

import streamlit as st
from firestore_db import create_user, authenticate_user, get_user_profile

def init_auth_session():
    """Ensures session state keys exist for authentication."""
    if "user_email" not in st.session_state:
        # Default demo user or logged out state
        st.session_state["user_email"] = "admin@shieldedr.com"
        st.session_state["user_name"] = "Demo MSME Business"
        st.session_state["is_paid"] = True
        st.session_state["is_logged_in"] = True

def render_auth_sidebar():
    """Renders user profile & login/logout state in Streamlit sidebar."""
    init_auth_session()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👤 User Account")

    if st.session_state.get("is_logged_in"):
        email = st.session_state["user_email"]
        profile = get_user_profile(email) or {}
        business = profile.get("business_name", st.session_state.get("user_name", "MSME Business"))
        is_paid = profile.get("is_paid", st.session_state.get("is_paid", False))

        st.sidebar.markdown(f"**Business:** `{business}`")
        st.sidebar.markdown(f"**Account:** `{email}`")

        if is_paid:
            st.sidebar.success("✅ **Active Plan:** ₹1,000/yr Protection")
        else:
            st.sidebar.warning("⚠️ **Plan:** Unpaid / Trial")
            if st.sidebar.button("💳 Upgrade Now (₹1,000/yr)", type="primary"):
                st.switch_page("pages/4_💰_Pricing.py")

        if st.sidebar.button("🚪 Log Out", key="sidebar_logout_btn"):
            st.session_state["is_logged_in"] = False
            st.session_state["user_email"] = None
            st.session_state["is_paid"] = False
            st.rerun()

    else:
        st.sidebar.info("Log in or register to manage your devices & subscription.")
        with st.sidebar.expander("🔑 Log In / Register", expanded=True):
            tab_login, tab_reg = st.tabs(["Log In", "Register"])

            with tab_login:
                login_email = st.text_input("Email Address", key="auth_login_email")
                login_pass = st.text_input("Password", type="password", key="auth_login_pass")
                if st.button("Log In", type="primary", key="auth_login_submit"):
                    if login_email and login_pass:
                        res = authenticate_user(login_email, login_pass)
                        if res["success"]:
                            user = res["user"]
                            st.session_state["is_logged_in"] = True
                            st.session_state["user_email"] = user["email"]
                            st.session_state["user_name"] = user["business_name"]
                            st.session_state["is_paid"] = user.get("is_paid", False)
                            st.success(res["message"])
                            st.rerun()
                        else:
                            st.error(res["message"])
                    else:
                        st.warning("Please enter email and password.")

            with tab_reg:
                reg_name = st.text_input("Business Name", key="auth_reg_name")
                reg_email = st.text_input("Email Address", key="auth_reg_email")
                reg_pass = st.text_input("Create Password", type="password", key="auth_reg_pass")
                if st.button("Create Account", type="primary", key="auth_reg_submit"):
                    if reg_name and reg_email and reg_pass:
                        res = create_user(reg_email, reg_pass, reg_name)
                        if res["success"]:
                            user = res["user"]
                            st.session_state["is_logged_in"] = True
                            st.session_state["user_email"] = user["email"]
                            st.session_state["user_name"] = user["business_name"]
                            st.session_state["is_paid"] = False
                            st.success("Account created! Please complete payment to activate protection.")
                            st.switch_page("pages/4_💰_Pricing.py")
                        else:
                            st.error(res["message"])
                    else:
                        st.warning("Please fill in all fields.")
