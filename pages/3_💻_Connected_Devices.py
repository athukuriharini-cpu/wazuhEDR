"""
3_💻_Connected_Devices.py - Streamlit page showing connected EDR endpoint agents.
"""

import os
import sys

# Sys path manipulation to import test_data from parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import test_data

# Page Configuration
st.set_page_config(
    page_title="Connected Devices & Agents - EDR Dashboard",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Dark Theme, Glassmorphism, Status Badges with Glow, Card Layouts
st.markdown(
    """
    <style>
    /* Main Background & Fonts */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0b0f19 100%);
        color: #f3f4f6;
    }
    
    /* Summary Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Custom Device Cards */
    .device-card {
        background: rgba(17, 24, 39, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .device-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.45), 0 0 20px rgba(99, 102, 241, 0.15);
    }
    
    /* Glowing Status Badges */
    .status-badge-online {
        background: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.3);
    }
    
    .status-badge-offline {
        background: rgba(239, 68, 68, 0.12);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.35);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.3);
    }
    
    .status-dot-online {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10b981;
        display: inline-block;
    }
    
    .status-dot-offline {
        width: 8px;
        height: 8px;
        background-color: #ef4444;
        border-radius: 50%;
        box-shadow: 0 0 8px #ef4444;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main Header
st.title("💻 Connected Devices & Agents")
st.markdown("Monitor endpoint health, view registered security agents, and deploy new endpoints across your network.")

st.divider()

# Maintain agent data in session state for consistency
if "agent_list" not in st.session_state:
    st.session_state.agent_list = test_data.generate_agent_list(count=9)

# Action / Controls Bar
ctl_col1, ctl_col2, ctl_col3 = st.columns([3, 2, 1])
with ctl_col1:
    search_query = st.text_input("🔍 Search agents by hostname or IP:", placeholder="e.g. MSME-PC-01 or 192.168...")
with ctl_col2:
    status_filter = st.selectbox("Filter Status:", ["All Statuses", "Online Only", "Offline Only"])
with ctl_col3:
    st.write(" ")
    st.write(" ")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.agent_list = test_data.generate_agent_list(count=9)
        st.rerun()

agents = st.session_state.agent_list

# Filter agents according to controls
filtered_agents = agents
if search_query:
    filtered_agents = [
        a for a in filtered_agents
        if search_query.lower() in a["hostname"].lower() or search_query.lower() in a["ip_address"].lower()
    ]
if status_filter == "Online Only":
    filtered_agents = [a for a in filtered_agents if a["status"] == "online"]
elif status_filter == "Offline Only":
    filtered_agents = [a for a in filtered_agents if a["status"] == "offline"]

# Metrics summary calculation (using total fleet)
total_agents = len(agents)
online_agents = sum(1 for a in agents if a["status"] == "online")
offline_agents = sum(1 for a in agents if a["status"] == "offline")
threats_detected = sum(a["threats_detected"] for a in agents)

# Summary Metrics Row
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="Total Agents", value=total_agents, delta="Registered Fleet")
with m2:
    st.metric(label="Online", value=online_agents, delta=f"{round((online_agents/total_agents)*100)}% Active" if total_agents else "0%")
with m3:
    st.metric(label="Offline", value=offline_agents, delta=f"-{offline_agents}" if offline_agents > 0 else "0", delta_color="inverse")
with m4:
    st.metric(label="Threats Detected", value=threats_detected, delta="Requires Attention" if threats_detected > 0 else "Clean", delta_color="inverse" if threats_detected > 0 else "normal")

st.markdown("<br>", unsafe_allow_html=True)

# Helper function to assign OS icons
def get_os_icon(os_name: str) -> str:
    if "Windows" in os_name:
        return "🪟"
    elif "macOS" in os_name or "Mac" in os_name:
        return "🍎"
    elif "Ubuntu" in os_name or "Linux" in os_name:
        return "🐧"
    return "💻"

# Tabbed Display: Styled Dataframe vs Responsive Card Grid
view_tab1, view_tab2 = st.tabs(["📊 Agent Data Table", "🎴 Device Card Grid"])

with view_tab1:
    st.subheader("Agent Roster")
    if not filtered_agents:
        st.info("No agents match your filter criteria.")
    else:
        table_rows = []
        for a in filtered_agents:
            os_icon = get_os_icon(a["os"])
            status_badge = "🟢 Online" if a["status"] == "online" else "🔴 Offline"
            table_rows.append({
                "Hostname": a["hostname"],
                "OS": f"{os_icon} {a['os']}",
                "IP Address": a["ip_address"],
                "Status": status_badge,
                "Last Seen": a["last_seen"],
                "Agent Version": a["agent_version"],
                "Threats Detected": a["threats_detected"],
            })
        
        df = pd.DataFrame(table_rows)

        def color_status(val):
            if "Online" in str(val):
                return 'background-color: rgba(16, 185, 129, 0.2); color: #10b981; font-weight: bold;'
            elif "Offline" in str(val):
                return 'background-color: rgba(239, 68, 68, 0.2); color: #ef4444; font-weight: bold;'
            return ''

        # Handle compatibility for pandas style map / applymap
        if hasattr(df.style, 'map'):
            styled_df = df.style.map(color_status, subset=['Status'])
        else:
            styled_df = df.style.applymap(color_status, subset=['Status'])

        st.dataframe(
            styled_df,
            use_container_width=True,
            column_config={
                "Hostname": st.column_config.TextColumn("Hostname", help="Device name"),
                "OS": st.column_config.TextColumn("Operating System"),
                "IP Address": st.column_config.TextColumn("IP Address"),
                "Status": st.column_config.TextColumn("Agent Status"),
                "Last Seen": st.column_config.TextColumn("Last Heartbeat"),
                "Agent Version": st.column_config.TextColumn("Version"),
                "Threats Detected": st.column_config.NumberColumn("Threats", format="%d 🛡️"),
            },
            hide_index=True,
        )

with view_tab2:
    st.subheader("Device Cards")
    if not filtered_agents:
        st.info("No agents match your filter criteria.")
    else:
        cols_per_row = 3
        for i in range(0, len(filtered_agents), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(filtered_agents):
                    agent = filtered_agents[i + j]
                    is_online = agent["status"] == "online"
                    os_icon = get_os_icon(agent["os"])
                    badge_class = "status-badge-online" if is_online else "status-badge-offline"
                    dot_class = "status-dot-online" if is_online else "status-dot-offline"
                    status_lbl = "ONLINE" if is_online else "OFFLINE"
                    threat_style = "color: #ef4444; font-weight: bold;" if agent["threats_detected"] > 0 else "color: #10b981;"

                    with col:
                        st.markdown(
                            f"""
                            <div class="device-card">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                    <div style="font-size: 1.1rem; font-weight: 700; color: #f9fafb; display: flex; align-items: center; gap: 8px;">
                                        <span style="font-size: 1.3rem;">{os_icon}</span> {agent['hostname']}
                                    </div>
                                    <div class="{badge_class}">
                                        <span class="{dot_class}"></span> {status_lbl}
                                    </div>
                                </div>
                                <div style="font-size: 0.88rem; color: #9ca3af; line-height: 1.8;">
                                    <div><strong>OS:</strong> {agent['os']}</div>
                                    <div><strong>IP Address:</strong> <code style="background: rgba(31, 41, 55, 0.8); padding: 2px 6px; border-radius: 4px; color: #38bdf8;">{agent['ip_address']}</code></div>
                                    <div><strong>Last Seen:</strong> {agent['last_seen']}</div>
                                    <div><strong>Agent Version:</strong> {agent['agent_version']}</div>
                                    <div><strong>Threats Detected:</strong> <span style="{threat_style}">{agent['threats_detected']}</span></div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# Deploy New Agent Section
st.subheader("🚀 Deploy New Agent")
st.markdown("Deploy the EDR agent to new devices across your organization using the one-line installation command below.")

commands = {
    "Windows": 'powershell -Command "irm https://shield-edr.io/install.ps1 | iex"',
    "macOS": "curl -sSL https://shield-edr.io/install.sh | bash",
    "Linux": "wget -qO- https://shield-edr.io/install.sh | sudo bash",
}

tab_win, tab_mac, tab_linux = st.tabs(["🪟 Windows", "🍎 macOS", "🐧 Linux"])

with tab_win:
    st.markdown("##### 🪟 Windows Installation (PowerShell)")
    st.caption("Run the following command in an elevated PowerShell prompt:")
    c1, c2 = st.columns([5, 1])
    with c1:
        st.code(commands["Windows"], language="powershell")
    with c2:
        st.write(" ")
        if st.button("📋 Copy Command", key="copy_win"):
            st.toast("Windows install command copied!")
            components.html(
                f"<script>navigator.clipboard.writeText('{commands['Windows']}');</script>",
                height=0,
            )

with tab_mac:
    st.markdown("##### 🍎 macOS Installation (Terminal)")
    st.caption("Run the following command in macOS Terminal:")
    c1, c2 = st.columns([5, 1])
    with c1:
        st.code(commands["macOS"], language="bash")
    with c2:
        st.write(" ")
        if st.button("📋 Copy Command", key="copy_mac"):
            st.toast("macOS install command copied!")
            components.html(
                f"<script>navigator.clipboard.writeText('{commands['macOS']}');</script>",
                height=0,
            )

with tab_linux:
    st.markdown("##### 🐧 Linux Installation (Bash)")
    st.caption("Run the following command with sudo privileges:")
    c1, c2 = st.columns([5, 1])
    with c1:
        st.code(commands["Linux"], language="bash")
    with c2:
        st.write(" ")
        if st.button("📋 Copy Command", key="copy_linux"):
            st.toast("Linux install command copied!")
            components.html(
                f"<script>navigator.clipboard.writeText('{commands['Linux']}');</script>",
                height=0,
            )

st.info("💡 **Note:** Agent will auto-register to your dashboard upon successful installation.")
