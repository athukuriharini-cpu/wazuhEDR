"""
ShieldEDR — Main Application Entry Point
=========================================
Light-mode EDR Dashboard powered by open-source Wazuh API integration.
"""

import os
import sys
import pandas as pd
import streamlit as st

# Ensure workspace root is in python path
sys.path.insert(0, os.path.dirname(__file__))

from components.auth import init_auth_session, render_auth_sidebar
from components.shield import render_metric_card, render_shield
from components.styles import inject_light_theme
from config import APP_NAME, APP_TAGLINE, APP_VERSION
from wazuh.client import WazuhClient
from wazuh.mock_client import MockWazuhClient

# ─────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} — Enterprise Security Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Premium Light Mode Styles
inject_light_theme()
init_auth_session()

# ─────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────
if "threat_mode" not in st.session_state:
    st.session_state["threat_mode"] = False

if "use_real_wazuh" not in st.session_state:
    st.session_state["use_real_wazuh"] = False

if "wazuh_host" not in st.session_state:
    st.session_state["wazuh_host"] = "localhost"

if "wazuh_port" not in st.session_state:
    st.session_state["wazuh_port"] = 55000

if "wazuh_user" not in st.session_state:
    st.session_state["wazuh_user"] = "wazuh-wui"

if "wazuh_pass" not in st.session_state:
    st.session_state["wazuh_pass"] = "wazuh-wui"


# ─────────────────────────────────────
# Client Provider
# ─────────────────────────────────────
def get_wazuh_client():
    """Get either real or mock Wazuh client based on user toggle."""
    if st.session_state["use_real_wazuh"]:
        client = WazuhClient(
            api_host=st.session_state["wazuh_host"],
            api_port=st.session_state["wazuh_port"],
            api_user=st.session_state["wazuh_user"],
            api_pass=st.session_state["wazuh_pass"],
        )
        # Test connection
        conn = client.test_connection()
        if not conn.get("connected"):
            st.session_state["wazuh_connected"] = False
            # Fall back to mock client with warning
            mock = MockWazuhClient()
            mock.set_threat_mode(st.session_state["threat_mode"])
            return mock, False, conn.get("message", "Connection failed")
        st.session_state["wazuh_connected"] = True
        return client, True, "Connected to Wazuh Manager"
    else:
        mock = MockWazuhClient()
        mock.set_threat_mode(st.session_state["threat_mode"])
        return mock, False, "Demo Mode (Mock Wazuh Data)"


client, is_real, conn_msg = get_wazuh_client()

# ─────────────────────────────────────
# Sidebar
# ─────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 🛡️ {APP_NAME}")
    st.caption(f"v{APP_VERSION} · {APP_TAGLINE}")
    st.markdown("---")

    # Connection Mode Indicator
    st.markdown("### 🔌 Connection Mode")
    mode_choice = st.radio(
        "Data Source",
        ["Demo Mode (Simulated)", "Real Wazuh Manager API"],
        index=1 if st.session_state["use_real_wazuh"] else 0,
        help="Switch between simulated test data and a real Wazuh Manager REST API.",
    )
    st.session_state["use_real_wazuh"] = mode_choice == "Real Wazuh Manager API"

    if is_real:
        st.markdown(
            '<div class="conn-status"><span class="conn-dot online"></span> Connected to Wazuh API</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="conn-status"><span class="conn-dot demo"></span> Demo Mode Active</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Interactive Simulation Controls
    st.markdown("### 🧪 Threat Simulation")
    st.caption("Test how the screen reacts to threats:")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🟢 Safe State", key="btn_safe_mode", help="Set network state to Safe (All Clear)"):
            st.session_state["threat_mode"] = False
            st.rerun()

    with col_btn2:
        if st.button("🔴 Threat Mode", key="btn_threat_mode", help="Simulate a virus/ransomware threat"):
            st.session_state["threat_mode"] = True
            st.rerun()

    current_status = "🔴 Threat Active" if st.session_state["threat_mode"] else "🟢 All Clear"
    st.info(f"Current State: **{current_status}**")

    st.markdown("---")
    st.markdown("### 📦 Quick Agent Deploy")
    st.code("msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER=\"10.0.0.2\"", language="powershell")
    st.caption("Single-command deployment for Windows endpoints.")

    # Render User Account Auth Panel
    render_auth_sidebar()

# ─────────────────────────────────────
# Hero Header
# ─────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
    <h1>🛡️ {APP_NAME} EDR Command Center</h1>
    <p>Real-time endpoint detection, threat response, and compliance powered by Wazuh Open Source Security</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# Main Shield Status Display
# ─────────────────────────────────────
alerts = client.get_alerts(severity_min=7, limit=50)
critical_threats = [a for a in alerts if a.get("rule", {}).get("level", 0) >= 10]
is_threat_active = len(critical_threats) > 0 or st.session_state["threat_mode"]

render_shield(is_threat=is_threat_active, threat_count=max(len(critical_threats), 1 if st.session_state["threat_mode"] else 0))

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────
# Bento Grid Metrics
# ─────────────────────────────────────
agent_summary = client.get_agent_summary().get("data", {})
total_agents = agent_summary.get("total", 0)
active_agents = agent_summary.get("active", 0)
disconnected_agents = agent_summary.get("disconnected", 0)

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_metric_card(str(total_agents), "Total Endpoints", color="primary")

with col2:
    render_metric_card(str(active_agents), "Active & Monitored", color="success")

with col3:
    render_metric_card(str(disconnected_agents), "Offline / Disconnected", color="warning" if disconnected_agents > 0 else "")

with col4:
    threat_val = str(len(alerts))
    render_metric_card(threat_val, "Security Events (24h)", color="danger" if is_threat_active else "")

# ─────────────────────────────────────
# Interactive Dashboard Tabs
# ─────────────────────────────────────
tab1, tab2, tab3 = st.columns([1, 1, 1])

st.markdown('<div class="section-header">📋 Security Activity & Telemetry</div>', unsafe_allow_html=True)

tab_alerts, tab_endpoints, tab_health = st.tabs([
    "🚨 Live Alert Stream",
    "💻 Endpoint Health",
    "⚙️ Wazuh Engine Status",
])

# ── Tab 1: Alerts ──
with tab_alerts:
    if alerts:
        alert_rows = []
        for a in alerts:
            rule = a.get("rule", {})
            agent = a.get("agent", {})
            level = rule.get("level", 0)

            status_pill = (
                f'<span class="status-pill critical">Level {level}</span>' if level >= 12 else
                f'<span class="status-pill high">Level {level}</span>' if level >= 10 else
                f'<span class="status-pill medium">Level {level}</span>' if level >= 7 else
                f'<span class="status-pill info">Level {level}</span>'
            )

            alert_rows.append({
                "Timestamp": a.get("timestamp", "")[:19].replace("T", " "),
                "Agent": f"{agent.get('name', 'Unknown')} ({agent.get('ip', 'N/A')})",
                "Severity": status_pill,
                "Description": rule.get("description", "No details"),
                "Rule ID": rule.get("id", "N/A"),
            })

        df_alerts = pd.DataFrame(alert_rows)
        st.write(
            df_alerts.to_html(escape=False, index=False, classes="clean-table"),
            unsafe_allow_html=True,
        )
    else:
        st.success("No active high-severity security alerts detected.")

# ── Tab 2: Endpoints ──
with tab_endpoints:
    agents_data = client.get_agents().get("data", {}).get("affected_items", [])
    if agents_data:
        agent_rows = []
        for ag in agents_data:
            st_val = ag.get("status", "unknown")
            pill = (
                '<span class="status-pill active">Active</span>' if st_val == "active" else
                '<span class="status-pill offline">Offline</span>'
            )
            agent_rows.append({
                "ID": ag.get("id"),
                "Name": ag.get("name"),
                "IP Address": ag.get("ip"),
                "OS": f"{ag.get('os', {}).get('name', '')} {ag.get('os', {}).get('version', '')}",
                "Status": pill,
                "Version": ag.get("version"),
            })
        df_ag = pd.DataFrame(agent_rows)
        st.write(
            df_ag.to_html(escape=False, index=False, classes="clean-table"),
            unsafe_allow_html=True,
        )
    else:
        st.info("No endpoints registered yet.")

# ── Tab 3: Manager Health ──
with tab_health:
    mgr_status = client.get_manager_status().get("data", {}).get("affected_items", [{}])[0]
    if mgr_status:
        st.markdown("**Wazuh Manager Services:**")
        cols = st.columns(3)
        idx = 0
        for daemon, d_status in mgr_status.items():
            with cols[idx % 3]:
                d_color = "🟢" if d_status == "running" else "🔴"
                st.markdown(f"- {d_color} **{daemon}**: `{d_status}`")
            idx += 1
    else:
        st.info("Manager status information unavailable in current mode.")

# ─────────────────────────────────────
# Footer
# ─────────────────────────────────────
st.markdown(f"""
<div class="app-footer">
    {APP_NAME} v{APP_VERSION} · Powered by <a href="https://wazuh.com" target="_blank">Wazuh Open Source EDR</a> · Designed in Light Theme
</div>
""", unsafe_allow_html=True)
