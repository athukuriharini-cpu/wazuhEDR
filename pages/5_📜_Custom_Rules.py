"""
ShieldEDR — Custom Wazuh Rules & Firestore Persistence Page
============================================================
Create, customize, and push custom detection rules to Wazuh Manager & Cloud Firestore.
"""

import os
import sys
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from components.styles import inject_light_theme
from firestore_db import get_all_firestore_rules, save_rule_to_firestore
from wazuh.rule_builder import CustomRule, generate_rules_file_xml

st.set_page_config(page_title="Custom Rules — ShieldEDR", page_icon="📜", layout="wide")
inject_light_theme()

st.markdown("""
<div class="hero-header">
    <h1>📜 Custom Wazuh Rule Engine & Cloud Storage</h1>
    <p>Create tailored detection rules, store them in Google Cloud Firestore, and export Wazuh XML configs</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# 1. Existing Rules Overview
# ─────────────────────────────────────
st.markdown('<div class="section-header">Active Custom Detection Rules</div>', unsafe_allow_html=True)

rules_list = get_all_firestore_rules()

if rules_list:
    r_df = pd.DataFrame([
        {
            "Rule ID": r.get("rule_id"),
            "Level": f"Level {r.get('level')}",
            "Category": r.get("category"),
            "Description": r.get("description"),
            "Pattern": r.get("match_pattern"),
            "MITRE ATT&CK": r.get("mitre_id", "N/A"),
        }
        for r in rules_list
    ])
    st.write(
        r_df.to_html(escape=False, index=False, classes="clean-table"),
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────
# 2. Rule Creator Form
# ─────────────────────────────────────
st.markdown('<div class="section-header">➕ Create New Custom Rule</div>', unsafe_allow_html=True)

with st.form("create_rule_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_id = st.number_input("Rule ID (100000+)", min_value=100000, max_value=199999, value=100006)
        new_level = st.slider("Severity Level (1-15)", min_value=1, max_value=15, value=12)
        new_cat = st.selectbox("Threat Category", ["Ransomware", "Execution", "Initial Access", "Exfiltration", "Privilege Escalation", "Compliance"])
    with col2:
        new_desc = st.text_input("Rule Description", "Custom malware pattern detected")
        new_pattern = st.text_input("Regex Match Pattern", "bad_process\\.exe|malicious_script")
        new_mitre = st.text_input("MITRE Technique ID", "T1059")

    new_group = st.text_input("Wazuh Groups (comma-separated)", "malware,custom")

    submit_rule = st.form_submit_button("💾 Save Rule to Firestore & Wazuh Engine")

if submit_rule:
    rule_dict = {
        "rule_id": int(new_id),
        "level": int(new_level),
        "description": new_desc,
        "category": new_cat,
        "match_pattern": new_pattern,
        "mitre_id": new_mitre,
        "group": new_group,
    }
    save_rule_to_firestore(rule_dict)
    st.success(f"✅ Custom Rule #{new_id} saved to Cloud Firestore successfully!")
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────
# 3. Wazuh XML Export Engine
# ─────────────────────────────────────
st.markdown('<div class="section-header">📄 Generated Wazuh local_rules.xml</div>', unsafe_allow_html=True)

rule_objects = [
    CustomRule(
        rule_id=r.get("rule_id", 100000),
        level=r.get("level", 10),
        description=r.get("description", ""),
        group=r.get("group", "custom"),
        category=r.get("category", "General"),
        match_pattern=r.get("match_pattern", ""),
        mitre_id=r.get("mitre_id", ""),
    )
    for r in rules_list
]

xml_output = generate_rules_file_xml(rule_objects)

st.code(xml_output, language="xml")
st.download_button(
    label="📥 Download local_rules.xml for Wazuh Manager",
    data=xml_output,
    file_name="local_rules.xml",
    mime="application/xml",
)
