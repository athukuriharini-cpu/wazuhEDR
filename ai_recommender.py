import json

FEATURES = [
    {
        "id": 1,
        "name": "File Integrity Monitoring",
        "category": "Core Security",
        "description": "Monitors files for unauthorized changes.",
        "storage_mb": 500,
        "is_essential": True,
        "tags": ["all", "compliance", "core"]
    },
    {
        "id": 2,
        "name": "Rootkit Detection",
        "category": "Core Security",
        "description": "Scans system for hidden rootkits.",
        "storage_mb": 200,
        "is_essential": True,
        "tags": ["all", "core"]
    },
    {
        "id": 3,
        "name": "Vulnerability Scanner",
        "category": "Endpoint Management",
        "description": "Scans endpoints for known vulnerabilities.",
        "storage_mb": 300,
        "is_essential": True,
        "tags": ["all", "core"]
    },
    {
        "id": 4,
        "name": "Log Collection & Analysis",
        "category": "Core Security",
        "description": "Collects and analyzes system logs centrally.",
        "storage_mb": 1500,
        "is_essential": True,
        "tags": ["all", "core", "audit"]
    },
    {
        "id": 5,
        "name": "Active Response Engine",
        "category": "Core Security",
        "description": "Automated response actions to threats.",
        "storage_mb": 100,
        "is_essential": True,
        "tags": ["all", "core", "response"]
    },
    {
        "id": 6,
        "name": "Malware Detection (YARA)",
        "category": "Core Security",
        "description": "Signature-based malware detection.",
        "storage_mb": 800,
        "is_essential": True,
        "tags": ["all", "core"]
    },
    {
        "id": 7,
        "name": "Network Traffic Analysis",
        "category": "Network Protection",
        "description": "Analyzes network flows for anomalies.",
        "storage_mb": 1200,
        "is_essential": False,
        "tags": ["network", "office", "tech startup", "school"]
    },
    {
        "id": 8,
        "name": "Brute Force Protection",
        "category": "Network Protection",
        "description": "Detects and blocks brute force authentication attempts.",
        "storage_mb": 150,
        "is_essential": True,
        "tags": ["all", "core"]
    },
    {
        "id": 9,
        "name": "Compliance Auditing (PCI-DSS)",
        "category": "Compliance & Audit",
        "description": "Checks system against PCI-DSS standards.",
        "storage_mb": 250,
        "is_essential": False,
        "tags": ["retail", "ecommerce", "restaurant", "finance"]
    },
    {
        "id": 10,
        "name": "Compliance Auditing (HIPAA)",
        "category": "Compliance & Audit",
        "description": "Checks system against HIPAA standards.",
        "storage_mb": 250,
        "is_essential": False,
        "tags": ["healthcare", "clinic", "hospital", "medical"]
    },
    {
        "id": 11,
        "name": "Compliance Auditing (GDPR)",
        "category": "Compliance & Audit",
        "description": "Checks system against GDPR standards.",
        "storage_mb": 250,
        "is_essential": False,
        "tags": ["eu", "retail", "tech startup", "international"]
    },
    {
        "id": 12,
        "name": "Agent Auto-Update",
        "category": "Endpoint Management",
        "description": "Automatically updates endpoint agents.",
        "storage_mb": 50,
        "is_essential": True,
        "tags": ["all", "core"]
    },
    {
        "id": 13,
        "name": "Real-time Alerting",
        "category": "Integration & Alerts",
        "description": "Generates real-time alerts for critical events.",
        "storage_mb": 100,
        "is_essential": False,
        "tags": ["all", "response"]
    },
    {
        "id": 14,
        "name": "Incident Response Playbooks",
        "category": "Integration & Alerts",
        "description": "Pre-defined response playbooks for common incidents.",
        "storage_mb": 200,
        "is_essential": False,
        "tags": ["enterprise", "tech startup", "law firm"]
    },
    {
        "id": 15,
        "name": "API Gateway",
        "category": "Integration & Alerts",
        "description": "Provides API access to EDR functions.",
        "storage_mb": 150,
        "is_essential": False,
        "tags": ["tech startup", "developer", "enterprise"]
    },
    {
        "id": 16,
        "name": "Slack Integration",
        "category": "Integration & Alerts",
        "description": "Sends alerts to Slack channels.",
        "storage_mb": 50,
        "is_essential": False,
        "tags": ["tech startup", "remote", "office"]
    },
    {
        "id": 17,
        "name": "WhatsApp Alerts",
        "category": "Integration & Alerts",
        "description": "Sends high-priority alerts via WhatsApp.",
        "storage_mb": 50,
        "is_essential": False,
        "tags": ["retail", "restaurant", "small business"]
    },
    {
        "id": 18,
        "name": "Microsoft Teams Alerts",
        "category": "Integration & Alerts",
        "description": "Sends alerts to MS Teams.",
        "storage_mb": 50,
        "is_essential": False,
        "tags": ["enterprise", "office", "law firm", "accounting firm", "school"]
    },
    {
        "id": 19,
        "name": "Email Alerts",
        "category": "Integration & Alerts",
        "description": "Sends alerts via Email.",
        "storage_mb": 50,
        "is_essential": False,
        "tags": ["all", "standard"]
    },
    {
        "id": 20,
        "name": "Cloud Workload Protection",
        "category": "Endpoint Management",
        "description": "Secures cloud instances and VMs.",
        "storage_mb": 600,
        "is_essential": False,
        "tags": ["tech startup", "cloud", "enterprise"]
    },
    {
        "id": 21,
        "name": "Container Security",
        "category": "Endpoint Management",
        "description": "Secures Docker/Kubernetes containers.",
        "storage_mb": 500,
        "is_essential": False,
        "tags": ["tech startup", "developer", "cloud"]
    },
    {
        "id": 22,
        "name": "USB Device Control",
        "category": "Endpoint Management",
        "description": "Monitors and restricts USB device usage.",
        "storage_mb": 100,
        "is_essential": False,
        "tags": ["healthcare", "law firm", "accounting firm", "government", "school"]
    },
    {
        "id": 23,
        "name": "Application Whitelisting",
        "category": "Endpoint Management",
        "description": "Only allows approved applications to run.",
        "storage_mb": 250,
        "is_essential": False,
        "tags": ["healthcare", "finance", "kiosk", "warehouse", "retail"]
    },
    {
        "id": 24,
        "name": "Registry Monitoring (Windows)",
        "category": "Core Security",
        "description": "Monitors Windows registry for changes.",
        "storage_mb": 200,
        "is_essential": False,
        "tags": ["windows", "office"]
    },
    {
        "id": 25,
        "name": "Syslog Forwarding",
        "category": "Integration & Alerts",
        "description": "Forwards logs to external SIEM.",
        "storage_mb": 100,
        "is_essential": False,
        "tags": ["enterprise", "compliance"]
    },
    {
        "id": 26,
        "name": "Threat Intelligence Feed",
        "category": "Advanced Threat Intel",
        "description": "Integrates external threat intel feeds.",
        "storage_mb": 800,
        "is_essential": False,
        "tags": ["enterprise", "tech startup", "finance"]
    },
    {
        "id": 27,
        "name": "Behavioral Analysis Engine",
        "category": "Advanced Threat Intel",
        "description": "Detects anomalous behavior patterns.",
        "storage_mb": 1500,
        "is_essential": False,
        "tags": ["enterprise", "tech startup", "finance", "healthcare"]
    },
    {
        "id": 28,
        "name": "Memory Forensics",
        "category": "Advanced Threat Intel",
        "description": "Analyzes RAM for advanced threats.",
        "storage_mb": 2000,
        "is_essential": False,
        "tags": ["enterprise", "law firm", "finance"]
    },
    {
        "id": 29,
        "name": "DNS Monitoring",
        "category": "Network Protection",
        "description": "Monitors DNS requests for malicious domains.",
        "storage_mb": 400,
        "is_essential": False,
        "tags": ["network", "office", "school"]
    },
    {
        "id": 30,
        "name": "Automated Backup & Recovery",
        "category": "Endpoint Management",
        "description": "Automated endpoint backups and recovery tools.",
        "storage_mb": 2500,
        "is_essential": False,
        "tags": ["ransomware", "office", "accounting firm", "law firm"]
    }
]

LIMITATIONS = [
    {
        "id": 1,
        "name": "Reduce log retention to 7 days",
        "description": "Keep only 7 days of logs instead of 30.",
        "storage_saved_mb": 1000,
        "affects_features": [4]
    },
    {
        "id": 2,
        "name": "Disable real-time scanning",
        "description": "Use scheduled scanning to save resources.",
        "storage_saved_mb": 200,
        "affects_features": [6]
    },
    {
        "id": 3,
        "name": "Use lightweight YARA rules only",
        "description": "Reduces malware detection footprint.",
        "storage_saved_mb": 500,
        "affects_features": [6]
    },
    {
        "id": 4,
        "name": "Limit alert history to 30 days",
        "description": "Saves storage for alert metadata.",
        "storage_saved_mb": 50,
        "affects_features": [13]
    },
    {
        "id": 5,
        "name": "Use basic behavioral analysis only",
        "description": "Reduces storage needed for behavioral baselines.",
        "storage_saved_mb": 800,
        "affects_features": [27]
    },
    {
        "id": 6,
        "name": "Disable memory forensics",
        "description": "Avoid memory dump storage.",
        "storage_saved_mb": 2000,
        "affects_features": [28]
    },
    {
        "id": 7,
        "name": "Limit active agents to 10",
        "description": "Reduces overall central storage needs.",
        "storage_saved_mb": 500,
        "affects_features": []
    },
    {
        "id": 8,
        "name": "Disable container security",
        "description": "Turn off container monitoring.",
        "storage_saved_mb": 500,
        "affects_features": [21]
    },
    {
        "id": 9,
        "name": "Disable cloud sync",
        "description": "Keep backups local only.",
        "storage_saved_mb": 1500,
        "affects_features": [30]
    },
    {
        "id": 10,
        "name": "Reduce Threat Intel Feeds",
        "description": "Use only top priority feeds.",
        "storage_saved_mb": 500,
        "affects_features": [26]
    }
]

def get_feature_by_id(feature_id: int) -> dict:
    for feature in FEATURES:
        if feature["id"] == feature_id:
            return feature
    return None

def get_limitation_by_id(limitation_id: int) -> dict:
    for limitation in LIMITATIONS:
        if limitation["id"] == limitation_id:
            return limitation
    return None

def calculate_storage(feature_ids: list, limitation_ids: list) -> dict:
    base_storage_mb = 0
    savings_mb = 0
    feature_details = []

    for fid in feature_ids:
        f = get_feature_by_id(fid)
        if f:
            base_storage_mb += f["storage_mb"]
            feature_details.append({"name": f["name"], "storage_mb": f["storage_mb"]})

    for lid in limitation_ids:
        l = get_limitation_by_id(lid)
        if l:
            savings_mb += l["storage_saved_mb"]
            
    total_storage_mb = max(0, base_storage_mb - savings_mb)

    return {
        "base_storage_mb": base_storage_mb,
        "savings_mb": savings_mb,
        "total_storage_mb": total_storage_mb,
        "feature_details": feature_details
    }

def recommend_features(storage_mb: int, use_case: str) -> dict:
    use_case_lower = use_case.lower()
    
    recommended_feature_ids = set()
    suggested_limitation_ids = set()
    
    # Always include essential features
    for feature in FEATURES:
        if feature["is_essential"]:
            recommended_feature_ids.add(feature["id"])

    # Match use case keywords to tags
    tokens = use_case_lower.replace(",", " ").split()
    tokens.append(use_case_lower) # include full string
    
    for feature in FEATURES:
        for tag in feature["tags"]:
            if tag in tokens or tag in use_case_lower:
                recommended_feature_ids.add(feature["id"])
                
    recommended_feature_ids = list(recommended_feature_ids)
    
    # Calculate storage
    storage_info = calculate_storage(recommended_feature_ids, list(suggested_limitation_ids))
    
    # Apply limitations if over budget
    # Sort limitations by largest savings first for a greedy approach
    sorted_limitations = sorted(LIMITATIONS, key=lambda x: x["storage_saved_mb"], reverse=True)
    
    while storage_info["total_storage_mb"] > storage_mb and len(suggested_limitation_ids) < len(LIMITATIONS):
        added = False
        for limitation in sorted_limitations:
            if limitation["id"] not in suggested_limitation_ids:
                # check if limitation applies to chosen features or applies globally
                applies = not limitation["affects_features"] or any(f_id in recommended_feature_ids for f_id in limitation["affects_features"])
                if applies:
                    suggested_limitation_ids.add(limitation["id"])
                    added = True
                    storage_info = calculate_storage(recommended_feature_ids, list(suggested_limitation_ids))
                    break
        if not added:
            break
            
    reasoning = f"Based on the use case '{use_case}', essential core features were selected along with tailored capabilities. "
    if 'healthcare' in use_case_lower or 'medical' in use_case_lower:
        reasoning += "Prioritized HIPAA compliance and strict endpoint controls. "
    elif 'retail' in use_case_lower or 'shop' in use_case_lower:
        reasoning += "Prioritized PCI-DSS compliance and whitelisting. "
    elif 'tech startup' in use_case_lower or 'developer' in use_case_lower:
        reasoning += "Included advanced features like container security and API access. "
        
    if storage_info["total_storage_mb"] > storage_mb:
        reasoning += "Even with maximum limitations, the required storage exceeds the available budget."
    elif len(suggested_limitation_ids) > 0:
        reasoning += "Some limitations were suggested to fit the storage constraints."
    else:
        reasoning += "All recommended features fit within the provided storage budget."

    return {
        "recommended_features": recommended_feature_ids,
        "total_storage_mb": storage_info["total_storage_mb"],
        "suggested_limitations": list(suggested_limitation_ids),
        "reasoning": reasoning
    }
