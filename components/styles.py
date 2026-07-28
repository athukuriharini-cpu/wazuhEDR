"""
ShieldEDR — Premium Light Mode Styles
======================================
All CSS for the premium light-mode dashboard.
Based on Slate & Cyber Blue palette with Inter typography.
"""

import streamlit as st


def inject_light_theme() -> None:
    """Inject the premium light-mode CSS theme into the Streamlit page."""
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)


_GLOBAL_CSS = """
<style>
    /* ══════════════════════════════════════════
       Google Fonts
       ══════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ══════════════════════════════════════════
       CSS Custom Properties (Light Mode)
       ══════════════════════════════════════════ */
    :root {
        --bg-app: #F8FAFC;
        --bg-surface: #FFFFFF;
        --bg-subtle: #F1F5F9;
        --bg-hover: #E8EDF4;

        --border-light: #E2E8F0;
        --border-strong: #CBD5E1;

        --text-primary: #0F172A;
        --text-secondary: #475569;
        --text-muted: #94A3B8;

        --primary-500: #2563EB;
        --primary-600: #1D4ED8;
        --primary-50: #EFF6FF;
        --primary-100: #DBEAFE;

        --success-bg: #ECFDF5;
        --success-border: #A7F3D0;
        --success-text: #047857;
        --success-solid: #10B981;

        --warning-bg: #FFFBEB;
        --warning-border: #FDE68A;
        --warning-text: #B45309;
        --warning-solid: #F59E0B;

        --danger-bg: #FFF1F2;
        --danger-border: #FECDD3;
        --danger-text: #BE123C;
        --danger-solid: #E11D48;

        --info-bg: #EEF2FF;
        --info-border: #C7D2FE;
        --info-text: #4338CA;

        --shadow-sm: 0px 1px 2px 0px rgba(15,23,42,0.04), 0px 1px 3px 0px rgba(15,23,42,0.03);
        --shadow-md: 0px 4px 6px -1px rgba(15,23,42,0.06), 0px 10px 15px -3px rgba(15,23,42,0.04);
        --shadow-lg: 0px 10px 25px -5px rgba(15,23,42,0.08), 0px 20px 40px -8px rgba(15,23,42,0.06);

        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-full: 9999px;
    }

    /* ══════════════════════════════════════════
       Global Reset & Base
       ══════════════════════════════════════════ */
    .stApp {
        background-color: var(--bg-app) !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        -webkit-font-smoothing: antialiased;
    }

    .stApp header {
        background-color: var(--bg-surface) !important;
        border-bottom: 1px solid var(--border-light);
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-surface) !important;
        border-right: 1px solid var(--border-light);
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: var(--text-secondary) !important;
        font-size: 0.875rem;
    }

    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary) !important;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
    }

    /* ══════════════════════════════════════════
       Hero Header
       ══════════════════════════════════════════ */
    .hero-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
    }

    .hero-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 1.75rem;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: -0.03em;
        margin: 0;
    }

    .hero-header p {
        font-size: 0.9rem;
        color: var(--text-muted);
        margin: 0.25rem 0 0;
    }

    /* ══════════════════════════════════════════
       Shield Visualization
       ══════════════════════════════════════════ */
    .shield-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2.5rem 1rem 1.5rem;
    }

    /* ── Shield Shape (SVG-like via clip-path) ── */
    .shield-icon {
        width: 140px;
        height: 168px;
        clip-path: polygon(50% 0%, 100% 12%, 100% 62%, 50% 100%, 0% 62%, 0% 12%);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    /* ── Green Shield ── */
    .shield-safe {
        background: linear-gradient(170deg, #34D399 0%, #10B981 40%, #059669 100%);
        box-shadow: 0 0 0 8px rgba(16, 185, 129, 0.12), 0 0 0 16px rgba(16, 185, 129, 0.06);
        animation: shield-breathe-green 3s ease-in-out infinite;
    }
    .shield-safe::after {
        content: '✓';
        font-size: 3.5rem;
        color: white;
        font-weight: 900;
    }

    @keyframes shield-breathe-green {
        0%, 100% { transform: scale(1); filter: drop-shadow(0 8px 24px rgba(16,185,129,0.3)); }
        50%       { transform: scale(1.03); filter: drop-shadow(0 12px 32px rgba(16,185,129,0.45)); }
    }

    /* ── Red Shield ── */
    .shield-threat {
        background: linear-gradient(170deg, #FB7185 0%, #E11D48 40%, #BE123C 100%);
        box-shadow: 0 0 0 8px rgba(225, 29, 72, 0.15), 0 0 0 16px rgba(225, 29, 72, 0.07);
        animation: shield-breathe-red 1.5s ease-in-out infinite;
    }
    .shield-threat::after {
        content: '!';
        font-size: 3.5rem;
        color: white;
        font-weight: 900;
    }

    @keyframes shield-breathe-red {
        0%, 100% { transform: scale(1); filter: drop-shadow(0 8px 24px rgba(225,29,72,0.35)); }
        50%       { transform: scale(1.05); filter: drop-shadow(0 12px 36px rgba(225,29,72,0.55)); }
    }

    /* ── Pulse Rings ── */
    .pulse-ring-container {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .pulse-ring {
        position: absolute;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        border: 2px solid;
        animation: pulse-expand 2.5s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
    }

    .pulse-ring.safe  { border-color: var(--success-solid); }
    .pulse-ring.threat { border-color: var(--danger-solid); animation-duration: 1.3s; }

    .pulse-ring:nth-child(2) { animation-delay: 0.7s; }

    @keyframes pulse-expand {
        0%   { transform: scale(0.8); opacity: 0.7; }
        100% { transform: scale(1.6); opacity: 0; }
    }

    /* ── Shield Status Text ── */
    .shield-status-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 1.5rem;
        letter-spacing: -0.01em;
    }

    .shield-status-text.safe   { color: var(--success-text); }
    .shield-status-text.threat { color: var(--danger-text); animation: text-pulse 1.5s ease infinite; }

    @keyframes text-pulse {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.65; }
    }

    .shield-subtitle {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
    }

    /* ══════════════════════════════════════════
       Alert Banners
       ══════════════════════════════════════════ */
    .alert-banner {
        padding: 0.75rem 1.25rem;
        border-radius: var(--radius-md);
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.75rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .alert-banner.safe {
        background: var(--success-bg);
        border: 1px solid var(--success-border);
        color: var(--success-text);
    }

    .alert-banner.threat {
        background: var(--danger-bg);
        border: 1px solid var(--danger-border);
        color: var(--danger-text);
        animation: banner-glow 2s ease infinite;
    }

    @keyframes banner-glow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(225,29,72,0); }
        50%      { box-shadow: 0 0 12px 2px rgba(225,29,72,0.08); }
    }

    /* ══════════════════════════════════════════
       Metric Cards
       ══════════════════════════════════════════ */
    .metric-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        text-align: center;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: var(--shadow-sm);
    }

    .metric-card:hover {
        border-color: var(--border-strong);
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.2;
        font-variant-numeric: tabular-nums;
    }

    .metric-value.primary { color: var(--primary-500); }
    .metric-value.success { color: var(--success-text); }
    .metric-value.danger  { color: var(--danger-solid); }
    .metric-value.warning { color: var(--warning-text); }

    .metric-label {
        font-size: 0.7rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-top: 0.4rem;
    }

    /* ══════════════════════════════════════════
       Section Headers
       ══════════════════════════════════════════ */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 1.75rem 0 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-light);
        letter-spacing: -0.01em;
    }

    /* ══════════════════════════════════════════
       Status Pills / Badges
       ══════════════════════════════════════════ */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.2rem 0.6rem;
        border-radius: var(--radius-full);
        font-size: 0.7rem;
        font-weight: 600;
        border: 1px solid transparent;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .status-pill.active   { background: var(--success-bg); border-color: var(--success-border); color: var(--success-text); }
    .status-pill.critical { background: var(--danger-bg); border-color: var(--danger-border); color: var(--danger-text); }
    .status-pill.high     { background: #FFF7ED; border-color: #FDBA74; color: #C2410C; }
    .status-pill.medium   { background: var(--warning-bg); border-color: var(--warning-border); color: var(--warning-text); }
    .status-pill.low      { background: var(--info-bg); border-color: var(--info-border); color: var(--info-text); }
    .status-pill.info     { background: var(--bg-subtle); border-color: var(--border-light); color: var(--text-secondary); }
    .status-pill.offline  { background: #FEF2F2; border-color: #FECACA; color: #991B1B; }

    /* ══════════════════════════════════════════
       Cards
       ══════════════════════════════════════════ */
    .card {
        background: var(--bg-surface);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .card:hover {
        border-color: var(--border-strong);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }

    /* ══════════════════════════════════════════
       Buttons (Streamlit Override)
       ══════════════════════════════════════════ */
    .stButton > button {
        background: var(--primary-500) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.6rem 1.25rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(37, 99, 235, 0.2) !important;
    }

    .stButton > button:hover {
        background: var(--primary-600) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Simulation Buttons ── */
    .btn-safe > div > button {
        background: var(--success-solid) !important;
        box-shadow: 0 1px 3px rgba(16, 185, 129, 0.2) !important;
    }
    .btn-safe > div > button:hover {
        background: #059669 !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }

    .btn-threat > div > button {
        background: var(--danger-solid) !important;
        box-shadow: 0 1px 3px rgba(225, 29, 72, 0.2) !important;
    }
    .btn-threat > div > button:hover {
        background: #BE123C !important;
        box-shadow: 0 4px 12px rgba(225, 29, 72, 0.3) !important;
    }

    /* ══════════════════════════════════════════
       Expanders
       ══════════════════════════════════════════ */
    div[data-testid="stExpander"] {
        background: var(--bg-surface);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
    }

    /* ══════════════════════════════════════════
       Tabs
       ══════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--bg-subtle);
        border-radius: var(--radius-sm);
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.85rem;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background: var(--bg-surface) !important;
        color: var(--text-primary) !important;
        box-shadow: var(--shadow-sm);
        font-weight: 600;
    }

    /* ══════════════════════════════════════════
       Metric Overrides
       ══════════════════════════════════════════ */
    .stMetric label {
        color: var(--text-muted) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .stMetric [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }

    /* ══════════════════════════════════════════
       Demo Mode Badge
       ══════════════════════════════════════════ */
    .demo-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        background: var(--warning-bg);
        border: 1px solid var(--warning-border);
        color: var(--warning-text);
        padding: 0.3rem 0.75rem;
        border-radius: var(--radius-full);
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    /* ══════════════════════════════════════════
       Connection Status
       ══════════════════════════════════════════ */
    .conn-status {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.8rem;
        font-weight: 500;
        padding: 0.4rem 0;
    }

    .conn-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    .conn-dot.online  { background: var(--success-solid); box-shadow: 0 0 6px rgba(16,185,129,0.4); }
    .conn-dot.offline { background: var(--danger-solid); }
    .conn-dot.demo    { background: var(--warning-solid); animation: blink 2s infinite; }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.4; }
    }

    /* ══════════════════════════════════════════
       Data Table
       ══════════════════════════════════════════ */
    .clean-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.85rem;
    }

    .clean-table thead th {
        background: var(--bg-subtle);
        color: var(--text-muted);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
        padding: 0.6rem 0.75rem;
        border-bottom: 1px solid var(--border-light);
        text-align: left;
    }

    .clean-table tbody td {
        padding: 0.65rem 0.75rem;
        border-bottom: 1px solid var(--bg-subtle);
        color: var(--text-primary);
        vertical-align: middle;
    }

    .clean-table tbody tr:hover td {
        background: var(--bg-subtle);
    }

    .font-mono {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
    }

    /* ══════════════════════════════════════════
       Footer
       ══════════════════════════════════════════ */
    .app-footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-muted);
        font-size: 0.8rem;
        border-top: 1px solid var(--border-light);
        margin-top: 2rem;
    }

    .app-footer a {
        color: var(--primary-500);
        text-decoration: none;
    }

    /* ══════════════════════════════════════════
       Scrollbar (subtle)
       ══════════════════════════════════════════ */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-app); }
    ::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
</style>
"""
