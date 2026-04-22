# Deployment Guide - PHP DTM Bot

## Quick Start

### 1. Localhost Testing (Windows)

```bash
# Copy files to htdocs (if using XAMPP)
C:\xampp\htdocs\dtm-bot\

# Start XAMPP and go to:
http://localhost/dtm-bot/status.php
```

### 2. Free Hosting (000webhost)

1. **Sign up** at https://www.000webhost.com
2. **Create a website** in dashboard
3. **Upload files** via File Manager
   - Upload all `.php` files to `public_html/bot/`
   - Create `.env` file with your configuration
4. **Set webhook** by visiting: `https://yoursite.000webhostapp.com/bot/webhook.php`
5. **Test** at: `https://yoursite.000webhostapp.com/bot/status.php`

### 3. Shared Hosting (Hostinger, Bluehost, etc.)

1. **Connect via FTP/SFTP** using credentials from hosting provider
2. **Upload files** to public_html directory
3. **Set permissions:**
   ```bash
   chmod 755 .
   chmod 644 *.php
   chmod 666 leads.json sessions.json
   ```
4. **Create .env file** with configuration
5. **Visit webhook.php** to set Telegram webhook

### 4. Cloud Hosting (Replit)

1. **Create new Replit** with PHP template
2. **Upload files**
3. **Run webhook.php** to set webhook
4. **Share the URL** with Telegram

## Configuration for Different Hosts

### .env File Setup

```bash
# Create .env file with:
API_TOKEN=your_bot_token_here
CHANNEL_USERNAME=@channel_name
GROUP_ID=-1001234567890
ADMIN_ID=your_user_id
```

### For Render.com (Node.js environment)

```bash
# Use environment variables in dashboard
API_TOKEN = your_token
CHANNEL_USERNAME = @channel
GROUP_ID = -group_id
ADMIN_ID = your_id
```

## File Structure for Upload

```
bot/
├── index.php          ← Main webhook entry point
├── config.php         ← Configuration
├── webhook.php        ← Webhook setup
├── status.php         ← Status check page
├── .env              ← Configuration file (create on server)
├── .env.example       ← Template
├── leads.json         ← Auto-created
├── sessions.json      ← Auto-created
├── .htaccess          ← Apache config
└── composer.json      ← Dependencies
```

## Apache Configuration (.htaccess)

If using Apache, add this to `.htaccess`:

```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    
    # Deny access to sensitive files
    <FilesMatch "\.env$">
        Order allow,deny
        Deny from all
    </FilesMatch>
    
    # Allow only POST requests to index.php
    <FilesMatch "index\.php$">
        Order allow,deny
        Allow from all
    </FilesMatch>
</IfModule>

# Set proper headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "SAMEORIGIN"
</IfModule>

# Disable directory listing
Options -Indexes
```

## Security Checklist

- [ ] `.env` file created with real credentials
- [ ] `.env` added to `.gitignore` (if using Git)
- [ ] API token not hardcoded in PHP files
- [ ] File permissions set correctly (644 for PHP, 666 for JSON)
- [ ] HTTPS enabled on webhook URL
- [ ] `.htaccess` configured to block `.env` file access
- [ ] Directory listing disabled
- [ ] Input validation enabled (already done in code)

## Testing Webhook

### Method 1: Via status.php
```
https://yoursite.com/bot/status.php
```

### Method 2: Manual cURL
```bash
curl -X GET https://api.telegram.org/bot<TOKEN>/getMe
```

Should return:
```json
{
  "ok": true,
  "result": {
    "id": 123456789,
    "is_bot": true,
    "first_name": "DTM Bot"
  }
}
```

## Troubleshooting Deployment

### Error: "PHP files not executing"
- Check file extensions are `.php`
- Verify PHP is enabled on hosting
- Check file permissions

### Error: "Can't write leads.json"
- Set write permissions: `chmod 666 leads.json`
- Check folder permissions: `chmod 755` for folders

### Error: "Webhook not connecting"
- Verify URL is publicly accessible
- Check HTTPS is enabled
- Run `webhook.php` again
- Check firewall settings

### Error: "API Token invalid"
- Copy token from @BotFather exactly
- No spaces before/after token
- Check .env file syntax (no quotes needed)

## Migrating from Python to PHP

1. **Keep your leads data:**
   - Export Python leads to JSON
   - Copy to PHP `leads.json`

2. **Update Telegram webhook:**
   - Set new webhook URL in `webhook.php`
   - Old polling will stop automatically

3. **Test thoroughly:**
   - Send test messages
   - Check `/admin` panel
   - Verify leads are saved

## Performance Tips

- Add caching for channel subscription checks
- Limit leads history (archive old leads)
- Use database instead of JSON for large datasets
- Implement rate limiting for API calls

## Database Migration (Optional)

For production with more leads, use MySQL:

```php
// Add to config.php
$db = new mysqli("localhost", "user", "pass", "dbname");
// Implement database functions instead of JSON
```

## Logging Setup

Add logging to `config.php` for debugging:

```php
function logEvent($message) {
    $log_file = __DIR__ . '/bot.log';
    $timestamp = date('Y-m-d H:i:s');
    error_log("[$timestamp] $message\n", 3, $log_file);
}
```

## Support & Resources

- **Telegram Bot API**: https://core.telegram.org/bots/api
- **PHP Manual**: https://www.php.net/manual
- **Free Hosting**: https://www.000webhost.com
- **Testing Bot**: @BotFather on Telegram

---

**Last Updated:** April 2024
