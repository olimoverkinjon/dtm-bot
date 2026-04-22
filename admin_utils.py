#!/usr/bin/env python3
"""
DTM Bot - Admin Utilities
Command-line tools for bot administration and lead management
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from tabulate import tabulate
import sys

from config import (
    get_leads, save_leads, get_leads_count,
    get_sessions, LEADS_FILE, SESSIONS_FILE, logger
)


def print_header(title: str):
    """Print section header"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}\n")


def show_leads():
    """Display all leads in table format"""
    leads = get_leads()
    
    if not leads:
        print("❌ No leads found")
        return
    
    # Prepare table data
    table_data = []
    for i, lead in enumerate(leads, 1):
        table_data.append([
            i,
            lead['name'],
            lead['phone'],
            lead['extra'],
            lead['timestamp']
        ])
    
    headers = ["#", "Name", "Phone", "Extra", "Timestamp"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def show_stats():
    """Display statistics"""
    leads = get_leads()
    sessions = get_sessions()
    
    print_header("📊 Statistics")
    print(f"Total Leads: {len(leads)}")
    print(f"Active Sessions: {len(sessions)}")
    print(f"Data File: {LEADS_FILE}")
    print(f"Sessions File: {SESSIONS_FILE}")
    
    if leads:
        latest = leads[-1]
        print(f"\nLatest Lead:")
        print(f"  Name: {latest['name']}")
        print(f"  Phone: {latest['phone']}")
        print(f"  Time: {latest['timestamp']}")


def export_csv():
    """Export leads to CSV"""
    leads = get_leads()
    
    if not leads:
        print("❌ No leads to export")
        return
    
    filename = f"leads_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'phone', 'extra', 'timestamp'])
            writer.writeheader()
            writer.writerows(leads)
        
        print(f"✅ Exported {len(leads)} leads to: {filename}")
    except Exception as e:
        print(f"❌ Error: {e}")


def export_json():
    """Export leads to JSON (backup)"""
    leads = get_leads()
    
    if not leads:
        print("❌ No leads to export")
        return
    
    filename = f"leads_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(leads, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Backed up {len(leads)} leads to: {filename}")
    except Exception as e:
        print(f"❌ Error: {e}")


def clear_leads():
    """Clear all leads (with confirmation)"""
    confirmation = input("⚠️  This will delete ALL leads. Type 'yes' to confirm: ")
    
    if confirmation.lower() == 'yes':
        save_leads([])
        print("✅ All leads cleared")
    else:
        print("❌ Cancelled")


def clear_sessions():
    """Clear all sessions"""
    confirmation = input("⚠️  This will clear all user sessions. Type 'yes' to confirm: ")
    
    if confirmation.lower() == 'yes':
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        print("✅ All sessions cleared")
    else:
        print("❌ Cancelled")


def search_lead(query: str):
    """Search for lead by name or phone"""
    leads = get_leads()
    query = query.lower()
    
    results = [l for l in leads if query in l['name'].lower() or query in l['phone']]
    
    if not results:
        print(f"❌ No leads found matching: {query}")
        return
    
    print(f"✅ Found {len(results)} matching lead(s):\n")
    
    table_data = []
    for lead in results:
        table_data.append([
            lead['name'],
            lead['phone'],
            lead['extra'],
            lead['timestamp']
        ])
    
    headers = ["Name", "Phone", "Extra", "Timestamp"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def remove_lead(index: int):
    """Remove specific lead by index"""
    leads = get_leads()
    
    if index < 0 or index >= len(leads):
        print("❌ Invalid index")
        return
    
    removed = leads.pop(index)
    save_leads(leads)
    
    print(f"✅ Removed lead: {removed['name']} ({removed['phone']})")


def show_menu():
    """Display main menu"""
    print_header("🤖 DTM Bot - Admin Utilities")
    print("""
1. 📋 Show all leads
2. 📊 Show statistics
3. 🔍 Search lead
4. 📥 Export to CSV
5. 💾 Backup to JSON
6. 🗑️  Clear all leads
7. 🧹 Clear sessions
8. ❌ Remove specific lead
9. 📞 Add lead manually
0. Exit

Choose option (0-9): """, end='')


def add_lead_manual():
    """Manually add a lead"""
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    extra = input("Enter extra phone: ").strip()
    
    if not name or not phone or not extra:
        print("❌ All fields required")
        return
    
    from config import add_lead
    add_lead(name, phone, extra)
    print(f"✅ Lead added: {name}")


def main():
    """Main admin utility menu"""
    while True:
        show_menu()
        choice = input().strip()
        
        if choice == '1':
            print_header("📋 All Leads")
            show_leads()
        
        elif choice == '2':
            show_stats()
        
        elif choice == '3':
            query = input("Search for: ").strip()
            if query:
                search_lead(query)
        
        elif choice == '4':
            export_csv()
        
        elif choice == '5':
            export_json()
        
        elif choice == '6':
            clear_leads()
        
        elif choice == '7':
            clear_sessions()
        
        elif choice == '8':
            try:
                print_header("🗑️  Remove Lead")
                show_leads()
                idx = int(input("\nEnter lead number to remove: ")) - 1
                remove_lead(idx)
            except (ValueError, IndexError):
                print("❌ Invalid input")
        
        elif choice == '9':
            add_lead_manual()
        
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        # Try to import tabulate for nice tables
        from tabulate import tabulate
        main()
    except ImportError:
        print("⚠️  Missing dependency: tabulate")
        print("Install with: pip install tabulate")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
