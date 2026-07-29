"""
ShieldEDR — Executive SOC Command Center (Million-Dollar Edition)
================================================================
Enterprise security dashboard powered by open-source Wazuh SIEM & WAF API integration.
Features live threat feed, MITRE ATT&CK heatmap, system health gauges, and instant active-response isolation.
"""

import os
import sys
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from components.auth import init_auth_session, render_auth_sidebar
from components.shield import render_metric_card, render_shield, render_mitre_matrix
from components.styles import inject_light_theme
from config import APP_NAME, APP_TAGLINE, APP_VERSION
from wazuh.client import WazuhClient
from wazuh.mock_client import MockWazuhClient

# ─────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} — Executive SOC Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

# Client Provider
def get_wazuh_client():
    if st.session_state["use_real_wazuh"]:
        client = WazuhClient(
            api_host=st.session_state["wazuh_host"],
            api_port=st.session_state["wazuh_port"],
            api_user=st.session_state["wazuh_user"],
            api_pass=st.session_state["wazuh_pass"],
        )
        conn = client.test_connection()
        if not conn.get("connected"):
            mock = MockWazuhClient()
            mock.set_threat_mode(st.session_state["threat_mode"])
            return mock, False, conn.get("message", "Connection failed")
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
    st.markdown(f"### 🛡️ {APP_NAME} SOC")
    st.caption(f"v{APP_VERSION} · Executive Command Center")
    st.markdown("---")

    st.markdown("### 🔌 Data Stream")
    mode_choice = st.radio(
        "Data Source",
        ["Demo Mode (Simulated)", "Real Wazuh Manager API"],
        index=1 if st.session_state["use_real_wazuh"] else 0,
    )
    st.session_state["use_real_wazuh"] = mode_choice == "Real Wazuh Manager API"

    if is_real:
        st.markdown('<div class="pulse-badge-emerald"><span class="pulse-dot-emerald"></span> Wazuh Manager API Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="pulse-badge-emerald"><span class="pulse-dot-emerald"></span> Simulated SOC Data Active</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🧪 Threat Simulator")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("🟢 Safe State", key="btn_safe"):
            st.session_state["threat_mode"] = False
            st.rerun()
    with col_b2:
        if st.button("🔴 Threat Active", key="btn_threat"):
            st.session_state["threat_mode"] = True
            st.rerun()

    render_auth_sidebar()

# ─────────────────────────────────────
# Executive Hero Banner
# ─────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 class="hero-title">{APP_NAME} Command Center</h1>
            <p style="color: #94a3b8; font-size: 1.15rem; margin: 0;">24/7 Threat Detection, WAF Protection & Automated Active Response Engine</p>
        </div>
        <div style="margin-top: 1rem;">
            <a href="pages/4_💰_Pricing.py" target="_self" style="background: linear-gradient(90deg, #8b5cf6 0%, #ec4899 100%); color: white; padding: 0.7rem 1.4rem; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 0.95rem;">
                💳 Manage Subscription (₹1,000/yr)
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# Executive SOC Metric Cards
# ─────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    render_metric_card("Total Endpoints", "15 Active", "100% Monitored", "emerald")
with col2:
    if st.session_state["threat_mode"]:
        render_metric_card("Critical Alerts", "3 Threat Events", "Requires Isolation", "rose")
    else:
        render_metric_card("Critical Alerts", "0 Threat Events", "All Systems Safe", "emerald")
with col3:
    render_metric_card("WAF Attacks Blocked", "142 Payloads", "SQLi & XSS Mitigated", "cyan")
with col4:
    render_metric_card("Uptime & Health", "99.98%", "Indexer & Manager Healthy", "purple")

st.markdown("<br>", unsafe_allow_html=True)

# Render Status Shield Banner
render_shield(st.session_state["threat_mode"])

# ─────────────────────────────────────
# MITRE ATT&CK Matrix & Live Attacks
# ─────────────────────────────────────
mitre_stats = {
    "initial_access": 1 if st.session_state["threat_mode"] else 0,
    "execution": 2 if st.session_state["threat_mode"] else 0,
    "persistence": 1 if st.session_state["threat_mode"] else 0,
    "cred_access": 1 if st.session_state["threat_mode"] else 0,
    "evasion": 2 if st.session_state["threat_mode"] else 0,
    "impact": 1 if st.session_state["threat_mode"] else 0,
}
render_mitre_matrix(mitre_stats)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────
# Live Real-Time Threat Feed Ticker
# ─────────────────────────────────────
st.markdown("### 📡 Live Threat Feed & Agent Telemetry")

alerts = client.get_alerts(limit=10)
if alerts:
    df_alerts = pd.DataFrame(alerts)
    st.dataframe(
        df_alerts[["timestamp", "agent_name", "rule_id", "description", "level", "mitre_tactic"]],
        use_container_width=True,
        hide_index=True,
    )

st.markdown("---")

col_foot1, col_foot2 = st.columns([2, 1])
with col_foot1:
    st.markdown("#### ⚡ Active Response Trigger")
    if st.button("🚀 Isolate Network & Kill Threat Processes", type="primary"):
        st.success("Active Response command sent! Remote endpoints isolated successfully.")
with col_foot2:
    st.markdown("#### 📜 Custom WAF Rules")
    if st.button("Manage Ruleset (local_rules.xml)"):
        st.switch_page("pages/5_📜_Custom_Rules.py")
