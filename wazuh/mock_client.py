"""
Wazuh Mock Client
=================
Provides the same interface as WazuhClient but returns realistic simulated data.
Used in demo mode when no real Wazuh Manager is available.
"""

import random
from datetime import datetime, timedelta


class MockWazuhClient:
    """Mock implementation of WazuhClient for demonstration purposes."""

    def __init__(self):
        self._threat_mode = False

    def set_threat_mode(self, enabled: bool) -> None:
        self._threat_mode = enabled

    # ─── Authentication ───
    def authenticate(self) -> bool:
        return True

    def test_connection(self) -> dict:
        return {
            "connected": True,
            "version": "Wazuh v4.14.6 (Demo Mode)",
            "message": "Running in demo mode — no real Wazuh server connected",
        }

    # ─── Agent Management ───
    def get_agents(self, limit=500, offset=0, status=None) -> dict:
        agents = [
            {"id": "001", "name": "MSME-PC-01", "ip": "192.168.1.101",
             "os": {"name": "Windows", "version": "11 Pro", "platform": "windows"},
             "status": "active", "version": "Wazuh v4.14.6",
             "lastKeepAlive": (datetime.now() - timedelta(seconds=30)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "group": ["default", "windows"]},
            {"id": "002", "name": "ACCOUNTS-WIN", "ip": "192.168.1.102",
             "os": {"name": "Windows", "version": "10 Pro", "platform": "windows"},
             "status": "active", "version": "Wazuh v4.14.6",
             "lastKeepAlive": (datetime.now() - timedelta(seconds=45)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "group": ["default", "windows"]},
            {"id": "003", "name": "CEO-MACBOOK", "ip": "192.168.1.110",
             "os": {"name": "macOS", "version": "15.1 Sequoia", "platform": "darwin"},
             "status": "active", "version": "Wazuh v4.14.6",
             "lastKeepAlive": (datetime.now() - timedelta(seconds=60)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "group": ["default", "macos"]},
            {"id": "004", "name": "SERVER-MAIN", "ip": "192.168.1.10",
             "os": {"name": "Ubuntu", "version": "22.04 LTS", "platform": "linux"},
             "status": "active", "version": "Wazuh v4.14.6",
             "lastKeepAlive": (datetime.now() - timedelta(seconds=15)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "group": ["default", "linux", "servers"]},
            {"id": "005", "name": "POS-TERMINAL-1", "ip": "192.168.1.201",
             "os": {"name": "Windows", "version": "10 IoT", "platform": "windows"},
             "status": "active", "version": "Wazuh v4.14.5",
             "lastKeepAlive": (datetime.now() - timedelta(seconds=120)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "group": ["default", "windows", "pos"]},
            {"id": "006", "name": "HR-LAPTOP-02", "ip": "192.168.1.155",
             "os": {"name": "Windows", "version": "11 Home", "platform": "windows"},
             "status": "disconnected" if self._threat_mode else "active",
             "version": "Wazuh v4.14.6",
             "lastKeepAlive": (datetime.now() - timedelta(hours=2 if self._threat_mode else 0, seconds=90)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "group": ["default", "windows"]},
            {"id": "007", "name": "INVENTORY-LINUX", "ip": "192.168.1.20",
             "os": {"name": "CentOS", "version": "Stream 9", "platform": "linux"},
             "status": "active", "version": "Wazuh v4.14.6",
             "lastKeepAlive": (datetime.now() - timedelta(seconds=55)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "group": ["default", "linux"]},
            {"id": "008", "name": "RECEPTION-DESK", "ip": "192.168.1.160",
             "os": {"name": "Windows", "version": "10 Pro", "platform": "windows"},
             "status": "disconnected",
             "version": "Wazuh v4.14.4",
             "lastKeepAlive": (datetime.now() - timedelta(hours=48)).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "group": ["default", "windows"]},
        ]
        if status:
            agents = [a for a in agents if a["status"] == status]
        return {
            "data": {"affected_items": agents[:limit], "total_affected_items": len(agents)},
            "error": 0,
        }

    def get_agent(self, agent_id: str) -> dict:
        all_agents = self.get_agents()["data"]["affected_items"]
        for a in all_agents:
            if a["id"] == agent_id:
                return {"data": {"affected_items": [a]}, "error": 0}
        return {"data": {"affected_items": []}, "error": 0}

    def get_agent_summary(self) -> dict:
        agents = self.get_agents()["data"]["affected_items"]
        active = sum(1 for a in agents if a["status"] == "active")
        disconnected = sum(1 for a in agents if a["status"] == "disconnected")
        return {
            "data": {
                "active": active,
                "disconnected": disconnected,
                "never_connected": 0,
                "pending": 0,
                "total": len(agents),
            },
            "error": 0,
        }

    def restart_agent(self, agent_id: str) -> dict:
        return {"data": {"affected_items": [agent_id]}, "error": 0}

    def delete_agent(self, agent_id: str) -> dict:
        return {"data": {"affected_items": [agent_id]}, "error": 0}

    # ─── Manager / Cluster ───
    def get_manager_status(self) -> dict:
        return {
            "data": {
                "affected_items": [{
                    "wazuh-modulesd": "running",
                    "wazuh-analysisd": "running",
                    "wazuh-remoted": "running",
                    "wazuh-syscheckd": "running",
                    "wazuh-monitord": "running",
                    "wazuh-logcollector": "running",
                    "wazuh-execd": "running",
                    "wazuh-db": "running",
                    "wazuh-apid": "running",
                }]
            },
            "error": 0,
        }

    def get_manager_info(self) -> dict:
        return {
            "data": {
                "affected_items": [{
                    "version": "Wazuh v4.14.6",
                    "compilation_date": "2026-07-15T10:30:00Z",
                    "type": "manager",
                    "max_agents": "14000",
                    "tz_offset": "+0530",
                    "tz_name": "IST",
                }]
            },
            "error": 0,
        }

    def get_cluster_status(self) -> dict:
        return {"data": {"enabled": "no", "running": "no"}, "error": 0}

    def get_cluster_nodes(self) -> dict:
        return {"data": {"affected_items": []}, "error": 0}

    # ─── Vulnerability Detection ───
    def get_agent_vulnerabilities(self, agent_id: str, limit: int = 50) -> dict:
        vulns = [
            {"cve": "CVE-2026-21345", "name": "Windows Kerberos Elevation of Privilege", "severity": "High",
             "status": "Active", "detection_time": "2026-07-25T09:15:00Z",
             "package": {"name": "Windows", "version": "10.0.26100"}},
            {"cve": "CVE-2026-1823", "name": "OpenSSL Buffer Overflow", "severity": "Critical",
             "status": "Active", "detection_time": "2026-07-26T14:22:00Z",
             "package": {"name": "openssl", "version": "3.1.4"}},
            {"cve": "CVE-2025-49821", "name": "Apache Log4j Remote Code Execution", "severity": "Critical",
             "status": "Resolved", "detection_time": "2026-07-20T08:00:00Z",
             "package": {"name": "log4j-core", "version": "2.17.0"}},
            {"cve": "CVE-2026-3347", "name": "Chrome V8 Type Confusion", "severity": "Medium",
             "status": "Active", "detection_time": "2026-07-27T06:30:00Z",
             "package": {"name": "google-chrome", "version": "128.0.6613.84"}},
            {"cve": "CVE-2025-12345", "name": "Python pip Install Script Injection", "severity": "Low",
             "status": "Resolved", "detection_time": "2026-07-18T11:45:00Z",
             "package": {"name": "pip", "version": "25.3"}},
        ]
        if self._threat_mode:
            for v in vulns:
                v["status"] = "Active"
        return {
            "data": {"affected_items": vulns[:limit], "total_affected_items": len(vulns)},
            "error": 0,
        }

    # ─── FIM ───
    def get_fim_events(self, agent_id: str, limit: int = 50) -> dict:
        events = [
            {"file": "/etc/passwd", "event": "modified", "date": "2026-07-27T10:00:00Z",
             "size_after": 2048, "md5_after": "a1b2c3d4e5f6", "uid_after": "0", "perm_after": "0644"},
            {"file": "C:\\Windows\\System32\\config\\SAM", "event": "modified",
             "date": "2026-07-27T09:30:00Z", "size_after": 65536, "md5_after": "f6e5d4c3b2a1"},
            {"file": "/var/log/auth.log", "event": "modified", "date": "2026-07-27T10:15:00Z",
             "size_after": 1048576, "md5_after": "1a2b3c4d5e6f"},
        ]
        if self._threat_mode:
            events.append({
                "file": "C:\\Users\\Admin\\Documents\\budget.xlsx.locked",
                "event": "added", "date": "2026-07-27T10:25:00Z",
                "size_after": 0, "md5_after": "deadbeef0000",
            })
        return {
            "data": {"affected_items": events[:limit], "total_affected_items": len(events)},
            "error": 0,
        }

    # ─── SCA ───
    def get_sca_results(self, agent_id: str) -> dict:
        return {
            "data": {
                "affected_items": [
                    {"policy_id": "cis_win2022", "name": "CIS Benchmark for Windows Server 2022",
                     "pass": 142, "fail": 8 if not self._threat_mode else 23,
                     "invalid": 3, "total_checks": 153, "score": 93 if not self._threat_mode else 67,
                     "end_scan": "2026-07-27T10:00:00Z"},
                    {"policy_id": "cis_ubuntu22", "name": "CIS Benchmark for Ubuntu 22.04",
                     "pass": 98, "fail": 5 if not self._threat_mode else 18,
                     "invalid": 2, "total_checks": 105, "score": 93 if not self._threat_mode else 72,
                     "end_scan": "2026-07-27T09:45:00Z"},
                ],
            },
            "error": 0,
        }

    # ─── Rules ───
    def get_rules(self, limit: int = 50, level: str | None = None) -> dict:
        rules = [
            {"id": 5715, "level": 5, "description": "User logged in to the system", "groups": ["authentication"]},
            {"id": 5716, "level": 3, "description": "Successful sudo to ROOT executed", "groups": ["authentication"]},
            {"id": 550, "level": 7, "description": "Integrity checksum changed", "groups": ["syscheck"]},
            {"id": 554, "level": 10, "description": "File added to the system", "groups": ["syscheck"]},
            {"id": 5710, "level": 10, "description": "Multiple failed login attempts", "groups": ["authentication"]},
            {"id": 87924, "level": 12, "description": "Possible ransomware activity detected", "groups": ["malware"]},
            {"id": 87900, "level": 14, "description": "Trojan detected in system directory", "groups": ["malware"]},
        ]
        return {
            "data": {"affected_items": rules[:limit], "total_affected_items": len(rules)},
            "error": 0,
        }

    def get_rule(self, rule_id: str) -> dict:
        return self.get_rules(limit=100)

    # ─── Active Response ───
    def run_active_response(self, agent_id: str, command: str, arguments: list | None = None) -> dict:
        return {"data": {"affected_items": [agent_id]}, "message": f"Active response '{command}' sent", "error": 0}

    def run_fim_scan(self, agent_id: str) -> dict:
        return {"data": {"affected_items": [agent_id]}, "error": 0}

    # ─── Alerts (simulated) ───
    def get_alerts(self, time_range_minutes=1440, severity_min=0, limit=50, agent_id=None) -> list[dict]:
        now = datetime.now()
        safe_alerts = [
            {"timestamp": (now - timedelta(minutes=random.randint(5, 1400))).isoformat(),
             "agent": {"id": "001", "name": "MSME-PC-01", "ip": "192.168.1.101"},
             "rule": {"level": 3, "description": "User authentication success", "id": "5715",
                      "groups": ["authentication"]},
             "data": {"srcip": "192.168.1.1"}},
            {"timestamp": (now - timedelta(minutes=random.randint(5, 1400))).isoformat(),
             "agent": {"id": "004", "name": "SERVER-MAIN", "ip": "192.168.1.10"},
             "rule": {"level": 5, "description": "File integrity checksum changed", "id": "550",
                      "groups": ["syscheck"]},
             "data": {"file": "/etc/hosts"}},
            {"timestamp": (now - timedelta(minutes=random.randint(5, 1400))).isoformat(),
             "agent": {"id": "002", "name": "ACCOUNTS-WIN", "ip": "192.168.1.102"},
             "rule": {"level": 3, "description": "New Windows service installed", "id": "5100",
                      "groups": ["windows"]},
             "data": {"service": "wuauserv"}},
            {"timestamp": (now - timedelta(minutes=random.randint(5, 1400))).isoformat(),
             "agent": {"id": "003", "name": "CEO-MACBOOK", "ip": "192.168.1.110"},
             "rule": {"level": 2, "description": "Successful sudo command executed", "id": "5716",
                      "groups": ["authentication"]},
             "data": {"srcuser": "admin"}},
        ]

        threat_alerts = []
        if self._threat_mode:
            threat_alerts = [
                {"timestamp": (now - timedelta(minutes=random.randint(1, 30))).isoformat(),
                 "agent": {"id": "001", "name": "MSME-PC-01", "ip": "192.168.1.101"},
                 "rule": {"level": 14, "description": "Ransomware activity: rapid file encryption detected", "id": "87924",
                          "groups": ["malware", "ransomware"]},
                 "data": {"srcip": "45.142.214.193", "file": "C:\\Users\\budget.xlsx.locked"}},
                {"timestamp": (now - timedelta(minutes=random.randint(1, 30))).isoformat(),
                 "agent": {"id": "006", "name": "HR-LAPTOP-02", "ip": "192.168.1.155"},
                 "rule": {"level": 12, "description": "Multiple failed SSH login attempts from external IP", "id": "5710",
                          "groups": ["authentication", "brute_force"]},
                 "data": {"srcip": "193.27.228.27"}},
                {"timestamp": (now - timedelta(minutes=random.randint(1, 30))).isoformat(),
                 "agent": {"id": "004", "name": "SERVER-MAIN", "ip": "192.168.1.10"},
                 "rule": {"level": 15, "description": "Trojan dropper detected in system32 directory", "id": "87900",
                          "groups": ["malware"]},
                 "data": {"srcip": "185.220.101.5", "file": "/tmp/.hidden_payload"}},
                {"timestamp": (now - timedelta(minutes=random.randint(1, 30))).isoformat(),
                 "agent": {"id": "005", "name": "POS-TERMINAL-1", "ip": "192.168.1.201"},
                 "rule": {"level": 13, "description": "Data exfiltration: large outbound transfer to suspicious IP", "id": "88001",
                          "groups": ["data_exfiltration"]},
                 "data": {"srcip": "192.168.1.201", "dstip": "194.26.29.114"}},
            ]

        all_alerts = safe_alerts + threat_alerts
        all_alerts = [a for a in all_alerts if a["rule"]["level"] >= severity_min]
        if agent_id:
            all_alerts = [a for a in all_alerts if a["agent"]["id"] == agent_id]
        all_alerts.sort(key=lambda x: x["timestamp"], reverse=True)
        return all_alerts[:limit]
