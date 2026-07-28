"""
ShieldEDR — Security Reports & Analytics Page
=============================================
Detailed analytics for vulnerabilities, FIM changes, and compliance checks.
"""

import os
import sys
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from components.styles import inject_light_theme
from wazuh.client import WazuhClient
from wazuh.mock_client import MockWazuhClient

st.set_page_config(page_title="Security Reports — ShieldEDR", page_icon="📊", layout="wide")
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
    <h1>📊 Security Analytics & Reports</h1>
    <p>Comprehensive vulnerability reports, file integrity logs, and CIS compliance benchmarks</p>
</div>
""", unsafe_allow_html=True)

report_type = st.selectbox(
    "Select Report Type",
    ["Vulnerability Analysis (CVE)", "File Integrity Monitoring (FIM)", "Security Configuration Assessment (SCA)", "Wazuh Detection Rules"],
)

if report_type == "Vulnerability Analysis (CVE)":
    st.markdown('<div class="section-header">CVE Vulnerability Summary</div>', unsafe_allow_html=True)
    vulns = client.get_agent_vulnerabilities("001").get("data", {}).get("affected_items", [])

    if vulns:
        c1, c2, c3 = st.columns(3)
        crit = sum(1 for v in vulns if v.get("severity") == "Critical")
        high = sum(1 for v in vulns if v.get("severity") == "High")
        active = sum(1 for v in vulns if v.get("status") == "Active")

        with c1:
            st.metric("Critical CVEs", crit)
        with c2:
            st.metric("High CVEs", high)
        with c3:
            st.metric("Active Unpatched", active)

        st.markdown("<br>", unsafe_allow_html=True)
        v_df = pd.DataFrame([
            {
                "CVE ID": v.get("cve"),
                "Vulnerability Name": v.get("name"),
                "Severity": v.get("severity"),
                "Status": v.get("status"),
                "Package": v.get("package", {}).get("name"),
                "Detected": v.get("detection_time", "")[:10],
            }
            for v in vulns
        ])
        st.dataframe(v_df, use_container_width=True)
    else:
        st.info("No vulnerabilities recorded.")

elif report_type == "File Integrity Monitoring (FIM)":
    st.markdown('<div class="section-header">File Integrity Audit Trail</div>', unsafe_allow_html=True)
    fim_data = client.get_fim_events("001").get("data", {}).get("affected_items", [])
    if fim_data:
        st.dataframe(pd.DataFrame(fim_data), use_container_width=True)

elif report_type == "Security Configuration Assessment (SCA)":
    st.markdown('<div class="section-header">CIS Benchmark SCA Scores</div>', unsafe_allow_html=True)
    sca_data = client.get_sca_results("001").get("data", {}).get("affected_items", [])
    if sca_data:
        st.dataframe(pd.DataFrame(sca_data), use_container_width=True)

elif report_type == "Wazuh Detection Rules":
    st.markdown('<div class="section-header">Active Wazuh Rule Set</div>', unsafe_allow_html=True)
    rules = client.get_rules(limit=50).get("data", {}).get("affected_items", [])
    if rules:
        r_df = pd.DataFrame([
            {
                "Rule ID": r.get("id"),
                "Level": r.get("level"),
                "Description": r.get("description"),
                "Groups": ", ".join(r.get("groups", [])),
            }
            for r in rules
        ])
        st.dataframe(r_df, use_container_width=True)
