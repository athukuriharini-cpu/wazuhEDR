"""
ShieldEDR — Wazuh Connection Settings Page
===========================================
Configure connection parameters to an open-source Wazuh Manager REST API and Indexer.
"""

import os
import sys
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from components.styles import inject_light_theme
from wazuh.client import WazuhClient

st.set_page_config(page_title="Wazuh Settings — ShieldEDR", page_icon="⚙️", layout="wide")
inject_light_theme()

st.markdown("""
<div class="hero-header">
    <h1>⚙️ Wazuh Integration Settings</h1>
    <p>Configure credentials and connection parameters for your open-source Wazuh EDR Manager</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-header">Wazuh Manager API Credentials (Port 55000)</div>', unsafe_allow_html=True)

with st.form("wazuh_config_form"):
    c1, c2 = st.columns(2)
    with c1:
        w_host = st.text_input(
            "Wazuh Manager Host / IP",
            value=st.session_state.get("wazuh_host", "localhost"),
            help="IP address or domain of the Wazuh Manager instance.",
        )
        w_user = st.text_input(
            "API Username",
            value=st.session_state.get("wazuh_user", "wazuh-wui"),
            help="Default API user is 'wazuh-wui' or 'wazuh'.",
        )

    with c2:
        w_port = st.number_input(
            "API Port",
            value=int(st.session_state.get("wazuh_port", 55000)),
            min_value=1,
            max_value=65535,
        )
        w_pass = st.text_input(
            "API Password",
            value=st.session_state.get("wazuh_pass", "wazuh-wui"),
            type="password",
        )

    submitted = st.form_submit_button("🔌 Test Connection & Save")

if submitted:
    st.session_state["wazuh_host"] = w_host
    st.session_state["wazuh_port"] = w_port
    st.session_state["wazuh_user"] = w_user
    st.session_state["wazuh_pass"] = w_pass

    client = WazuhClient(
        api_host=w_host,
        api_port=w_port,
        api_user=w_user,
        api_pass=w_pass,
    )

    with st.spinner("Authenticating with Wazuh REST API..."):
        test_res = client.test_connection()

    if test_res.get("connected"):
        st.success(f"✅ Connection successful! Manager Version: {test_res.get('version')}")
        st.session_state["use_real_wazuh"] = True
    else:
        st.error(f"❌ Connection failed: {test_res.get('message')}")
        st.info("Ensure the Wazuh Manager service is running and port 55000 is open.")

st.markdown('<div class="section-header">Wazuh Architecture Info</div>', unsafe_allow_html=True)
st.markdown("""
- **REST API Port**: `55000` (HTTPS)
- **Indexer / Alerts Port**: `9200` (HTTPS)
- **Agent Communication Port**: `1514` (UDP/TCP)
- **Enrollment Port**: `1515` (TCP)
""")
