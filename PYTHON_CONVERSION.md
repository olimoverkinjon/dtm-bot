# 🔄 PHP to Python Conversion Guide

## Overview

This document explains the conversion of the DTM Bot from PHP to Python. All PHP functionality has been ported to Python using the `aiogram` framework.

---

## File Mapping

| PHP File | Python Equivalent | Purpose |
|----------|-------------------|---------|
| `config.php` | `config.py` | Configuration, helpers, and file management |
| `index.php` | `bot.py` | Main bot logic and webhook handler |
| `webhook.php` | `setup_webhook.py` | Webhook configuration setup |
| `status.php` | `status.py` | Health check and status endpoints |
| `main.php` | `main.py` | Entry point |

---

## Key Conversions

### 1. Configuration (config.php → config.py)

**PHP:**
```php
define('API_TOKEN', getenv('API_TOKEN') ?: '...');
define('CHANNEL_USERNAME', getenv('CHANNEL_USERNAME') ?: '@...');
```

**Python:**
```python
from config import API_TOKEN, CHANNEL_USERNAME
# or
API_TOKEN = os.getenv("API_TOKEN", "...")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@...")
```

### 2. File Storage

**PHP:**
```php
file_get_contents(LEADS_FILE)
json_decode($content, true)
file_put_contents(LEADS_FILE, json_encode(...))
```

**Python:**
```python
from config import get_leads, save_leads, add_lead

leads = get_leads()  # Read JSON file
add_lead(name, phone, extra_phone)  # Add and save
save_leads(leads)  # Write JSON file
```

### 3. Session Management

**PHP:**
```php
getSession($user_id)
saveSession($user_id, $state, $data)
deleteSession($user_id)
```

**Python:**
```python
from config import get_session, save_session, delete_session

session = get_session(user_id)
save_session(user_id, "waiting_name", {"key": "value"})
delete_session(user_id)
```

### 4. Message Handlers

**PHP:**
```php
function handleStart($user_id, $chat_id) {
    if (!checkSubscription($user_id)) {
        sendMessage($chat_id, "Subscribe first");
        return;
    }
    // ... rest of logic
}
```

**Python:**
```python
from aiogram.filters import Command

@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    if not await check_subscription(message.from_user.id):
        await bot.send_message(message.chat.id, "Subscribe first")
        return
    # ... rest of logic
```

### 5. Telegram API Calls

**PHP:**
```php
function sendMessage($chat_id, $text, $reply_markup = null) {
    $data = ['chat_id' => $chat_id, 'text' => $text];
    $curl = curl_init();
    curl_setopt_array($curl, [CURLOPT_URL => ...]);
    return curl_exec($curl);
}
```

**Python:**
```python
# Using aiogram - much simpler!
await bot.send_message(chat_id, text, reply_markup=keyboard)
```

### 6. State Management (FSM)

**PHP:**
```php
// Manual session-based state tracking
$session = getSession($user_id);
if ($session['state'] === 'waiting_name') {
    handleName(...);
}
```

**Python:**
```python
# Aiogram FSM - automatic state management
class Form(StatesGroup):
    name = State()
    phone = State()

@router.message(Form.name)
async def handle_name(message: Message, state: FSMContext):
    # ...
```

---

## Installation & Setup

### Requirements
```bash
pip install aiogram python-dotenv aiohttp
```

### Environment Variables (.env)
```env
API_TOKEN=your_bot_token_here
CHANNEL_USERNAME=@your_channel
GROUP_ID=-1003890628671
ADMIN_ID=6653845419
PORT=8000
```

### Running the Bot

**Development (Polling):**
```bash
python main.py
```

**Production (Webhook):**
```bash
python setup_webhook.py https://yoursite.com/webhook
python bot.py
```

**Status Dashboard:**
```bash
python status.py
```

---

## Feature Comparison

| Feature | PHP Version | Python Version |
|---------|------------|-----------------|
| Subscription Check | CURL API calls | aiogram built-in |
| Message Handling | Manual routing | @router decorators |
| State Management | JSON sessions | aiogram FSM |
| File Storage | json_encode/decode | json module |
| Keyboard Layout | Manual arrays | InlineKeyboardMarkup |
| Async Operations | Blocking | Full async/await |
| Error Handling | try/catch | try/except |

---

## Data Files

Both versions use the same JSON file format:

### leads.json
```json
[
  {
    "name": "John Doe",
    "phone": "+998901234567",
    "extra": "901234568",
    "timestamp": "2026-04-22 14:30:45"
  }
]
```

### sessions.json
```json
{
  "123456789": {
    "state": "waiting_name",
    "data": {}
  }
}
```

---

## API Endpoints

### Bot Commands
- `/start` - Begin registration
- `/admin` - Admin panel (ADMIN_ID only)

### Callback Queries
- `check_sub` - Check subscription status
- `stat` - Show statistics
- `leads` - Show recent leads

### HTTP Endpoints (if running with webhook)
- `GET /` - Health check
- `POST /webhook` - Telegram webhook

### Status Server Endpoints
- `GET /` - Status dashboard (HTML)
- `GET /health` - Health check (JSON)
- `GET /api/stats` - Statistics
- `GET /api/leads` - Leads list

---

## Error Handling

**PHP:**
```php
try {
    $response = curl_exec($curl);
} catch (Exception $e) {
    // handle error
}
```

**Python:**
```python
try:
    member = await bot.get_chat_member(channel, user_id)
except Exception as e:
    logger.error(f"Error: {e}")
```

---

## Logging

**Python Version:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Event happened")
logger.error("Error occurred")
```

---

## Advantages of Python Version

✅ **Async/Await** - Non-blocking operations  
✅ **Cleaner Code** - Less boilerplate  
✅ **Type Hints** - Better IDE support  
✅ **Modern Framework** - aiogram is actively maintained  
✅ **Better Testing** - Easier to unit test  
✅ **Performance** - Async I/O is more efficient  

---

## Migration Checklist

- [x] Convert configuration (config.php → config.py)
- [x] Convert main handlers (index.php → bot.py)
- [x] Convert webhook setup (webhook.php → setup_webhook.py)
- [x] Convert status page (status.php → status.py)
- [x] Port file storage (JSON)
- [x] Port session management
- [x] Port all message handlers
- [x] Port all callback handlers
- [x] Add logging
- [x] Create main entry point (main.py)

---

## Running the Full Application

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
echo "API_TOKEN=your_token_here" > .env

# 3. Start the bot
python main.py

# 4. (Optional) Start status dashboard in another terminal
python status.py
```

---

## Troubleshooting

### Bot doesn't respond
- Check API_TOKEN in .env
- Verify bot is running: `python main.py`
- Check logs for errors

### File permission issues
- Ensure `leads.json` and `sessions.json` are writable
- Check directory permissions: `chmod 755 ./`

### Webhook issues
- Use `setup_webhook.py` to configure webhook
- Verify URL is publicly accessible
- Check bot logs for webhook errors

---

## Future Improvements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Backup/restore functionality
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Rate limiting
- [ ] Admin authentication tokens

---

**Conversion Date:** April 2026  
**Original Version:** PHP  
**Current Version:** Python 3.10+  
**Framework:** aiogram 3.x
