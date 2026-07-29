"""
ShieldEDR Executive SOC Dashboard Components
==============================================
Provides high-end metric cards, visual threat shields, MITRE tactic heatmaps,
and live attack feed tickers.
"""

import streamlit as st

def render_metric_card(title: str, value: str, delta: str = None, color: str = "purple"):
    """Renders a sleek executive glassmorphism metric card."""
    border_colors = {
        "purple": "rgba(168, 85, 247, 0.35)",
        "emerald": "rgba(16, 185, 129, 0.35)",
        "cyan": "rgba(6, 182, 212, 0.35)",
        "rose": "rgba(244, 63, 94, 0.35)",
        "amber": "rgba(245, 158, 11, 0.35)",
    }
    glow_color = border_colors.get(color, border_colors["purple"])

    delta_html = ""
    if delta:
        is_pos = "+" in delta or "up" in delta.lower() or "active" in delta.lower()
        delta_color = "#34d399" if is_pos else "#fb7185"
        delta_html = f'<div style="font-size: 0.82rem; color: {delta_color}; font-weight: 600; margin-top: 0.4rem;">{delta}</div>'

    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid {glow_color}; border-radius: 16px; padding: 1.3rem; backdrop-filter: blur(16px); box-shadow: 0 10px 25px -10px rgba(0, 0, 0, 0.5);">
        <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{title}</div>
        <div style="font-size: 2.2rem; font-weight: 900; color: #f8fafc; margin-top: 0.2rem; letter-spacing: -0.02em;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def render_shield(is_threat_mode: bool = False):
    """Renders executive SOC status banner."""
    if is_threat_mode:
        st.markdown("""
        <div class="glass-card" style="border-color: rgba(244, 63, 94, 0.6) !important; background: rgba(244, 63, 94, 0.08) !important;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <div class="pulse-badge-rose"><span class="pulse-dot-rose"></span> 🚨 CRITICAL THREAT DETECTED</div>
                    <h2 style="color: #fb7185; margin: 0.5rem 0 0.2rem 0; font-weight: 900;">Ransomware / Encoded Execution Triggered</h2>
                    <p style="color: #cbd5e1; margin: 0; font-size: 0.95rem;">Active Response Engine is isolating infected process trees and blocking egress network connections.</p>
                </div>
                <div style="background: rgba(244, 63, 94, 0.2); padding: 0.8rem 1.4rem; border-radius: 12px; border: 1px solid rgba(244, 63, 94, 0.4); text-align: center;">
                    <span style="font-size: 0.8rem; color: #fca5a5; font-weight: bold;">SEVERITY</span>
                    <div style="font-size: 1.6rem; font-weight: 900; color: #ffffff;">LEVEL 14</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="border-color: rgba(16, 185, 129, 0.4) !important; background: rgba(16, 185, 129, 0.05) !important;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <div class="pulse-badge-emerald"><span class="pulse-dot-emerald"></span> SYSTEM OPTIMAL · 24/7 SIEM ACTIVE</div>
                    <h2 style="color: #34d399; margin: 0.5rem 0 0.2rem 0; font-weight: 900;">All Endpoints Protected & Healthy</h2>
                    <p style="color: #cbd5e1; margin: 0; font-size: 0.95rem;">Sysmon correlation engine active. 0 active ransomware threats or malicious injections detected across network.</p>
                </div>
                <div style="background: rgba(16, 185, 129, 0.15); padding: 0.8rem 1.4rem; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.3); text-align: center;">
                    <span style="font-size: 0.8rem; color: #6ee7b7; font-weight: bold;">SECURITY SCORE</span>
                    <div style="font-size: 1.6rem; font-weight: 900; color: #34d399;">98 / 100</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_mitre_matrix(stats: dict):
    """Renders visual MITRE ATT&CK Tactic Heatmap."""
    st.markdown("### 🎯 MITRE ATT&CK® Threat Tactic Heatmap")
    cols = st.columns(6)

    tactics = [
        ("Initial Access", stats.get("initial_access", 0), "T1190 / T1566"),
        ("Execution", stats.get("execution", 0), "T1059 / Base64"),
        ("Persistence", stats.get("persistence", 0), "T1547 / RunKeys"),
        ("Credential Access", stats.get("cred_access", 0), "T1003 / LSASS"),
        ("Defense Evasion", stats.get("evasion", 0), "T1562 / Bypass"),
        ("Impact", stats.get("impact", 0), "T1486 / Ransomware"),
    ]

    for col, (label, count, ref) in zip(cols, tactics):
        with col:
            color_class = "color: #fb7185;" if count > 0 else "color: #34d399;"
            st.markdown(f"""
            <div class="mitre-tactic-box">
                <div class="mitre-label">{label}</div>
                <div class="mitre-count" style="{color_class}">{count}</div>
                <div style="font-size: 0.72rem; color: #64748b; font-family: 'JetBrains Mono', monospace;">{ref}</div>
            </div>
            """, unsafe_allow_html=True)
