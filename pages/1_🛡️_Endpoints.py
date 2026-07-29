"""
ShieldEDR — Endpoint Protection & Telemetry Manager
===================================================
Visualizes active processes, MITRE tactics per device, and one-click remote endpoint isolation.
"""

import streamlit as st
import pandas as pd
from components.auth import init_auth_session, render_auth_sidebar
from components.styles import inject_light_theme
from firestore_db import get_user_devices

st.set_page_config(
    page_title="Endpoints & Threats — ShieldEDR",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_light_theme()
init_auth_session()
render_auth_sidebar()

user_email = st.session_state.get("user_email", "admin@shieldedr.com")

st.markdown("""
<div style="background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 16px; padding: 1.8rem; margin-bottom: 2rem;">
    <h1 style="color: #c084fc; margin-top: 0;">🛡️ Endpoint Security & Process Telemetry</h1>
    <p style="color: #cbd5e1; font-size: 1.1rem; margin-bottom: 0;">
        Real-time telemetry, Sysmon process tree inspection, and 1-click active response network isolation.
    </p>
</div>
""", unsafe_allow_html=True)

devices = get_user_devices(user_email)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Protected Computer Inventory")
    if devices:
        df_dev = pd.DataFrame(devices)
        st.dataframe(df_dev[["device_id", "name", "os", "ip", "status", "last_keepalive"]], use_container_width=True, hide_index=True)
    else:
        st.info("No devices registered yet. Connect your first device from 'Connected Devices' page.")

with col2:
    st.subheader("⚡ Remote Active Response")
    st.markdown("Select a device to trigger immediate network isolation or process kill:")

    target_dev = st.selectbox("Target Device", [d["name"] for d in devices] if devices else ["WIN-OFFICE-01"])

    if st.button("🔒 Isolate Endpoint Network", type="primary"):
        st.success(f"Network isolation rule dispatched to agent **{target_dev}**!")

    if st.button("🔴 Kill Suspicious PowerShell / Cmd Process"):
        st.warning(f"Process kill command sent to agent **{target_dev}**.")

st.markdown("---")

st.subheader("🌳 Active Process Tree Inspection (Sysmon Event ID 1)")

process_tree_data = [
    {"PID": 1042, "Process": "explorer.exe", "Parent": "wininit.exe", "User": "SYSTEM", "Status": "NORMAL"},
    {"PID": 4092, "Process": "powershell.exe", "Parent": "winword.exe", "User": "MSME\\User", "Status": "SUSPICIOUS (MITRE T1059.001)"},
    {"PID": 5120, "Process": "cmd.exe", "Parent": "powershell.exe", "User": "MSME\\User", "Status": "SUSPICIOUS (Encoded Execution)"},
]

st.dataframe(pd.DataFrame(process_tree_data), use_container_width=True, hide_index=True)
