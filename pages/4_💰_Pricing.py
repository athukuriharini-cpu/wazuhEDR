import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pricing - Enterprise EDR",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Styling & Custom CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Dark Purple/Blue Deep Gradient Background */
    .stApp {
        background: #0b0e17;
        color: #f1f5f9;
    }
    
    /* Hero Container */
    .hero-card {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.75) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 20px;
        padding: 3rem 2rem 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
    }
    
    .hero-title {
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #c084fc 0%, #60a5fa 50%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.75rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtext {
        font-size: 1.3rem;
        color: #94a3b8;
        max-width: 750px;
        margin: 0 auto 1.8rem auto;
        line-height: 1.6;
    }
    
    .hero-pill-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .hero-pill {
        background: rgba(139, 92, 246, 0.12);
        color: #ddd6fe;
        border: 1px solid rgba(139, 92, 246, 0.3);
        padding: 0.45rem 1.1rem;
        border-radius: 9999px;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* Pricing Cards Layout */
    .tier-card {
        background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 18px;
        padding: 2rem 1.6rem;
        height: 100%;
        transition: all 0.35s ease;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .tier-card:hover {
        transform: translateY(-8px);
        border-color: rgba(167, 139, 250, 0.5);
        box-shadow: 0 20px 30px -10px rgba(99, 102, 241, 0.35);
    }
    
    /* Highlighted Most Popular Card with Glow */
    .tier-card-popular {
        background: linear-gradient(180deg, #2e1065 0%, #0f172a 100%);
        border: 2px solid #8b5cf6;
        border-radius: 20px;
        padding: 2.2rem 1.6rem;
        position: relative;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.45), 0 15px 30px -10px rgba(0, 0, 0, 0.6);
        transition: all 0.35s ease;
    }
    
    .tier-card-popular:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 0 45px rgba(139, 92, 246, 0.75), 0 25px 35px -10px rgba(139, 92, 246, 0.4);
    }

    /* Badges */
    .badge-starter {
        background: rgba(59, 130, 246, 0.2);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.4);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 1rem;
    }

    .badge-popular {
        background: linear-gradient(90deg, #8b5cf6 0%, #ec4899 100%);
        color: #ffffff;
        padding: 0.4rem 1rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 1rem;
        letter-spacing: 0.05em;
        box-shadow: 0 0 15px rgba(236, 72, 153, 0.6);
    }

    .badge-enterprise {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 1rem;
    }

    .tier-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }

    .tier-price-amount {
        font-size: 2.6rem;
        font-weight: 900;
        color: #f8fafc;
    }

    .tier-price-unit {
        font-size: 0.95rem;
        color: #94a3b8;
        font-weight: 500;
    }

    .tier-subtitle {
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        line-height: 1.4;
        min-height: 2.6rem;
    }

    .feature-list {
        margin: 1rem 0 1.5rem 0;
        padding: 0;
        list-style: none;
    }

    .feature-item {
        color: #e2e8f0;
        font-size: 0.92rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .check-icon {
        color: #34d399;
        font-weight: bold;
    }

    /* Calculator Styling */
    .calc-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 2.2rem;
        margin-top: 3rem;
        margin-bottom: 3rem;
        box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.5);
    }

    .calc-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.5rem;
    }

    .calc-sub {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1.8rem;
    }

    .calc-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
    }

    .calc-card-active {
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.5);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.25);
    }

    .calc-price {
        font-size: 1.8rem;
        font-weight: 800;
        color: #a78bfa;
    }

    .calc-savings {
        color: #34d399;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }

    /* Table Customizations */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Section Headings */
    .section-title {
        font-size: 2rem;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Hero Section
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">Enterprise Security. Startup Pricing.</div>
    <div class="hero-subtext">
        Shield your infrastructure with military-grade EDR protection. 
        Zero minimum device commitments, zero lock-in contracts, and 100% pay-as-you-grow transparency.
    </div>
    <div class="hero-pill-container">
        <span class="hero-pill">⚡ 2-Minute Agent Deployment</span>
        <span class="hero-pill">🛡️ Zero Infrastructure Overhead</span>
        <span class="hero-pill">💳 No Credit Card Required for Trial</span>
        <span class="hero-pill">🇮🇳 Native Rupee Billing</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Pricing Tiers Display (3 Columns)
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 1.05, 1])

with col1:
    st.markdown("""
    <div class="tier-card">
        <div>
            <span class="badge-starter">Perfect for Solo Founders</span>
            <div class="tier-title">Starter</div>
            <div class="tier-price-amount">₹10 <span class="tier-price-unit">/ device / month</span></div>
            <div class="tier-subtitle">Core EDR defenses tailored for micro-teams, side projects, and bootstrapped startups.</div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 1rem 0;">
            <ul class="feature-list">
                <li class="feature-item"><span class="check-icon">✓</span> Up to 5 devices</li>
                <li class="feature-item"><span class="check-icon">✓</span> Core security features (Behavioral Shield)</li>
                <li class="feature-item"><span class="check-icon">✓</span> Instant email alerts</li>
                <li class="feature-item"><span class="check-icon">✓</span> 7-day log retention</li>
                <li class="feature-item"><span class="check-icon">✓</span> Community support</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Get Started with Starter", key="btn_starter", use_container_width=True):
        st.session_state["selected_tier"] = "Starter"
        st.session_state["show_trial_modal"] = True

with col2:
    st.markdown("""
    <div class="tier-card-popular">
        <div>
            <span class="badge-popular">⭐ Most Popular</span>
            <div class="tier-title">Professional</div>
            <div class="tier-price-amount">₹50 <span class="tier-price-unit">/ device / month</span></div>
            <div class="tier-subtitle">Full-spectrum endpoint defense with real-time multi-channel incident response.</div>
            <hr style="border-color: rgba(139, 92, 246, 0.3); margin: 1rem 0;">
            <ul class="feature-list">
                <li class="feature-item"><span class="check-icon">✓</span> Up to 50 devices</li>
                <li class="feature-item"><span class="check-icon">✓</span> All security features</li>
                <li class="feature-item"><span class="check-icon">✓</span> Slack + Email + WhatsApp alerts</li>
                <li class="feature-item"><span class="check-icon">✓</span> 30-day log retention</li>
                <li class="feature-item"><span class="check-icon">✓</span> Priority support</li>
                <li class="feature-item"><span class="check-icon">✓</span> Compliance reports</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔥 Start Pro Free Trial", key="btn_pro", type="primary", use_container_width=True):
        st.session_state["selected_tier"] = "Professional"
        st.session_state["show_trial_modal"] = True

with col3:
    st.markdown("""
    <div class="tier-card">
        <div>
            <span class="badge-enterprise">For Growing Businesses</span>
            <div class="tier-title">Enterprise</div>
            <div class="tier-price-amount">₹100 <span class="tier-price-unit">/ device / month</span></div>
            <div class="tier-subtitle">Unrestricted threat intelligence, dedicated security engineer, and custom API access.</div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 1rem 0;">
            <ul class="feature-list">
                <li class="feature-item"><span class="check-icon">✓</span> Unlimited devices</li>
                <li class="feature-item"><span class="check-icon">✓</span> All features + Advanced Threat Intel</li>
                <li class="feature-item"><span class="check-icon">✓</span> All integrations</li>
                <li class="feature-item"><span class="check-icon">✓</span> 90-day log retention</li>
                <li class="feature-item"><span class="check-icon">✓</span> 24/7 dedicated support</li>
                <li class="feature-item"><span class="check-icon">✓</span> Custom compliance</li>
                <li class="feature-item"><span class="check-icon">✓</span> API access</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Contact Enterprise Sales", key="btn_enterprise", use_container_width=True):
        st.session_state["selected_tier"] = "Enterprise"
        st.session_state["show_trial_modal"] = True

# -----------------------------------------------------------------------------
# 5. Interactive Pricing Calculator
# -----------------------------------------------------------------------------
st.markdown("""
<div class="calc-container">
    <div class="calc-header">🧮 Interactive Pricing Calculator</div>
    <div class="calc-sub">Drag the slider to calculate monthly cost based on your fleet size.</div>
""", unsafe_allow_html=True)

calc_col1, calc_col2 = st.columns([1.2, 1])

with calc_col1:
    device_count = st.slider(
        "Number of Endpoint Devices (1 - 100):",
        min_value=1,
        max_value=100,
        value=15,
        step=1,
        help="Adjust device count to see auto-calculated monthly investment for each tier."
    )
    
    billing_cycle = st.radio(
        "Billing Frequency:",
        options=["Monthly", "Annually (20% Off)"],
        horizontal=True
    )
    
    discount_multiplier = 0.8 if "Annually" in billing_cycle else 1.0

with calc_col2:
    starter_monthly = device_count * 10 * discount_multiplier
    pro_monthly = device_count * 50 * discount_multiplier
    ent_monthly = device_count * 100 * discount_multiplier

    c1, c2, c3 = st.columns(3)
    
    with c1:
        is_disabled = device_count > 5
        st.markdown(f"""
        <div class="calc-card">
            <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;">STARTER</div>
            <div class="calc-price">₹{int(starter_monthly):,}</div>
            <div style="font-size: 0.75rem; color: #cbd5e1;">/month</div>
            {'<div style="color: #ef4444; font-size: 0.7rem; margin-top:4px;">(Max 5 devices)</div>' if is_disabled else '<div class="calc-savings">Best for ≤5 dev</div>'}
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        is_pro_disabled = device_count > 50
        st.markdown(f"""
        <div class="calc-card-active">
            <div style="font-size: 0.85rem; color: #c084fc; font-weight: 700;">PROFESSIONAL</div>
            <div class="calc-price">₹{int(pro_monthly):,}</div>
            <div style="font-size: 0.75rem; color: #cbd5e1;">/month</div>
            {'<div style="color: #ef4444; font-size: 0.7rem; margin-top:4px;">(Max 50 devices)</div>' if is_pro_disabled else '<div class="calc-savings">Most Popular</div>'}
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="calc-card">
            <div style="font-size: 0.85rem; color: #34d399; font-weight: 600;">ENTERPRISE</div>
            <div class="calc-price">₹{int(ent_monthly):,}</div>
            <div style="font-size: 0.75rem; color: #cbd5e1;">/month</div>
            <div class="calc-savings">Unlimited Devices</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. Detailed Feature Comparison Table
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">📊 Feature Matrix & Comparison</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Compare tier capabilities side-by-side to choose the right fit for your security posture.</div>', unsafe_allow_html=True)

feature_data = {
    "Feature / Capability": [
        "Device Capacity",
        "Security Features",
        "Alert Channels",
        "Log Retention",
        "Support SLA",
        "Compliance Reports",
        "Advanced Threat Intel",
        "API Access",
        "All Integrations",
        "Custom Rules Engine"
    ],
    "Starter (₹10/device/mo)": [
        "Up to 5 devices",
        "✅ Core security features",
        "✅ Email alerts",
        "7-day log retention",
        "Community support",
        "❌",
        "❌",
        "❌",
        "❌",
        "❌"
    ],
    "Professional (₹50/device/mo)": [
        "Up to 50 devices",
        "✅ All security features",
        "✅ Slack + Email + WhatsApp",
        "30-day log retention",
        "Priority support",
        "✅ Included",
        "❌",
        "❌",
        "Partial Integrations",
        "✅ Included"
    ],
    "Enterprise (₹100/device/mo)": [
        "Unlimited devices",
        "✅ All features + Advanced Intel",
        "✅ All integrations + Webhooks",
        "90-day log retention",
        "24/7 dedicated support",
        "✅ Custom compliance",
        "✅ Included",
        "✅ Full API access",
        "✅ All integrations",
        "✅ Unlimited custom rules"
    ]
}

df_features = pd.DataFrame(feature_data)
st.table(df_features)

# -----------------------------------------------------------------------------
# 7. Start Free Trial Button & Call-to-Action Section
# -----------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
with cta_col2:
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 16px; padding: 2rem;">
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">Ready to Secure Your Business?</h3>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.25rem;">Deploy full enterprise protection in 2 minutes. No credit card required.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Start Free Trial", key="btn_trial_main", type="primary", use_container_width=True):
        st.session_state["show_trial_modal"] = True
        st.session_state["selected_tier"] = st.session_state.get("selected_tier", "Professional")

# Handle Modal / Form for Trial Activation
if st.session_state.get("show_trial_modal", False):
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander(f"⚡ Instant Trial Activation ({st.session_state.get('selected_tier', 'Professional')} Tier)", expanded=True):
        st.write("Enter your details to generate your 14-day free trial license key:")
        
        with st.form(key="trial_activation_form"):
            form_col1, form_col2 = st.columns(2)
            with form_col1:
                full_name = st.text_input("Full Name *", placeholder="e.g. Ananya Rao")
                work_email = st.text_input("Work Email *", placeholder="ananya@company.com")
            with form_col2:
                company_name = st.text_input("Company Name *", placeholder="Acme Cyber Corp")
                est_devices = st.number_input("Number of Devices", min_value=1, max_value=500, value=15)
            
            submit_trial = st.form_submit_button("🛡️ Generate Free Trial License Key", type="primary", use_container_width=True)
            
            if submit_trial:
                if full_name and work_email and company_name:
                    st.success(f"🎉 Free Trial Activated for **{company_name}** under the **{st.session_state.get('selected_tier')}** tier!")
                    st.info(f"🔑 License Key: `EDR-FREE-{work_email.split('@')[0].upper()}-2026-X99`\n\nInstructions sent to **{work_email}**.")
                    st.balloons()
                else:
                    st.error("Please fill in all required fields marked with *")
