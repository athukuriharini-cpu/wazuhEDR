"""
Wazuh REST API Client
=====================
Connects to a real Wazuh Manager API (port 55000) and Wazuh Indexer (port 9200).
Handles JWT authentication, token refresh, and provides methods for all major endpoints.

Usage:
    from wazuh.client import WazuhClient
    client = WazuhClient()
    client.authenticate()
    agents = client.get_agents()
"""

import requests
import urllib3
from datetime import datetime, timedelta
from typing import Any

# Suppress insecure HTTPS warnings for self-signed Wazuh certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WazuhClient:
    """Client for the Wazuh Manager REST API (v4.x)."""

    def __init__(
        self,
        api_host: str = "localhost",
        api_port: int = 55000,
        api_user: str = "wazuh-wui",
        api_pass: str = "wazuh-wui",
        protocol: str = "https",
        verify_ssl: bool = False,
        indexer_host: str = "localhost",
        indexer_port: int = 9200,
        indexer_user: str = "admin",
        indexer_pass: str = "admin",
    ):
        self.api_base = f"{protocol}://{api_host}:{api_port}"
        self.api_user = api_user
        self.api_pass = api_pass
        self.verify_ssl = verify_ssl
        self.token: str | None = None
        self.token_expiry: datetime | None = None

        # Indexer config
        self.indexer_base = f"https://{indexer_host}:{indexer_port}"
        self.indexer_user = indexer_user
        self.indexer_pass = indexer_pass

    # ─────────────────────────────────────
    # Authentication
    # ─────────────────────────────────────
    def authenticate(self) -> bool:
        """Authenticate with Wazuh API and obtain a JWT token.

        Returns:
            True if authentication succeeded, False otherwise.
        """
        try:
            resp = requests.get(
                f"{self.api_base}/security/user/authenticate",
                auth=(self.api_user, self.api_pass),
                verify=self.verify_ssl,
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                self.token = data.get("data", {}).get("token", "")
                # Wazuh tokens typically expire in 900 seconds (15 min)
                self.token_expiry = datetime.now() + timedelta(seconds=880)
                return True
            return False
        except requests.exceptions.ConnectionError:
            return False
        except Exception:
            return False

    def _ensure_token(self) -> None:
        """Refresh token if expired or missing."""
        if not self.token or (self.token_expiry and datetime.now() >= self.token_expiry):
            self.authenticate()

    def _headers(self) -> dict:
        """Return authorization headers."""
        self._ensure_token()
        return {"Authorization": f"Bearer {self.token}"}

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        """Make an authenticated GET request to the Wazuh Manager API.

        Args:
            endpoint: API path (e.g., '/agents')
            params: Optional query parameters

        Returns:
            JSON response as dict, or error dict on failure.
        """
        try:
            resp = requests.get(
                f"{self.api_base}{endpoint}",
                headers=self._headers(),
                params=params,
                verify=self.verify_ssl,
                timeout=15,
            )
            return resp.json()
        except Exception as e:
            return {"error": 1, "message": str(e)}

    def _put(self, endpoint: str, json_body: dict | None = None) -> dict:
        """Make an authenticated PUT request."""
        try:
            resp = requests.put(
                f"{self.api_base}{endpoint}",
                headers=self._headers(),
                json=json_body,
                verify=self.verify_ssl,
                timeout=15,
            )
            return resp.json()
        except Exception as e:
            return {"error": 1, "message": str(e)}

    # ─────────────────────────────────────
    # Agent Management
    # ─────────────────────────────────────
    def get_agents(self, limit: int = 500, offset: int = 0, status: str | None = None) -> dict:
        """List all registered agents.

        Args:
            limit: Max number of agents to return.
            offset: Pagination offset.
            status: Filter by status ('active', 'disconnected', 'never_connected', 'pending').

        Returns:
            API response with agent list under data.affected_items.
        """
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        return self._get("/agents", params)

    def get_agent(self, agent_id: str) -> dict:
        """Get details for a specific agent."""
        return self._get(f"/agents/{agent_id}")

    def get_agent_summary(self) -> dict:
        """Get agent status summary counts (active, disconnected, etc.)."""
        return self._get("/agents/summary/status")

    def delete_agent(self, agent_id: str) -> dict:
        """Delete an agent by ID."""
        try:
            resp = requests.delete(
                f"{self.api_base}/agents",
                headers=self._headers(),
                params={"agents_list": agent_id, "status": "all", "older_than": "0s"},
                verify=self.verify_ssl,
                timeout=15,
            )
            return resp.json()
        except Exception as e:
            return {"error": 1, "message": str(e)}

    def restart_agent(self, agent_id: str) -> dict:
        """Restart a specific agent."""
        return self._put(f"/agents/{agent_id}/restart")

    # ─────────────────────────────────────
    # Manager / Cluster
    # ─────────────────────────────────────
    def get_manager_status(self) -> dict:
        """Get running status of all Wazuh manager daemons."""
        return self._get("/manager/status")

    def get_manager_info(self) -> dict:
        """Get manager version and general information."""
        return self._get("/manager/info")

    def get_cluster_status(self) -> dict:
        """Get cluster enabled/disabled status."""
        return self._get("/cluster/status")

    def get_cluster_nodes(self) -> dict:
        """List cluster nodes."""
        return self._get("/cluster/nodes")

    # ─────────────────────────────────────
    # Vulnerability Detection
    # ─────────────────────────────────────
    def get_agent_vulnerabilities(self, agent_id: str, limit: int = 50) -> dict:
        """Get detected vulnerabilities for an agent.

        Args:
            agent_id: The agent ID.
            limit: Max number of results.
        """
        return self._get(f"/vulnerability/{agent_id}", {"limit": limit})

    # ─────────────────────────────────────
    # File Integrity Monitoring (FIM / Syscheck)
    # ─────────────────────────────────────
    def get_fim_events(self, agent_id: str, limit: int = 50) -> dict:
        """Get FIM/Syscheck events for an agent."""
        return self._get(f"/syscheck/{agent_id}", {"limit": limit})

    def run_fim_scan(self, agent_id: str) -> dict:
        """Trigger a FIM scan on an agent."""
        return self._put(f"/syscheck/{agent_id}")

    # ─────────────────────────────────────
    # Security Configuration Assessment
    # ─────────────────────────────────────
    def get_sca_results(self, agent_id: str) -> dict:
        """Get SCA policy check results for an agent."""
        return self._get(f"/sca/{agent_id}")

    # ─────────────────────────────────────
    # Rules
    # ─────────────────────────────────────
    def get_rules(self, limit: int = 50, level: str | None = None) -> dict:
        """List detection rules.

        Args:
            limit: Max number of rules to return.
            level: Filter by rule level range (e.g., '10-15' for high severity).
        """
        params: dict[str, Any] = {"limit": limit}
        if level:
            params["level"] = level
        return self._get("/rules", params)

    def get_rule(self, rule_id: str) -> dict:
        """Get a specific rule by ID."""
        return self._get(f"/rules/{rule_id}")

    # ─────────────────────────────────────
    # Active Response
    # ─────────────────────────────────────
    def run_active_response(self, agent_id: str, command: str, arguments: list | None = None) -> dict:
        """Execute an active response command on an agent.

        Args:
            agent_id: Target agent ID.
            command: Active response command name.
            arguments: Optional list of command arguments.
        """
        body: dict[str, Any] = {"command": command, "arguments": arguments or []}
        return self._put(f"/active-response/{agent_id}", body)

    # ─────────────────────────────────────
    # Alerts (via Wazuh Indexer / OpenSearch)
    # ─────────────────────────────────────
    def get_alerts(
        self,
        time_range_minutes: int = 1440,
        severity_min: int = 0,
        limit: int = 50,
        agent_id: str | None = None,
    ) -> list[dict]:
        """Query alerts from the Wazuh Indexer (OpenSearch).

        Args:
            time_range_minutes: How far back to query (default 24 hours).
            severity_min: Minimum rule level to include.
            limit: Max alerts to return.
            agent_id: Optional filter by agent ID.

        Returns:
            List of alert source documents.
        """
        now = datetime.utcnow()
        start = now - timedelta(minutes=time_range_minutes)

        query: dict[str, Any] = {
            "size": limit,
            "sort": [{"timestamp": {"order": "desc"}}],
            "query": {
                "bool": {
                    "must": [
                        {"range": {"timestamp": {"gte": start.isoformat(), "lte": now.isoformat()}}},
                        {"range": {"rule.level": {"gte": severity_min}}},
                    ]
                }
            },
        }

        if agent_id:
            query["query"]["bool"]["must"].append({"match": {"agent.id": agent_id}})

        try:
            resp = requests.get(
                f"{self.indexer_base}/wazuh-alerts*/_search",
                auth=(self.indexer_user, self.indexer_pass),
                json=query,
                verify=self.verify_ssl,
                timeout=15,
            )
            data = resp.json()
            hits = data.get("hits", {}).get("hits", [])
            return [h.get("_source", {}) for h in hits]
        except Exception:
            return []

    # ─────────────────────────────────────
    # Connection Test
    # ─────────────────────────────────────
    def test_connection(self) -> dict:
        """Test if the Wazuh Manager API is reachable and credentials work.

        Returns:
            dict with 'connected' (bool), 'version', and 'message'.
        """
        try:
            auth_ok = self.authenticate()
            if not auth_ok:
                return {"connected": False, "version": None, "message": "Authentication failed"}

            info = self.get_manager_info()
            version = info.get("data", {}).get("affected_items", [{}])[0].get("version", "Unknown")
            return {"connected": True, "version": version, "message": "Connected successfully"}
        except Exception as e:
            return {"connected": False, "version": None, "message": str(e)}
