"""
ShieldEDR — Endpoint Management Page
====================================
Manage monitored endpoints, view detailed telemetry, restart agents, or trigger active response.
"""

import os
import sys
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from components.styles import inject_light_theme
from wazuh.client import WazuhClient
from wazuh.mock_client import MockWazuhClient

st.set_page_config(page_title="Endpoints — ShieldEDR", page_icon="💻", layout="wide")
inject_light_theme()


def get_client():
    if st.session_state.get("use_real_wazuh"):
        return WazuhClient(
            api_host=st.session_state.get("wazuh_host", "localhost"),
            api_port=st.session_state.get("wazuh_port", 55000),
            api_user=st.session_state.get("wazuh_user", "wazuh-wui"),
            api_pass=st.session_state.get("wazuh_pass", "wazuh-wui"),
        )
    mock = MockWazuhClient()
    mock.set_threat_mode(st.session_state.get("threat_mode", False))
    return mock


client = get_client()

st.markdown("""
<div class="hero-header">
    <h1>💻 Endpoint Fleet Management</h1>
    <p>Monitor, inspect, and execute active response on all registered agents across your organization</p>
</div>
""", unsafe_allow_html=True)

agents = client.get_agents().get("data", {}).get("affected_items", [])

col_filter1, col_filter2 = st.columns([2, 1])
with col_filter1:
    search_query = st.text_input("🔍 Search agents by name, IP, or OS", "")
with col_filter2:
    status_filter = st.selectbox("Status Filter", ["All", "active", "disconnected"])

# Filter agents
filtered = agents
if status_filter != "All":
    filtered = [a for a in filtered if a.get("status") == status_filter]
if search_query:
    q = search_query.lower()
    filtered = [
        a for a in filtered
        if q in a.get("name", "").lower()
        or q in a.get("ip", "").lower()
        or q in a.get("os", {}).get("name", "").lower()
    ]

st.markdown(f'<div class="section-header">Registered Endpoints ({len(filtered)})</div>', unsafe_allow_html=True)

if filtered:
    for ag in filtered:
        ag_id = ag.get("id")
        ag_name = ag.get("name")
        ag_ip = ag.get("ip")
        ag_os = f"{ag.get('os', {}).get('name', 'N/A')} {ag.get('os', {}).get('version', '')}"
        ag_status = ag.get("status")

        status_pill = (
            '<span class="status-pill active">Active</span>' if ag_status == "active"
            else '<span class="status-pill offline">Offline</span>'
        )

        with st.expander(f"🖥️ {ag_name} — {ag_ip} | ID: {ag_id}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Agent ID:** `{ag_id}`")
                st.markdown(f"**Host Name:** `{ag_name}`")
                st.markdown(f"**IP Address:** `{ag_ip}`")
            with c2:
                st.markdown(f"**Operating System:** {ag_os}")
                st.markdown(f"**Wazuh Version:** `{ag.get('version', 'N/A')}`")
                st.markdown(f"**Status:** {status_pill}", unsafe_allow_html=True)
            with c3:
                st.markdown("**Actions:**")
                ac1, ac2 = st.columns(2)
                with ac1:
                    if st.button("🔄 Restart Agent", key=f"restart_{ag_id}"):
                        res = client.restart_agent(ag_id)
                        st.success(f"Restart command sent to {ag_name}.")
                with ac2:
                    if st.button("🛡️ Run FIM Scan", key=f"fim_{ag_id}"):
                        client.run_fim_scan(ag_id)
                        st.success(f"FIM scan triggered on {ag_name}.")

            # Sub-tabs for detailed host data
            subtab1, subtab2, subtab3 = st.tabs(["Vulnerabilities", "FIM Events", "SCA Benchmark"])
            with subtab1:
                vulns = client.get_agent_vulnerabilities(ag_id).get("data", {}).get("affected_items", [])
                if vulns:
                    v_df = pd.DataFrame([
                        {
                            "CVE": v.get("cve"),
                            "Title": v.get("name"),
                            "Severity": v.get("severity"),
                            "Status": v.get("status"),
                            "Package": v.get("package", {}).get("name"),
                        }
                        for v in vulns
                    ])
                    st.dataframe(v_df, use_container_width=True)
                else:
                    st.info("No vulnerabilities detected on this host.")

            with subtab2:
                fim_ev = client.get_fim_events(ag_id).get("data", {}).get("affected_items", [])
                if fim_ev:
                    st.dataframe(pd.DataFrame(fim_ev), use_container_width=True)
                else:
                    st.info("No recent file integrity changes.")

            with subtab3:
                sca = client.get_sca_results(ag_id).get("data", {}).get("affected_items", [])
                if sca:
                    st.dataframe(pd.DataFrame(sca), use_container_width=True)
                else:
                    st.info("SCA assessment not performed yet.")
else:
    st.info("No endpoints match the current filter criteria.")
