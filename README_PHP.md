# DTM Bot - PHP Version

Telegram bot for registering users in the Registan Abituriyent channel - **PHP Edition**

## Features

✅ Channel subscription verification
✅ User registration form (name, phone numbers)
✅ Lead collection and storage
✅ Admin panel with statistics
✅ JSON-based data storage
✅ Webhook support for Telegram

## Requirements

- PHP 7.4+
- cURL extension enabled
- Telegram Bot API Token
- Web server (Apache, Nginx, etc.)

## Installation

### 1. Download files
```bash
# All files should be in the same directory
index.php          # Main webhook handler
config.php         # Configuration and helpers
webhook.php        # Webhook setup script
.env              # Environment variables (local)
.env.example       # Example environment file
```

### 2. Set environment variables

Create `.env` file with your credentials:
```
API_TOKEN=8516827967:AAHDYsWDsYrsM3HBna24ceonbpM9a8zb_Yw
CHANNEL_USERNAME=@registan_abituriyent
GROUP_ID=-1003890628671
ADMIN_ID=6653845419
```

### 3. Upload to your server

Upload all PHP files to your web server (e.g., `example.com/bot/`)

### 4. Set webhook

Visit: `https://yoursite.com/bot/webhook.php`

This will set the Telegram webhook to `https://yoursite.com/bot/index.php`

## File Structure

```
dtm-bot/
├── index.php          # Main entry point (webhook)
├── config.php         # Configuration and helpers
├── webhook.php        # Webhook setup tool
├── .env              # Environment variables (ignored)
├── .env.example       # Example environment
├── leads.json         # Stored leads (auto-created)
├── sessions.json      # User sessions (auto-created)
└── README.md         # This file
```

## How It Works

### User Flow
1. User sends `/start` command
2. Bot checks if user is subscribed to channel
3. If not subscribed → shows subscribe button + check button
4. If subscribed → asks for name
5. Collects phone number (via contact button)
6. Collects extra phone number
7. Saves lead and notifies admin group

### Admin Features (`/admin`)
- **📊 Statistika** - Total number of leads
- **📥 Oxirgi lidlar** - Last 5 leads with details

### Data Storage

**leads.json** - Stores all leads
```json
[
  {
    "name": "John Doe",
    "phone": "+998901234567",
    "extra": "987654321",
    "timestamp": "2024-04-21 10:30:00"
  }
]
```

**sessions.json** - Stores user conversation states
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

## Configuration

### Via environment variables
```php
API_TOKEN          # Telegram bot token
CHANNEL_USERNAME   # Channel to check subscription
GROUP_ID          # Group ID for lead notifications
ADMIN_ID          # Your Telegram user ID for admin panel
```

### Via .env file (recommended for local development)
Create `.env` file with the above variables.

## Deployment Options

### ✅ Free Hosting
- **000webhost.com** - Free PHP hosting
- **Infinityfree.net** - Free with cPanel
- **Replit.com** - Quick deployment
- **Heroku** (with additional config)

### ✅ Paid Hosting
- **Bluehost**
- **SiteGround**
- **DreamHost**
- **Hostinger**

## Setting Webhook (Important!)

For production, Telegram needs to push updates to your server via webhook:

### Option 1: Visit webhook.php
```
https://yoursite.com/bot/webhook.php
```

### Option 2: Manual via cURL
```bash
curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook \
  -d "url=https://yoursite.com/bot/index.php"
```

### Option 3: PHP code
```php
$curl = curl_init();
curl_setopt_array($curl, [
    CURLOPT_URL => "https://api.telegram.org/bot$TOKEN/setWebhook",
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => ['url' => 'https://yoursite.com/bot/index.php']
]);
curl_exec($curl);
```

## Admin Commands

### Start conversation
```
/start
```

### Open admin panel (only for ADMIN_ID)
```
/admin
```

## File Permissions

Make sure these directories are writable:
```bash
chmod 755 .
chmod 644 *.php
chmod 666 leads.json sessions.json
```

## Troubleshooting

### 🔴 "API Token is invalid"
- Check `.env` file has correct `API_TOKEN`
- Make sure token is in single line

### 🔴 "Webhook not working"
- Visit `webhook.php` to set webhook
- Check URL is publicly accessible
- Verify `index.php` returns 200 status

### 🔴 "Can't send messages to group"
- Check `GROUP_ID` is correct (negative number for groups)
- Make sure bot is member of the group

### 🔴 "Subscription check failing"
- Verify `CHANNEL_USERNAME` is correct
- Make sure bot is member of channel
- Bot needs at least read permissions

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` file with real token
- Always use `.env.example` as template
- Add `.env` to `.gitignore`
- Use HTTPS for webhook
- Validate all user inputs

## Support

For issues with aiogram Python version, see [aiogram documentation](https://docs.aiogram.dev/)

For PHP Telegram Bot API, see [Telegram Bot API docs](https://core.telegram.org/bots/api)

## License

MIT
