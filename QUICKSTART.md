# 🚀 Quick Start Guide - PHP DTM Bot

## Option 1: Local Testing (Windows with XAMPP)

### Step 1: Install XAMPP
- Download from: https://www.apachefriends.org
- Install and start XAMPP

### Step 2: Copy Files
```bash
# Copy all files to:
C:\xampp\htdocs\dtm-bot\
```

### Step 3: Create .env File
Create file: `C:\xampp\htdocs\dtm-bot\.env`
```
API_TOKEN=8516827967:AAHDYsWDsYrsM3HBna24ceonbpM9a8zb_Yw
CHANNEL_USERNAME=@registan_abituriyent
GROUP_ID=-1003890628671
ADMIN_ID=6653845419
```

### Step 4: Test
Visit: http://localhost/dtm-bot/status.php

---

## Option 2: Free Web Hosting (000webhost.com)

### Step 1: Create Account
1. Go to https://www.000webhost.com
2. Sign up (free)
3. Create a new website

### Step 2: Upload Files
1. Go to Dashboard → File Manager
2. Create folder: `bot`
3. Upload all PHP files to `bot/` folder

### Step 3: Create .env
1. Create new file: `.env`
2. Add your configuration:
```
API_TOKEN=your_bot_token
CHANNEL_USERNAME=@your_channel
GROUP_ID=-your_group_id
ADMIN_ID=your_user_id
```

### Step 4: Set Webhook
1. Visit: `https://yoursite.000webhostapp.com/bot/webhook.php`
2. Wait for confirmation

### Step 5: Test Bot
1. Message @BotFather to get your bot token
2. Start your bot in Telegram
3. Click `/start`

---

## Option 3: Docker (Advanced)

### Prerequisites
- Install Docker from: https://www.docker.com

### Step 1: Create .env
```bash
API_TOKEN=your_token
CHANNEL_USERNAME=@channel
GROUP_ID=-group_id
ADMIN_ID=your_id
```

### Step 2: Run Docker
```bash
docker-compose up -d
```

### Step 3: Access
Visit: http://localhost:8080/status.php

---

## Troubleshooting

### Bot doesn't respond
1. Check `.env` file exists
2. Visit `status.php` to verify configuration
3. Check Telegram Bot API token is correct

### Can't write leads.json
1. Set folder permissions to 755
2. Set file permissions to 666

### Webhook failing
1. Make sure URL is HTTPS
2. Bot must have internet access
3. Check API token is correct

---

## Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| "Call to undefined function" | Install cURL extension |
| "Permission denied" | Run `chmod 755 .` and `chmod 666 *.json` |
| "Webhook not working" | Visit webhook.php again |
| "Can't connect to API" | Check internet, verify token |

---

## What's Next?

- ✅ Test with `/start` command
- ✅ Register as a test user
- ✅ Check `/admin` panel
- ✅ Verify leads are saved

---

## Need Help?

Check these files:
- `status.php` - View system status
- `README_PHP.md` - Complete documentation
- `DEPLOYMENT_GUIDE.md` - Detailed setup instructions

**Bot API Token should NOT be shared!** 🔐
