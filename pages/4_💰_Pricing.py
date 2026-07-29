"""
ShieldEDR — Pricing & Subscription Page (MSME ₹1,000 / Year Plan)
===============================================================
Presents clear pricing tiers focused on the ₹1,000 / year per endpoint plan,
with integrated UPI payments, GPay/PhonePe QR codes, and Razorpay support.
"""

import streamlit as st
from components.auth import init_auth_session, render_auth_sidebar
from components.payment import render_payment_section
from components.styles import inject_light_theme

st.set_page_config(
    page_title="Pricing & Subscription — ShieldEDR",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_light_theme()
init_auth_session()
render_auth_sidebar()

st.markdown("""
<div style="background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 20px; padding: 2.5rem; text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 2.8rem; font-weight: 900; background: linear-gradient(90deg, #c084fc 0%, #60a5fa 50%, #34d399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">
        Enterprise Security Tailored for Indian MSMEs
    </h1>
    <p style="color: #94a3b8; font-size: 1.2rem; max-width: 750px; margin: 0 auto;">
        Antivirus is obsolete against modern ransomware. Get 24/7 EDR protection, Sysmon threat correlation, and automated active response for just <b>₹83 / month</b>.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Pricing Tiers Display
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 1.2, 1])

with col1:
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 1.8rem;">
        <span style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.8rem; font-weight: bold;">FREE TRIAL</span>
        <h3 style="color: #f8fafc; margin-top: 0.8rem; margin-bottom: 0.3rem;">Starter Protection</h3>
        <h2 style="color: #60a5fa; font-size: 2.2rem; margin: 0;">₹0 <span style="font-size: 1rem; color: #94a3b8;">/ 14 days</span></h2>
        <p style="color: #94a3b8; font-size: 0.9rem;">Test 2 endpoints with basic threat scanning.</p>
        <hr style="border-color: rgba(255,255,255,0.1);" />
        <ul style="color: #cbd5e1; font-size: 0.9rem; padding-left: 1.2rem; line-height: 1.8;">
            <td>✔ Up to 2 Devices</td>
            <td>✔ Basic Ransomware Rules</td>
            <td>✔ Community Support</td>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(180deg, #2e1065 0%, #0f172a 100%); border: 2px solid #8b5cf6; border-radius: 18px; padding: 2rem; box-shadow: 0 0 30px rgba(139, 92, 246, 0.4);">
        <span style="background: linear-gradient(90deg, #8b5cf6 0%, #ec4899 100%); color: white; padding: 0.35rem 1rem; border-radius: 999px; font-size: 0.8rem; font-weight: 800;">🔥 MOST POPULAR MSME PLAN</span>
        <h3 style="color: #ffffff; margin-top: 0.8rem; margin-bottom: 0.3rem;">MSME Full Guardian</h3>
        <h2 style="color: #34d399; font-size: 2.6rem; margin: 0;">₹1,000 <span style="font-size: 1rem; color: #94a3b8;">/ year</span></h2>
        <p style="color: #c084fc; font-size: 0.95rem; font-weight: bold; margin-top: 0.3rem;">(Just ₹83 / month per endpoint)</p>
        <hr style="border-color: rgba(139, 92, 246, 0.4);" />
        <ul style="color: #f1f5f9; font-size: 0.95rem; padding-left: 1.2rem; line-height: 2;">
            <li>✅ <b>24/7 Central Server Protection</b></li>
            <li>✅ <b>Full Ransomware & Shadow Copy Blocking</b></li>
            <li>✅ <b>Base64 PowerShell & Sysmon Correlation</b></li>
            <li>✅ <b>Automated Active Response Engine</b></li>
            <li>✅ <b>1-Click Double-Click Installer Script</b></li>
            <li>✅ <b>Priority WhatsApp & Email Alerts</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 16px; padding: 1.8rem;">
        <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.8rem; font-weight: bold;">ENTERPRISE / AGENTS</span>
        <h3 style="color: #f8fafc; margin-top: 0.8rem; margin-bottom: 0.3rem;">Custom Corporate</h3>
        <h2 style="color: #34d399; font-size: 2.2rem; margin: 0;">Custom <span style="font-size: 1rem; color: #94a3b8;">/ volume</span></h2>
        <p style="color: #94a3b8; font-size: 0.9rem;">For organizations with 50+ endpoints & SOC integration.</p>
        <hr style="border-color: rgba(255,255,255,0.1);" />
        <ul style="color: #cbd5e1; font-size: 0.9rem; padding-left: 1.2rem; line-height: 1.8;">
            <li>✔ Unlimited Endpoints</li>
            <li>✔ Dedicated Tenant Isolation</li>
            <li>✔ Custom Rule Engine</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# Payment Section Trigger
# -----------------------------------------------------------------------------
user_email = st.session_state.get("user_email", "admin@shieldedr.com")
is_paid = st.session_state.get("is_paid", False)

if is_paid:
    st.success("🎉 You have an active **₹1,000 / year MSME Guardian Subscription**!")
    col_act1, col_act2 = st.columns([1, 1])
    with col_act1:
        if st.button("💻 Go to Connect Device & Onboarding", type="primary"):
            st.switch_page("pages/3_💻_Connected_Devices.py")
    with col_act2:
        if st.button("📊 View Endpoint Threats & Alerts"):
            st.switch_page("pages/1_🛡️_Endpoints.py")
else:
    st.markdown("## 💳 Complete Your Payment (₹1,000 / Year)")
    render_payment_section(user_email)
