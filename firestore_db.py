"""
Firestore Database Storage Module
=================================
Persists custom security rules, business configuration profiles, and alert logs to Google Cloud Firestore.
Provides local memory/JSON fallback when running offline or without GCP service account credentials.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Global memory cache for fallback mode
_LOCAL_RULES_CACHE: List[Dict[str, Any]] = []
_LOCAL_CONFIG_CACHE: Dict[str, Any] = {
    "business_name": "MSME Small Business",
    "endpoint_limit": 50,
    "active_tier": "Pro Protection",
    "updated_at": datetime.now().isoformat(),
}


def get_firestore_client():
    """Attempt to initialize Google Cloud Firestore client."""
    try:
        from google.cloud import firestore
        db = firestore.Client()
        return db
    except Exception:
        return None


def save_rule_to_firestore(rule_data: Dict[str, Any]) -> bool:
    """Save or update a custom detection rule in Firestore.

    Args:
        rule_data: Dict containing rule_id, level, description, match_pattern, category, etc.

    Returns:
        True if saved successfully (Firestore or fallback cache).
    """
    db = get_firestore_client()
    rule_data["updated_at"] = datetime.now().isoformat()

    if db:
        try:
            doc_ref = db.collection("custom_wazuh_rules").document(str(rule_data["rule_id"]))
            doc_ref.set(rule_data)
            return True
        except Exception:
            pass

    # Fallback to local memory cache
    existing_idx = next((i for i, r in enumerate(_LOCAL_RULES_CACHE) if r.get("rule_id") == rule_data["rule_id"]), None)
    if existing_idx is not None:
        _LOCAL_RULES_CACHE[existing_idx] = rule_data
    else:
        _LOCAL_RULES_CACHE.append(rule_data)
    return True


def get_all_firestore_rules() -> List[Dict[str, Any]]:
    """Retrieve all custom detection rules from Firestore or local fallback cache."""
    db = get_firestore_client()
    if db:
        try:
            docs = db.collection("custom_wazuh_rules").stream()
            rules = [doc.to_dict() for doc in docs]
            if rules:
                return rules
        except Exception:
            pass

    # Return local cache or default presets
    if not _LOCAL_RULES_CACHE:
        from wazuh.rule_builder import DEFAULT_RULE_PRESETS
        for r in DEFAULT_RULE_PRESETS:
            _LOCAL_RULES_CACHE.append({
                "rule_id": r.rule_id,
                "level": r.level,
                "description": r.description,
                "group": r.group,
                "category": r.category,
                "match_pattern": r.match_pattern,
                "mitre_id": r.mitre_id,
            })
    return _LOCAL_RULES_CACHE


def save_tenant_config(config_data: Dict[str, Any]) -> bool:
    """Save business tenant configuration to Firestore."""
    db = get_firestore_client()
    config_data["updated_at"] = datetime.now().isoformat()

    if db:
        try:
            db.collection("tenant_configs").document("default_tenant").set(config_data)
            return True
        except Exception:
            pass

    _LOCAL_CONFIG_CACHE.update(config_data)
    return True


def get_tenant_config() -> Dict[str, Any]:
    """Get tenant configuration from Firestore or local cache."""
    db = get_firestore_client()
    if db:
        try:
            doc = db.collection("tenant_configs").document("default_tenant").get()
            if doc.exists:
                return doc.to_dict()
        except Exception:
            pass
    return _LOCAL_CONFIG_CACHE
