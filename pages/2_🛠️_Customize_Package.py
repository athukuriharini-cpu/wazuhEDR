"""
ShieldEDR — Package Customizer Page
===================================
Tailor your EDR security package based on business size, regulatory needs, and budget.
"""

import os
import sys
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai_recommender import FEATURES, LIMITATIONS, recommend_package
from components.styles import inject_light_theme

st.set_page_config(page_title="Package Customizer — ShieldEDR", page_icon="🛠️", layout="wide")
inject_light_theme()

st.markdown("""
<div class="hero-header">
    <h1>🛠️ Package & Feature Customizer</h1>
    <p>Build a tailored protection tier for your business — only pay for what you need</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-header">1. Business Profile</div>', unsafe_allow_html=True)

col_input1, col_input2, col_input3 = st.columns(3)

with col_input1:
    business_type = st.selectbox(
        "Business Type",
        ["Retail / POS", "Healthcare / Clinic", "Legal / Finance", "Tech / Remote", "General Small Business"],
    )

with col_input2:
    endpoints_count = st.number_input("Number of Endpoints", min_value=1, max_value=500, value=15)

with col_input3:
    compliance_need = st.multiselect(
        "Compliance Requirements",
        ["PCI-DSS", "HIPAA", "GDPR", "SOC2", "ISO27001"],
        default=["PCI-DSS"] if "Retail" in business_type else [],
    )

st.markdown('<div class="section-header">2. Select Modules & Features</div>', unsafe_allow_html=True)

col_feat1, col_feat2 = st.columns(2)

selected_features = []
with col_feat1:
    st.markdown("##### Core Protection")
    for feat_key, feat_info in list(FEATURES.items())[:4]:
        chk = st.checkbox(
            f"**{feat_info['name']}** — ${feat_info['cost_per_agent']}/agent/mo",
            value=True,
            help=feat_info["desc"],
            key=f"chk_{feat_key}",
        )
        if chk:
            selected_features.append(feat_key)

with col_feat2:
    st.markdown("##### Advanced / Add-On Modules")
    for feat_key, feat_info in list(FEATURES.items())[4:]:
        chk = st.checkbox(
            f"**{feat_info['name']}** — ${feat_info['cost_per_agent']}/agent/mo",
            value="pci" in feat_key or "soc" in feat_key if compliance_need else False,
            help=feat_info["desc"],
            key=f"chk_{feat_key}",
        )
        if chk:
            selected_features.append(feat_key)

st.markdown('<div class="section-header">3. Estimated Cost & Recommendations</div>', unsafe_allow_html=True)

# Calculate cost
monthly_per_agent = sum(FEATURES[k]["cost_per_agent"] for k in selected_features)
total_monthly = monthly_per_agent * endpoints_count

col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.metric("Price per Endpoint", f"${monthly_per_agent:.2f} / mo")
with col_res2:
    st.metric("Total Monthly Cost", f"${total_monthly:.2f} / mo")
with col_res3:
    st.metric("Annual Billing (15% off)", f"${total_monthly * 12 * 0.85:.2f} / yr")

# AI Recommender Engine Call
rec = recommend_package(business_type, endpoints_count, compliance_need)
st.markdown("---")
st.markdown("### 💡 Tailored Recommendation")
st.info(f"**Recommended Tier:** {rec.get('tier', 'Standard Tier')}\n\n{rec.get('reasoning', '')}")
