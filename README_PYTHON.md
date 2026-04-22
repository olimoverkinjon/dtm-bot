# 🤖 DTM Bot - Complete Python Version

**A Telegram bot for lead collection and user registration**  
*Originally written in PHP, now fully converted to Python*

---

## 📋 Overview

This is a complete Python implementation of the DTM Bot, a Telegram bot that:

✅ Collects user leads through a registration flow  
✅ Validates phone numbers and user information  
✅ Stores leads in JSON files  
✅ Manages user sessions for conversation flow  
✅ Provides admin panel for statistics and reports  
✅ Checks channel subscriptions  
✅ Sends notifications to group chats  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip package manager

### Installation

1. **Clone or navigate to project directory**
```bash
cd "c:\Users\admin\Desktop\DTM bot"
```

2. **Create virtual environment** (recommended)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file with your configuration**
```bash
API_TOKEN=your_telegram_bot_token_here
CHANNEL_USERNAME=@your_channel_name
GROUP_ID=-1003890628671
ADMIN_ID=your_admin_user_id
PORT=8000
```

5. **Run the bot**
```bash
python main.py
```

✅ Bot is now running! Send `/start` on Telegram to begin.

---

## 📁 File Structure

```
.
├── main.py              # 🔴 Entry point - Start here!
├── bot.py               # 🤖 Main bot logic (aiogram handlers)
├── config.py            # ⚙️ Configuration & helpers
├── status.py            # 📊 Status/health check server
├── setup_webhook.py     # 🔗 Webhook configuration script
│
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Project metadata
├── .env                # Configuration (create this)
│
├── leads.json          # 📝 Stored leads (auto-created)
├── sessions.json       # 👤 User sessions (auto-created)
│
├── README.md           # Documentation
├── README_PHP.md       # Original PHP version docs
└── PYTHON_CONVERSION.md # PHP → Python migration guide
```

---

## 🎯 Core Files Explained

### main.py
**Entry point for the application**
- Imports the bot from `bot.py`
- Prints startup banner
- Handles Ctrl+C gracefully
```bash
python main.py
```

### bot.py
**Main bot logic - all Telegram interactions**
- Message handlers (`/start`, `/admin`)
- Callback handlers (buttons, inline keyboards)
- User registration flow (name → phone → extra phone)
- Admin panel (statistics, recent leads)
- Lead storage and validation

### config.py
**Configuration and helper functions**
- Environment variables management
- File I/O operations (leads.json, sessions.json)
- Lead management (`get_leads()`, `save_leads()`, `add_lead()`)
- Session management (`get_session()`, `save_session()`)
- Validation functions (`validate_phone()`)

### status.py
**Health check and status dashboard**
- Provides HTTP endpoints for bot status
- HTML dashboard at `http://localhost:8000`
- JSON API endpoints (`/api/stats`, `/api/leads`)
```bash
python status.py
```

### setup_webhook.py
**Webhook configuration script**
- Configures Telegram webhook for your server
- Useful for production deployments
```bash
python setup_webhook.py https://yoursite.com/webhook
```

---

## 🎮 Bot Features

### User Commands

#### `/start`
Begins the registration process:
1. ✅ Check if user is subscribed to channel
2. 📝 Ask for user's name
3. 📞 Ask for main phone number (contact button)
4. 📱 Ask for additional phone number
5. ✅ Confirm and save lead

```
User: /start
Bot: ❗️Avval kanalga obuna bo'ling:
     📢 Kanalga obuna bo'lish | ✅ Tekshirish
```

#### `/admin`
Admin panel (ADMIN_ID only):
- 📊 **Statistika** - Show total lead count
- 📥 **Oxirgi lidlar** - Show last 5 leads
```
/admin → Admin panel with buttons
```

### Features

**Subscription Check:**
- Verifies user is subscribed to channel before allowing registration
- Uses Telegram API `getChatMember` method

**Session Management:**
- Tracks user state across messages
- Stores temporary data (name, phone) until complete

**Phone Validation:**
- Checks if phone is digits only
- Minimum 7 characters

**Lead Storage:**
- Saves leads with timestamp
- JSON format for easy backup/export
- Structured data: name, phone, extra_phone, timestamp

**Admin Features:**
- View total leads count
- View last 5 recent leads
- Protected by ADMIN_ID check

---

## 💾 Data Storage

### leads.json
Stores all collected leads:
```json
[
  {
    "name": "John Doe",
    "phone": "+998901234567",
    "extra": "901234568",
    "timestamp": "2026-04-22 14:30:45"
  },
  {
    "name": "Jane Smith",
    "phone": "+998902345678",
    "extra": "902345679",
    "timestamp": "2026-04-22 15:45:30"
  }
]
```

### sessions.json
Tracks active user sessions:
```json
{
  "123456789": {
    "state": "waiting_extra_phone",
    "data": {
      "name": "John Doe",
      "phone": "+998901234567"
    }
  }
}
```

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# Required
API_TOKEN=8516827967:AAHDYsWDsYrsM3HBna24ceonbpM9a8zb_Yw

# Telegram Configuration
CHANNEL_USERNAME=@registan_abituriyent
GROUP_ID=-1003890628671
ADMIN_ID=6653845419

# Optional
PORT=8000
STATUS_PORT=8000
```

### Getting Your Values

**API_TOKEN:**
- Create bot with BotFather on Telegram
- Copy the token

**CHANNEL_USERNAME:**
- Your public channel username (starts with @)

**GROUP_ID:**
- Forward message from group to @userinfobot
- Note the ID

**ADMIN_ID:**
- Send any message to bot
- Check logs: `"user_id": 123456789`

---

## 📊 HTTP Endpoints

### Bot Health Check
```
GET http://localhost:8000/
GET http://localhost:8000/health
```
Response:
```json
{
  "status": "ok",
  "timestamp": "2026-04-22T14:30:45.123456",
  "bot": "operational"
}
```

### Statistics API
```
GET http://localhost:8000/api/stats
```
Response:
```json
{
  "total_leads": 42,
  "admin_id": 6653845419,
  "channel": "@registan_abituriyent",
  "group_id": -1003890628671,
  "timestamp": "2026-04-22T14:30:45.123456"
}
```

### Leads API
```
GET http://localhost:8000/api/leads
```
Response:
```json
{
  "count": 5,
  "leads": [
    {"name": "John", "phone": "+998901234567", ...},
    ...
  ],
  "timestamp": "2026-04-22T14:30:45.123456"
}
```

---

## 🚀 Deployment

### Local Development
```bash
python main.py
```
Bot uses polling mode - connects every few seconds to fetch updates.

### Production with Webhook

1. **Set up webhook:**
```bash
python setup_webhook.py https://yourdomain.com/webhook
```

2. **Run bot with webhook:**
```python
# In bot.py, change from polling to webhook mode
# The bot.py file already supports both modes
```

3. **On Server (e.g., Render, Heroku, AWS):**
```bash
gunicorn -w 1 -b 0.0.0.0:${PORT} bot:app
```

---

## 📚 API Reference

### Config Module

```python
from config import (
    # Configuration
    API_TOKEN, CHANNEL_USERNAME, GROUP_ID, ADMIN_ID,
    
    # Lead functions
    get_leads, save_leads, add_lead,
    
    # Session functions
    get_session, save_session, delete_session,
    
    # Utilities
    validate_phone, get_leads_count,
)
```

### Bot Module

```python
from bot import bot, router, Form

# Access bot instance
await bot.send_message(chat_id, "Message")

# Form states
class Form(StatesGroup):
    name = State()
    phone = State()
    extra_phone = State()
```

---

## 🐛 Troubleshooting

### Bot doesn't start
**Error:** `ModuleNotFoundError: No module named 'aiogram'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Bot doesn't respond to /start
**Check:**
- API_TOKEN is correct in .env
- Bot is still running (`python main.py`)
- Telegram app is not in offline mode

**Debug:**
```bash
# Run with verbose logging
python -c "import logging; logging.basicConfig(level=logging.DEBUG); import main; main.main()"
```

### "Please set API token" error
**Solution:**
Create `.env` file in project directory:
```env
API_TOKEN=your_token_here
```

### Storage files not found
**Auto-fixed:** Bot automatically creates `leads.json` and `sessions.json` on first run.

### Port already in use
**Change port:**
```bash
PORT=8001 python status.py
```

---

## 📈 Usage Examples

### Getting Leads Count
```python
from config import get_leads_count
count = get_leads_count()
print(f"Total leads: {count}")
```

### Exporting Leads to CSV
```python
from config import export_leads_to_csv
export_leads_to_csv("leads_backup.csv")
```

### Getting Recent Leads
```python
from config import get_recent_leads
recent = get_recent_leads(count=10)
for lead in recent:
    print(f"{lead['name']}: {lead['phone']}")
```

### Clearing All Sessions
```python
import json
from pathlib import Path
sessions_file = Path(__file__).parent / "sessions.json"
with open(sessions_file, 'w') as f:
    json.dump({}, f)
```

---

## 🔄 Comparison with PHP Version

| Feature | PHP | Python |
|---------|-----|--------|
| Framework | None (Plain PHP) | aiogram |
| File I/O | fopen/fwrite | pathlib/json |
| HTTP Requests | curl | aiogram built-in |
| Async | No (blocking) | Yes (async/await) |
| State Management | Manual sessions | FSM (Finite State Machine) |
| Type Hints | No | Yes (PEP 484) |
| Performance | Slower | Faster (async) |

See [PYTHON_CONVERSION.md](PYTHON_CONVERSION.md) for detailed comparison.

---

## 🤝 Contributing

To improve the bot:

1. Test changes locally:
```bash
python main.py
```

2. Check logs:
```bash
# Enable debug logging in config.py
logging.basicConfig(level=logging.DEBUG)
```

3. Follow code style:
```bash
# Format code (optional)
black *.py
```

---

## 📝 License

This project is provided as-is. Free to modify and use.

---

## 🆘 Support

**Issues?**

1. Check [Troubleshooting](#troubleshooting) section
2. Review [PYTHON_CONVERSION.md](PYTHON_CONVERSION.md)
3. Check logs: `python main.py` shows errors

**Original PHP docs:** [README_PHP.md](README_PHP.md)  
**Migration guide:** [PYTHON_CONVERSION.md](PYTHON_CONVERSION.md)

---

## 📞 Bot Commands Summary

| Command | Who | Purpose |
|---------|-----|---------|
| `/start` | Everyone | Begin registration |
| `/admin` | Admin only | Show admin panel |
| `check_sub` | Callback | Check subscription |
| `stat` | Callback | Show statistics |
| `leads` | Callback | Show recent leads |

---

**Version:** 2.0 (Python)  
**Original Version:** 1.0 (PHP)  
**Last Updated:** April 2026  
**Status:** ✅ Fully Functional

🚀 **Ready to use!** Start the bot with `python main.py`
