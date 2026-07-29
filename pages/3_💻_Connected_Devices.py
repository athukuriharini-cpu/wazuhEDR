"""
ShieldEDR — Connected Devices & 1-Click Agent Onboarding
======================================================
Manages registered client endpoints and provides pre-configured double-click installers
for non-technical MSME customers.
"""

import os
import streamlit as st
import pandas as pd
from firestore_db import get_user_devices, register_device
from config import WAZUH_API_HOST
from components.auth import init_auth_session, render_auth_sidebar
from components.styles import inject_light_theme

st.set_page_config(
    page_title="Connected Devices — ShieldEDR",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_light_theme()
init_auth_session()
render_auth_sidebar()

user_email = st.session_state.get("user_email", "admin@shieldedr.com")
is_paid = st.session_state.get("is_paid", False)

st.markdown("""
<div style="background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 16px; padding: 1.8rem; margin-bottom: 2rem;">
    <h1 style="color: #c084fc; margin-top: 0;">💻 Connected Devices & 1-Click Agent Onboarding</h1>
    <p style="color: #cbd5e1; font-size: 1.1rem; margin-bottom: 0;">
        Easily connect Windows computers, laptops, and Linux servers to your central EDR server for 24/7 ransomware protection.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Onboarding Section (Pre-Configured 1-Click Installers)
# -----------------------------------------------------------------------------
st.markdown("## 🚀 Step 1: Connect a New Computer (1-Click Installer)")

if not is_paid:
    st.warning("⚠️ Your subscription is unpaid. Please complete payment (₹1,000/yr) to activate agent registration.")
    if st.button("💳 Upgrade & Pay ₹1,000 / Year", type="primary"):
        st.switch_page("pages/4_💰_Pricing.py")

tab_win, tab_linux, tab_mac = st.tabs(["🪟 Windows (Double-Click Installer)", "🐧 Linux (Ubuntu/Debian/RHEL)", "🍎 macOS"])

with tab_win:
    st.subheader("Windows 1-Click Automatic Installer Script")
    st.markdown("""
    Your non-technical customers just need to download this single file and **double-click** it. 
    It automatically installs the Wazuh EDR agent and links it to your Central Cloud Server!
    """)

    server_ip = WAZUH_API_HOST if WAZUH_API_HOST != "localhost" else "YOUR_SERVER_IP"

    # Pre-configured Windows Batch Script Content
    bat_content = f"""@echo off
:: ==============================================================================
:: ShieldEDR One-Click Agent Installer for Windows
:: Central Server: {server_ip}
:: ==============================================================================
echo ==============================================================================
echo   🛡️ ShieldEDR — 24/7 Cyber Security & Ransomware Protection Agent Setup
echo ==============================================================================
echo.

:: Check Admin Rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Please right-click this installer and select 'Run as administrator'.
    pause
    exit /b 1
)

echo [1/3] Downloading Wazuh EDR Agent package...
powershell -Command "Invoke-WebRequest -Uri 'https://packages.wazuh.com/4.x/windows/wazuh-agent-4.9.0-1.msi' -OutFile '%TEMP%\\wazuh-agent.msi'"

echo [2/3] Installing EDR Agent and linking to Central Server ({server_ip})...
msiexec.exe /i "%TEMP%\\wazuh-agent.msi" /q WAZUH_MANAGER="{server_ip}" WAZUH_REGISTRATION_SERVER="{server_ip}"

echo [3/3] Starting ShieldEDR Protection Service...
net start WazuhSvc >nul 2>&1

echo.
echo ==============================================================================
echo   🎉 SUCCESS! Your computer is now 24/7 protected by ShieldEDR Cloud!
echo ==============================================================================
pause
"""

    st.download_button(
        label="📥 Download Windows 1-Click Installer (shield_installer.bat)",
        data=bat_content,
        file_name="shield_installer.bat",
        mime="text/plain",
        type="primary",
    )

    st.code(f"""msiexec.exe /i wazuh-agent-4.9.0-1.msi /q WAZUH_MANAGER='{server_ip}' WAZUH_REGISTRATION_SERVER='{server_ip}'
net start WazuhSvc""", language="powershell")

with tab_linux:
    st.subheader("Linux 1-Line Terminal Setup")
    st.code(f"""curl -sSL https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo gpg --dearmor -o /usr/share/keyrings/wazuh-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/wazuh-keyring.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list
sudo apt-get update && sudo WAZUH_MANAGER='{server_ip}' apt-get install wazuh-agent -y
sudo systemctl enable --now wazuh-agent""", language="bash")

with tab_mac:
    st.subheader("macOS Installer Setup")
    st.markdown(f"1. Download Wazuh macOS Package from `https://packages.wazuh.com/4.x/macos/wazuh-agent-4.9.0-1.pkg`\n"
                f"2. Set Server Manager IP: `{server_ip}`")

st.markdown("---")

# -----------------------------------------------------------------------------
# Registered Devices List
# -----------------------------------------------------------------------------
st.markdown("## 📊 Step 2: Manage Connected Endpoints")

col_add1, col_add2 = st.columns([2, 1])

with col_add1:
    st.subheader("Protected Computer Inventory")

with col_add2:
    with st.expander("➕ Register Device Manually"):
        with st.form("manual_reg_form"):
            dev_name = st.text_input("Device Name", placeholder="e.g. LAPTOP-OFFICE-01")
            dev_os = st.selectbox("Operating System", ["Windows 11 Pro", "Windows 10 Home", "Ubuntu Linux 22.04", "macOS Sonoma"])
            dev_ip = st.text_input("IP Address", value="192.168.1.100")
            submit_dev = st.form_submit_button("Register Device", type="primary")

            if submit_dev and dev_name:
                res = register_device(user_email, dev_name, dev_os, dev_ip)
                if res["success"]:
                    st.success("Device registered!")
                    st.rerun()

# Load User Devices from Database
devices = get_user_devices(user_email)

if devices:
    df_devs = pd.DataFrame(devices)
    st.dataframe(
        df_devs[["device_id", "name", "os", "ip", "status", "agent_version", "installed_at"]],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(f"**Total Protected Devices:** `{len(devices)}` / `50` Max Limit")
else:
    st.info("No computers connected yet. Download the installer above to connect your first computer!")
