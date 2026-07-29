"""
ShieldEDR — AI Recommender & Feature Matrix Module
===================================================
Provides smart feature recommendations, cost estimations, and storage budget tailoring
for MSME EDR deployments.
"""

FEATURES = {
    "core_fim": {
        "id": 1,
        "name": "File Integrity Monitoring (FIM)",
        "category": "Core Security",
        "cost_per_agent": 1.50,
        "desc": "Monitors system files and registry keys for unauthorized modifications and ransomware activity.",
        "storage_mb": 500,
        "is_essential": True,
    },
    "core_rootkit": {
        "id": 2,
        "name": "Rootkit & Anomaly Scanner",
        "category": "Core Security",
        "cost_per_agent": 1.00,
        "desc": "Scans system memory and kernel space for hidden rootkits and memory injection threats.",
        "storage_mb": 200,
        "is_essential": True,
    },
    "core_sysmon": {
        "id": 3,
        "name": "Windows Sysmon Correlation",
        "category": "Core Security",
        "cost_per_agent": 1.25,
        "desc": "Correlates process creation, LSASS memory access, and remote thread injections.",
        "storage_mb": 400,
        "is_essential": True,
    },
    "core_active_resp": {
        "id": 4,
        "name": "Automated Active Response",
        "category": "Core Security",
        "cost_per_agent": 1.25,
        "desc": "Automatically blocks attacker IPs, terminates malicious processes, and isolates endpoints.",
        "storage_mb": 100,
        "is_essential": True,
    },
    "addon_vulnerability": {
        "id": 5,
        "name": "Vulnerability Scanner",
        "category": "Endpoint Management",
        "cost_per_agent": 0.75,
        "desc": "Scans endpoints against CVE databases to detect unpatched software vulnerabilities.",
        "storage_mb": 300,
        "is_essential": False,
    },
    "addon_yara": {
        "id": 6,
        "name": "YARA Malware Engine",
        "category": "Core Security",
        "cost_per_agent": 1.00,
        "desc": "Executes custom YARA signature rules on suspicious executable creation.",
        "storage_mb": 800,
        "is_essential": False,
    },
    "addon_pci_compliance": {
        "id": 7,
        "name": "Regulatory Compliance Audit (PCI/HIPAA/GDPR)",
        "category": "Compliance",
        "cost_per_agent": 1.50,
        "desc": "Generates continuous audit trails and compliance reports for regulatory frameworks.",
        "storage_mb": 600,
        "is_essential": False,
    },
    "addon_threat_intel": {
        "id": 8,
        "name": "Live Threat Intelligence Feed",
        "category": "Advanced Intel",
        "cost_per_agent": 1.00,
        "desc": "Integrates live threat intelligence IOC feeds to catch zero-day exploits and C2 domains.",
        "storage_mb": 800,
        "is_essential": False,
    },
}

LIMITATIONS = [
    {
        "id": 1,
        "name": "7-Day Log Retention",
        "desc": "Keep 7 days of active logs to save central indexer storage.",
        "storage_saved_mb": 1000,
    },
    {
        "id": 2,
        "name": "Local Active Response Only",
        "desc": "Execute response actions locally on endpoint without cloud relay.",
        "storage_saved_mb": 200,
    },
    {
        "id": 3,
        "name": "Lightweight YARA Ruleset",
        "desc": "Use top-priority malware signatures only to reduce RAM footprint.",
        "storage_saved_mb": 500,
    },
]

def recommend_package(business_type: str, endpoints_count: int, compliance_need: list) -> dict:
    """Recommends an EDR security tier based on business profile."""
    tier = "Starter Protection"
    if endpoints_count > 50 or "SOC2" in compliance_need or "ISO27001" in compliance_need:
        tier = "Enterprise Guardian Suite"
    elif endpoints_count > 15 or "HIPAA" in compliance_need or "PCI-DSS" in compliance_need:
        tier = "Business Security Suite"

    reasoning = f"Based on your **{business_type}** profile with **{endpoints_count} endpoints**"
    if compliance_need:
        reasoning += f" and compliance requirements ({', '.join(compliance_need)}),"
    else:
        reasoning += ","
    reasoning += f" we recommend the **{tier}** to deliver complete threat protection while optimizing cloud resource costs."

    return {
        "tier": tier,
        "reasoning": reasoning
    }

def calculate_storage(feature_keys: list, limitation_ids: list = None) -> dict:
    """Calculates total storage requirements based on selected features."""
    base_storage_mb = 0
    for key in feature_keys:
        if key in FEATURES:
            base_storage_mb += FEATURES[key]["storage_mb"]

    return {
        "total_storage_mb": base_storage_mb,
        "base_storage_mb": base_storage_mb,
    }
