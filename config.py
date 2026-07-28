"""
ShieldEDR Configuration
=======================
Central config for Wazuh API connection and application settings.
Reads from environment variables or falls back to defaults.
"""

import os

# ── Wazuh Manager API ──
WAZUH_API_HOST = os.getenv("WAZUH_API_HOST", "localhost")
WAZUH_API_PORT = int(os.getenv("WAZUH_API_PORT", "55000"))
WAZUH_API_USER = os.getenv("WAZUH_API_USER", "wazuh-wui")
WAZUH_API_PASS = os.getenv("WAZUH_API_PASS", "wazuh-wui")
WAZUH_API_PROTO = os.getenv("WAZUH_API_PROTO", "https")
WAZUH_VERIFY_SSL = os.getenv("WAZUH_VERIFY_SSL", "false").lower() == "true"

# ── Wazuh Indexer (OpenSearch) ──
WAZUH_INDEXER_HOST = os.getenv("WAZUH_INDEXER_HOST", "localhost")
WAZUH_INDEXER_PORT = int(os.getenv("WAZUH_INDEXER_PORT", "9200"))
WAZUH_INDEXER_USER = os.getenv("WAZUH_INDEXER_USER", "admin")
WAZUH_INDEXER_PASS = os.getenv("WAZUH_INDEXER_PASS", "admin")

# ── Application Settings ──
APP_NAME = "ShieldEDR"
APP_VERSION = "3.0.0"
APP_TAGLINE = "Enterprise Security for Everyone"
DEMO_MODE = os.getenv("SHIELD_DEMO_MODE", "true").lower() == "true"

# ── Wazuh API base URL ──
WAZUH_API_BASE = f"{WAZUH_API_PROTO}://{WAZUH_API_HOST}:{WAZUH_API_PORT}"
WAZUH_INDEXER_BASE = f"https://{WAZUH_INDEXER_HOST}:{WAZUH_INDEXER_PORT}"


def get_wazuh_base_url() -> str:
    """Returns the Wazuh Manager API base URL."""
    return WAZUH_API_BASE


def get_indexer_base_url() -> str:
    """Returns the Wazuh Indexer API base URL."""
    return WAZUH_INDEXER_BASE
