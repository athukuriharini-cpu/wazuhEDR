"""
Shield Visualization Component
==============================
Renders the animated shield SVG with pulse rings.
"""

import streamlit as st


def render_shield(is_threat: bool, threat_count: int = 0) -> None:
    """Render the main shield visualization.

    Args:
        is_threat: True to show red threat shield, False for green safe shield.
        threat_count: Number of threats detected (shown when is_threat=True).
    """
    if is_threat:
        st.markdown(f"""
        <div class="shield-section">
            <div class="pulse-ring-container">
                <div class="pulse-ring threat"></div>
                <div class="pulse-ring threat"></div>
                <div class="shield-icon shield-threat"></div>
            </div>
            <div class="shield-status-text threat">
                ⚠ {threat_count} THREAT{'S' if threat_count != 1 else ''} DETECTED
            </div>
            <div class="shield-subtitle">
                Threats automatically isolated · Immediate review recommended
            </div>
        </div>

        <div class="alert-banner threat">
            🚨 <strong>ALERT:</strong>&nbsp; {threat_count} security threat(s) detected and quarantined.
            Affected endpoints have been automatically isolated.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="shield-section">
            <div class="pulse-ring-container">
                <div class="pulse-ring safe"></div>
                <div class="pulse-ring safe"></div>
                <div class="shield-icon shield-safe"></div>
            </div>
            <div class="shield-status-text safe">YOUR NETWORK IS PROTECTED</div>
            <div class="shield-subtitle">
                All endpoints monitored · No threats detected · Continuous protection active
            </div>
        </div>

        <div class="alert-banner safe">
            ✅ <strong>All Clear:</strong>&nbsp; All monitored endpoints are secure. Real-time protection is active.
        </div>
        """, unsafe_allow_html=True)


def render_metric_card(value: str, label: str, color: str = "") -> None:
    """Render a styled metric card.

    Args:
        value: The metric value to display.
        label: The metric label.
        color: CSS color class ('primary', 'success', 'danger', 'warning', or empty).
    """
    color_class = f" {color}" if color else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value{color_class}">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)
