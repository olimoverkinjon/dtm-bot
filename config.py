"""
Configuration module for DTM Bot
Equivalent to: config.php

This module contains all configuration settings and helper functions
for the Telegram bot application.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================
# 🔥 CONFIGURATION
# ==================

# Telegram API Configuration
API_TOKEN = os.getenv("API_TOKEN", "8516827967:AAHDYsWDsYrsM3HBna24ceonbpM9a8zb_Yw")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@registan_abituriyent")
GROUP_ID = int(os.getenv("GROUP_ID", "-1003890628671"))

# Admin IDs (multiple admins supported)
ADMIN_IDS = [
    int(os.getenv("ADMIN_ID", "6653845419")),
    int(os.getenv("ADMIN_ID_2", "5240893523"))
]

# Legacy single admin ID (for backward compatibility)
ADMIN_ID = ADMIN_IDS[0]

# File Storage Paths
LEADS_FILE = Path(__file__).parent / "leads.json"
SESSIONS_FILE = Path(__file__).parent / "sessions.json"

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================
# 💾 HELPER FUNCTIONS
# ==================

def get_leads() -> List[Dict]:
    """
    Get leads from JSON file
    Equivalent to: getLeads() in PHP
    """
    if LEADS_FILE.exists():
        try:
            with open(LEADS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f) or []
        except Exception as e:
            logger.error(f"Error reading leads: {e}")
            return []
    return []


def save_leads(leads: List[Dict]) -> None:
    """
    Save leads to JSON file
    Equivalent to: saveLeads() in PHP
    """
    try:
        with open(LEADS_FILE, 'w', encoding='utf-8') as f:
            json.dump(leads, f, ensure_ascii=False, indent=2)
        logger.info(f"Leads saved: {len(leads)} total")
    except Exception as e:
        logger.error(f"Error saving leads: {e}")


def add_lead(name: str, phone: str, extra_phone: str) -> None:
    """
    Add new lead to storage
    Equivalent to: addLead() in PHP
    """
    leads = get_leads()
    leads.append({
        'name': name,
        'phone': phone,
        'extra': extra_phone,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_leads(leads)
    logger.info(f"New lead added: {name}")


def get_sessions() -> Dict:
    """
    Get all sessions from JSON file
    Equivalent to: getSession() in PHP
    """
    if SESSIONS_FILE.exists():
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f) or {}
        except Exception as e:
            logger.error(f"Error reading sessions: {e}")
            return {}
    return {}


def get_session(user_id: int) -> Dict:
    """
    Get specific user session
    Equivalent to: getSession() in PHP
    """
    sessions = get_sessions()
    return sessions.get(str(user_id), {})


def save_session(user_id: int, state: str, data: Optional[Dict] = None) -> None:
    """
    Save user session
    Equivalent to: saveSession() in PHP
    """
    sessions = get_sessions()
    sessions[str(user_id)] = {
        'state': state,
        'data': data or {}
    }
    try:
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
        logger.debug(f"Session saved for user {user_id}: state={state}")
    except Exception as e:
        logger.error(f"Error saving session: {e}")


def delete_session(user_id: int) -> None:
    """
    Delete user session
    Equivalent to: deleteSession() in PHP
    """
    sessions = get_sessions()
    if str(user_id) in sessions:
        del sessions[str(user_id)]
    try:
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
        logger.debug(f"Session deleted for user {user_id}")
    except Exception as e:
        logger.error(f"Error deleting session: {e}")


# ==================
# 🧹 UTILITY FUNCTIONS
# ==================

def sanitize_input(text: str) -> str:
    """
    Sanitize user input for safety
    Equivalent to: htmlspecialchars() in PHP
    """
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    - Must contain only digits
    - Minimum 7 digits
    """
    return phone.isdigit() and len(phone) >= 7


def get_leads_count() -> int:
    """Get total number of leads"""
    return len(get_leads())


def get_recent_leads(count: int = 5) -> List[Dict]:
    """Get recent leads"""
    leads = get_leads()
    return leads[-count:] if leads else []


def export_leads_to_csv(filepath: str = "leads_export.csv") -> None:
    """Export leads to CSV file"""
    import csv
    leads = get_leads()
    
    if not leads:
        logger.warning("No leads to export")
        return
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'phone', 'extra', 'timestamp'])
            writer.writeheader()
            writer.writerows(leads)
        logger.info(f"Leads exported to {filepath}")
    except Exception as e:
        logger.error(f"Error exporting leads: {e}")


def clear_old_sessions(max_age_days: int = 30) -> None:
    """Clear sessions older than specified days"""
    sessions = get_sessions()
    cutoff_date = datetime.now().timestamp() - (max_age_days * 86400)
    
    # Sessions don't have timestamps, so this is a placeholder
    # In production, you'd add timestamps to sessions
    logger.info("Session cleanup check performed")


# ==================
# 📋 INITIALIZATION
# ==================

# Ensure data files exist
def initialize():
    """Initialize application files and logging"""
    # Create empty leads file if it doesn't exist
    if not LEADS_FILE.exists():
        save_leads([])
        logger.info(f"Created leads file: {LEADS_FILE}")
    
    # Create empty sessions file if it doesn't exist
    if not SESSIONS_FILE.exists():
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        logger.info(f"Created sessions file: {SESSIONS_FILE}")


if __name__ == "__main__":
    # Test configuration when run directly
    initialize()
    print(f"✅ Configuration loaded successfully")
    print(f"  API Token: {API_TOKEN[:20]}...")
    print(f"  Channel: {CHANNEL_USERNAME}")
    print(f"  Group ID: {GROUP_ID}")
    print(f"  Admin ID: {ADMIN_ID}")
    print(f"  Leads file: {LEADS_FILE}")
    print(f"  Sessions file: {SESSIONS_FILE}")
    print(f"  Total leads: {get_leads_count()}")
