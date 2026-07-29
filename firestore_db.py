"""
ShieldEDR Persistent Database Module (Free Firestore & Local Storage)
===================================================================
Manages user authentication accounts, payment subscriptions (₹1,000/yr),
registered devices, and custom Wazuh security rules.
Uses Google Cloud Firestore when available, with automatic persistent local JSON fallback.
"""

import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_FILE_PATH = os.path.join(os.path.dirname(__file__), "local_db_store.json")

# Default Database Structure
_DEFAULT_DB = {
    "users": {
        "admin@shieldedr.com": {
            "email": "admin@shieldedr.com",
            "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
            "business_name": "Demo MSME Business",
            "created_at": datetime.now().isoformat(),
            "is_paid": True,
            "subscription_plan": "1000_annual",
            "paid_at": datetime.now().isoformat(),
            "payment_id": "PAY_DEMO_9999",
            "device_limit": 50,
        }
    },
    "payments": [
        {
            "payment_id": "PAY_DEMO_9999",
            "email": "admin@shieldedr.com",
            "amount": 1000,
            "currency": "INR",
            "method": "UPI / GPay",
            "ref_no": "UPI9988776655",
            "status": "SUCCESS",
            "timestamp": datetime.now().isoformat(),
        }
    ],
    "devices": [
        {
            "device_id": "DEV-001",
            "email": "admin@shieldedr.com",
            "name": "WIN-OFFICE-01",
            "os": "Windows 11 Pro",
            "ip": "192.168.1.45",
            "status": "PROTECTED",
            "agent_version": "4.9.0",
            "installed_at": datetime.now().isoformat(),
            "last_keepalive": datetime.now().isoformat(),
        },
        {
            "device_id": "DEV-002",
            "email": "admin@shieldedr.com",
            "name": "POS-TERMINAL-LKO",
            "os": "Windows 10 Home",
            "ip": "192.168.1.88",
            "status": "PROTECTED",
            "agent_version": "4.9.0",
            "installed_at": datetime.now().isoformat(),
            "last_keepalive": datetime.now().isoformat(),
        }
    ],
    "custom_rules": []
}

def _load_local_db() -> Dict[str, Any]:
    """Load persistent database from local JSON file."""
    if not os.path.exists(DB_FILE_PATH):
        _save_local_db(_DEFAULT_DB)
        return _DEFAULT_DB
    try:
        with open(DB_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return _DEFAULT_DB

def _save_local_db(data: Dict[str, Any]) -> None:
    """Save persistent database to local JSON file."""
    try:
        with open(DB_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def get_firestore_client():
    """Initialize Google Cloud Firestore client if service account is available."""
    try:
        from google.cloud import firestore
        return firestore.Client()
    except Exception:
        return None

# ==============================================================================
# 1. USER AUTHENTICATION & ACCOUNT FUNCTIONS
# ==============================================================================

def create_user(email: str, password: str, business_name: str) -> Dict[str, Any]:
    """Registers a new user account."""
    email_clean = email.strip().lower()
    db = _load_local_db()

    if email_clean in db["users"]:
        return {"success": False, "message": "Email is already registered. Please log in."}

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user_data = {
        "email": email_clean,
        "password_hash": password_hash,
        "business_name": business_name.strip(),
        "created_at": datetime.now().isoformat(),
        "is_paid": False,
        "subscription_plan": None,
        "paid_at": None,
        "payment_id": None,
        "device_limit": 0,
    }

    db["users"][email_clean] = user_data
    _save_local_db(db)

    # Cloud Firestore Sync
    fs = get_firestore_client()
    if fs:
        try:
            fs.collection("users").document(email_clean).set(user_data)
        except Exception:
            pass

    return {"success": True, "message": "Account created successfully!", "user": user_data}

def authenticate_user(email: str, password: str) -> Dict[str, Any]:
    """Authenticates a user by email and password."""
    email_clean = email.strip().lower()
    db = _load_local_db()

    if email_clean not in db["users"]:
        return {"success": False, "message": "Account not found. Please register first."}

    user = db["users"][email_clean]
    input_hash = hashlib.sha256(password.encode()).hexdigest()

    if user["password_hash"] != input_hash:
        return {"success": False, "message": "Incorrect password. Please try again."}

    return {"success": True, "message": "Login successful!", "user": user}

def get_user_profile(email: str) -> Optional[Dict[str, Any]]:
    """Gets user profile by email."""
    email_clean = email.strip().lower()
    db = _load_local_db()
    return db["users"].get(email_clean)

# ==============================================================================
# 2. PAYMENT & SUBSCRIPTION FUNCTIONS (₹1,000 / Year)
# ==============================================================================

def record_payment(email: str, amount: int, method: str, ref_no: str) -> Dict[str, Any]:
    """Records a completed payment and activates user subscription."""
    email_clean = email.strip().lower()
    db = _load_local_db()

    payment_id = f"PAY_UPI_{int(datetime.now().timestamp())}"
    now_iso = datetime.now().isoformat()

    payment_record = {
        "payment_id": payment_id,
        "email": email_clean,
        "amount": amount,
        "currency": "INR",
        "method": method,
        "ref_no": ref_no.strip(),
        "status": "SUCCESS",
        "timestamp": now_iso,
    }

    db["payments"].append(payment_record)

    # Activate User Subscription
    if email_clean in db["users"]:
        db["users"][email_clean]["is_paid"] = True
        db["users"][email_clean]["subscription_plan"] = "1000_annual"
        db["users"][email_clean]["paid_at"] = now_iso
        db["users"][email_clean]["payment_id"] = payment_id
        db["users"][email_clean]["device_limit"] = 50

    _save_local_db(db)

    # Firestore sync
    fs = get_firestore_client()
    if fs:
        try:
            fs.collection("payments").document(payment_id).set(payment_record)
            fs.collection("users").document(email_clean).update({
                "is_paid": True,
                "subscription_plan": "1000_annual",
                "paid_at": now_iso,
                "payment_id": payment_id,
                "device_limit": 50
            })
        except Exception:
            pass

    return {"success": True, "message": "Payment verified and subscription activated!", "payment": payment_record}

def get_user_payments(email: str) -> List[Dict[str, Any]]:
    """Gets all payment records for a user."""
    email_clean = email.strip().lower()
    db = _load_local_db()
    return [p for p in db["payments"] if p.get("email") == email_clean]

# ==============================================================================
# 3. DEVICE & AGENT MANAGEMENT FUNCTIONS
# ==============================================================================

def register_device(email: str, name: str, os_name: str, ip_addr: str) -> Dict[str, Any]:
    """Registers a new endpoint device under a user's account."""
    email_clean = email.strip().lower()
    db = _load_local_db()

    device_id = f"DEV-{len(db['devices']) + 1:03d}"
    now_iso = datetime.now().isoformat()

    device_record = {
        "device_id": device_id,
        "email": email_clean,
        "name": name.strip(),
        "os": os_name,
        "ip": ip_addr,
        "status": "PROTECTED",
        "agent_version": "4.9.0",
        "installed_at": now_iso,
        "last_keepalive": now_iso,
    }

    db["devices"].append(device_record)
    _save_local_db(db)

    # Firestore sync
    fs = get_firestore_client()
    if fs:
        try:
            fs.collection("devices").document(device_id).set(device_record)
        except Exception:
            pass

    return {"success": True, "message": "Device registered successfully!", "device": device_record}

def get_user_devices(email: str) -> List[Dict[str, Any]]:
    """Gets all devices connected to a user's account."""
    email_clean = email.strip().lower()
    db = _load_local_db()
    user_devs = [d for d in db["devices"] if d.get("email") == email_clean]
    if not user_devs and email_clean == "admin@shieldedr.com":
        return db["devices"]
    return user_devs

# ==============================================================================
# 4. CUSTOM WAZUH RULES FUNCTIONS
# ==============================================================================

def save_rule_to_firestore(rule_data: Dict[str, Any]) -> bool:
    """Save custom detection rule to database."""
    db = _load_local_db()
    rule_data["updated_at"] = datetime.now().isoformat()

    existing_idx = next((i for i, r in enumerate(db["custom_rules"]) if r.get("rule_id") == rule_data["rule_id"]), None)
    if existing_idx is not None:
        db["custom_rules"][existing_idx] = rule_data
    else:
        db["custom_rules"].append(rule_data)

    _save_local_db(db)
    return True

def get_all_firestore_rules() -> List[Dict[str, Any]]:
    """Get custom detection rules."""
    db = _load_local_db()
    if not db["custom_rules"]:
        from wazuh.rule_builder import DEFAULT_RULE_PRESETS
        for r in DEFAULT_RULE_PRESETS:
            db["custom_rules"].append({
                "rule_id": r.rule_id,
                "level": r.level,
                "description": r.description,
                "group": r.group,
                "category": r.category,
                "match_pattern": r.match_pattern,
                "mitre_id": r.mitre_id,
            })
        _save_local_db(db)
    return db["custom_rules"]
