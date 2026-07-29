"""
ShieldEDR Million-Dollar Dark Glassmorphism Theme & Style System
===============================================================
Injects ultra-premium obsidian glassmorphism CSS styling, modern Google Inter typography,
glowing neon accents, animated pulse badges, and crisp responsive layouts.
"""

import streamlit as st

def inject_light_theme():
    """Injects ultra-premium Million-Dollar Dark Glassmorphism CSS Theme."""
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

        /* Root Variables */
        :root {
            --bg-obsidian: #07090e;
            --card-glass: rgba(15, 23, 42, 0.75);
            --card-border: rgba(139, 92, 246, 0.25);
            --neon-purple: #a855f7;
            --neon-emerald: #10b981;
            --neon-cyan: #06b6d4;
            --neon-rose: #f43f5e;
            --neon-amber: #f59e0b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
        }

        /* Global Styling Override */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: var(--bg-obsidian) !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(6, 182, 212, 0.15) 0px, transparent 50%),
                radial-gradient(at 50% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%) !important;
            font-family: 'Inter', sans-serif !important;
            color: var(--text-primary) !important;
        }

        /* Header / Toolbar Adjustments */
        [data-testid="stHeader"] {
            background: rgba(7, 9, 14, 0.6) !important;
            backdrop-filter: blur(12px) !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(11, 15, 25, 0.85) !important;
            border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
            backdrop-filter: blur(16px) !important;
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: var(--card-glass) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            backdrop-filter: blur(16px) !important;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin-bottom: 1.2rem !important;
        }

        .glass-card:hover {
            transform: translateY(-4px) !important;
            border-color: rgba(168, 85, 247, 0.5) !important;
            box-shadow: 0 20px 40px -15px rgba(168, 85, 247, 0.25) !important;
        }

        /* Hero Executive Banner */
        .hero-banner {
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
            border: 1px solid rgba(168, 85, 247, 0.35) !important;
            border-radius: 20px !important;
            padding: 2.2rem 2rem !important;
            margin-bottom: 2rem !important;
            box-shadow: 0 20px 50px -15px rgba(139, 92, 246, 0.3) !important;
        }

        .hero-title {
            font-size: 2.8rem !important;
            font-weight: 900 !important;
            letter-spacing: -0.03em !important;
            background: linear-gradient(90deg, #c084fc 0%, #60a5fa 50%, #34d399 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin-bottom: 0.5rem !important;
        }

        /* Animated Live Pulse Badge */
        .pulse-badge-emerald {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.35);
            padding: 0.35rem 0.9rem;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 700;
        }

        .pulse-dot-emerald {
            width: 8px;
            height: 8px;
            background-color: #34d399;
            border-radius: 50%;
            box-shadow: 0 0 10px #34d399;
            animation: pulse-ring 1.8s infinite;
        }

        .pulse-badge-rose {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(244, 63, 94, 0.15);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.35);
            padding: 0.35rem 0.9rem;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 700;
        }

        .pulse-dot-rose {
            width: 8px;
            height: 8px;
            background-color: #fb7185;
            border-radius: 50%;
            box-shadow: 0 0 10px #fb7185;
            animation: pulse-ring 1.2s infinite;
        }

        @keyframes pulse-ring {
            0% { transform: scale(0.95); opacity: 0.9; }
            50% { transform: scale(1.3); opacity: 0.4; }
            100% { transform: scale(0.95); opacity: 0.9; }
        }

        /* MITRE ATT&CK Matrix Card */
        .mitre-tactic-box {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            transition: all 0.2s ease;
        }

        .mitre-tactic-box:hover {
            border-color: var(--neon-cyan);
            background: rgba(6, 182, 212, 0.1);
        }

        .mitre-count {
            font-size: 1.8rem;
            font-weight: 900;
            color: #38bdf8;
        }

        .mitre-label {
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
        }

        /* Buttons Styling */
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 700 !important;
            transition: all 0.2s ease !important;
        }

        .stButton>button[kind="primary"] {
            background: linear-gradient(90deg, #8b5cf6 0%, #6366f1 100%) !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
        }

        .stButton>button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6) !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-obsidian);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(139, 92, 246, 0.3);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(139, 92, 246, 0.6);
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
