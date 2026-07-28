"""
test_data.py - EDR Security Dashboard Test Data Generator

This module generates realistic simulated EDR security event data, host health metrics,
agent statuses, and historical event count timelines for demo and testing purposes in
a small business network environment.
"""

import random
from datetime import datetime, timedelta

# Sample realistic hostnames for small business endpoints
HOSTNAMES = [
    "MSME-PC-01",
    "ACCOUNTS-WIN",
    "INVENTORY-LINUX",
    "CEO-MACBOOK",
    "RECEPTION-DESK",
    "SERVER-MAIN",
    "POS-TERMINAL-1",
    "HR-DESK-02",
    "DEV-WORKSTATION-1",
    "LOGISTICS-PC",
]

OS_OPTIONS = ["Windows 11", "Windows 10", "macOS Monterey", "Ubuntu 22.04 LTS"]

AGENT_VERSIONS = ["v2.4.1", "v2.4.0", "v2.3.9"]

INTERNAL_IP_PREFIXES = ["192.168.1.", "10.0.4."]
EXTERNAL_IPS = [
    "8.8.8.8",
    "1.1.1.1",
    "142.250.190.46",
    "13.107.42.14",
    "52.223.41.5",
    "104.16.249.249",
    "185.199.108.153",
]

MALICIOUS_IPS = [
    "45.142.214.193",
    "193.27.228.27",
    "185.220.101.5",
    "194.26.29.114",
    "91.240.118.172",
]


def _get_random_internal_ip() -> str:
    prefix = random.choice(INTERNAL_IP_PREFIXES)
    return f"{prefix}{random.randint(10, 250)}"


def generate_safe_events(count: int = 20) -> list[dict]:
    """Generates a list of simulated benign/safe EDR events.

    Args:
        count: Number of events to generate.

    Returns:
        List of dictionaries containing event properties.
    """
    events = []
    now = datetime.now()

    safe_descriptions = [
        "DNS lookup for internal portal resolved successfully",
        "HTTPS connection established with trusted gateway",
        "Routine file backup completed for local documents",
        "User authentication succeeded via local domain controller",
        "System security update package downloaded and verified",
        "Scheduled antivirus quick scan completed - zero threats found",
        "Printer service started by local user daemon",
        "Outbound HTTPS traffic authorized to cloud storage",
        "Network interface reconnected automatically",
        "Browser process launched in sandbox mode",
    ]

    event_types = [
        "DNS Query",
        "HTTPS Connection",
        "File Access",
        "User Login",
        "Process Start",
        "System Service",
    ]

    for _ in range(count):
        time_offset = timedelta(minutes=random.randint(1, 1440))
        event_time = (now - time_offset).strftime("%Y-%m-%d %H:%M:%S")

        events.append(
            {
                "timestamp": event_time,
                "event_type": random.choice(event_types),
                "source_ip": _get_random_internal_ip(),
                "destination_ip": random.choice(EXTERNAL_IPS),
                "severity": random.choice(["low", "info"]),
                "status": "allowed",
                "agent_name": random.choice(HOSTNAMES),
                "description": random.choice(safe_descriptions),
            }
        )

    events.sort(key=lambda x: x["timestamp"], reverse=True)
    return events


def generate_threat_events(count: int = 5) -> list[dict]:
    """Generates a list of simulated security threat events (critical/high severity).

    Args:
        count: Number of threat events to generate.

    Returns:
        List of dictionaries containing threat event properties.
    """
    events = []
    now = datetime.now()

    threat_scenarios = [
        {
            "event_type": "Ransomware Detection",
            "description": "Ransomware detected: Rapid file encryption attempt blocked on local volume.",
            "severity": "critical",
            "status": "quarantined",
        },
        {
            "event_type": "Suspicious Execution",
            "description": "Suspicious file execution: Powershell obfuscated script execution prevented.",
            "severity": "high",
            "status": "blocked",
        },
        {
            "event_type": "Brute Force Attempt",
            "description": "Brute force attempt: 50+ failed RDP login attempts from unrecognized IP.",
            "severity": "high",
            "status": "blocked",
        },
        {
            "event_type": "Data Exfiltration",
            "description": "Data exfiltration attempt: Large unauthorized transfer to suspicious remote IP.",
            "severity": "critical",
            "status": "quarantined",
        },
        {
            "event_type": "Process Injection",
            "description": "Malicious process injection: Code injection attempt detected into lsass.exe process.",
            "severity": "critical",
            "status": "blocked",
        },
        {
            "event_type": "Malware Payload",
            "description": "Trojan dropper download blocked from known malicious domain.",
            "severity": "critical",
            "status": "quarantined",
        },
        {
            "event_type": "Privilege Escalation",
            "description": "Unauthorized local admin privilege escalation attempt thwarted.",
            "severity": "high",
            "status": "blocked",
        },
    ]

    for i in range(count):
        scenario = threat_scenarios[i % len(threat_scenarios)]
        time_offset = timedelta(minutes=random.randint(5, 720))
        event_time = (now - time_offset).strftime("%Y-%m-%d %H:%M:%S")

        events.append(
            {
                "timestamp": event_time,
                "event_type": scenario["event_type"],
                "source_ip": _get_random_internal_ip(),
                "destination_ip": random.choice(MALICIOUS_IPS),
                "severity": scenario["severity"],
                "status": scenario["status"],
                "agent_name": random.choice(HOSTNAMES),
                "description": scenario["description"],
            }
        )

    events.sort(key=lambda x: x["timestamp"], reverse=True)
    return events


def generate_system_health() -> dict:
    """Generates normal system health metrics for a healthy network.

    Returns:
        Dict containing system usage stats, agent counts, and health status.
    """
    now = datetime.now()
    active = random.randint(3, 15)

    return {
        "cpu_usage": round(random.uniform(10.0, 45.0), 1),
        "memory_usage": round(random.uniform(20.0, 60.0), 1),
        "disk_usage": round(random.uniform(30.0, 70.0), 1),
        "active_agents": active,
        "online_agents": active,
        "offline_agents": random.randint(0, 2),
        "last_scan": (now - timedelta(minutes=random.randint(5, 30))).strftime("%Y-%m-%d %H:%M:%S"),
        "threats_blocked_today": 0,
        "vulnerabilities_found": 0,
        "compliance_score": round(random.uniform(85.0, 99.0), 1),
    }


def generate_threat_health() -> dict:
    """Generates elevated risk system health metrics representing an active threat environment.

    Returns:
        Dict containing elevated system load, active threat counts, and degraded health status.
    """
    now = datetime.now()
    active = random.randint(5, 15)
    offline = random.randint(1, 4)

    return {
        "cpu_usage": round(random.uniform(60.0, 95.0), 1),
        "memory_usage": round(random.uniform(50.0, 85.0), 1),
        "disk_usage": round(random.uniform(55.0, 88.0), 1),
        "active_agents": active,
        "online_agents": max(0, active - offline),
        "offline_agents": offline,
        "last_scan": (now - timedelta(minutes=random.randint(1, 15))).strftime("%Y-%m-%d %H:%M:%S"),
        "threats_blocked_today": random.randint(1, 5),
        "vulnerabilities_found": random.randint(2, 8),
        "compliance_score": round(random.uniform(40.0, 70.0), 1),
    }


def generate_agent_list(count: int = 8) -> list[dict]:
    """Generates a list of connected endpoint agents.

    Args:
        count: Number of agents to generate.

    Returns:
        List of dictionaries with agent details.
    """
    agents = []
    now = datetime.now()
    selected_hosts = random.sample(HOSTNAMES, min(count, len(HOSTNAMES)))

    for host in selected_hosts:
        is_online = random.random() > 0.15
        status = "online" if is_online else "offline"

        if is_online:
            last_seen = (now - timedelta(seconds=random.randint(10, 300))).strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_seen = (now - timedelta(hours=random.randint(2, 48))).strftime("%Y-%m-%d %H:%M:%S")

        agents.append(
            {
                "hostname": host,
                "os": random.choice(OS_OPTIONS),
                "ip_address": _get_random_internal_ip(),
                "status": status,
                "last_seen": last_seen,
                "agent_version": random.choice(AGENT_VERSIONS),
                "threats_detected": 0 if random.random() > 0.2 else random.randint(1, 3),
            }
        )

    return agents


def generate_timeline_data(days: int = 30) -> list[dict]:
    """Generates daily security event counts over a historical period for timeline charting.

    Args:
        days: Number of historical days to generate data for.

    Returns:
        List of dicts with 'date' (YYYY-MM-DD) and 'event_count'.
    """
    timeline = []
    today = datetime.now().date()

    for i in range(days - 1, -1, -1):
        event_date = today - timedelta(days=i)
        base_count = random.randint(12, 45)
        if random.random() < 0.1:
            base_count += random.randint(30, 80)

        timeline.append(
            {
                "date": event_date.strftime("%Y-%m-%d"),
                "event_count": base_count,
            }
        )

    return timeline
