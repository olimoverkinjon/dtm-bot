#!/usr/bin/env python3
"""
Setup webhook for Telegram bot
Equivalent to: webhook.php

Usage:
    python setup_webhook.py <webhook_url>
    
Example:
    python setup_webhook.py https://yoursite.com/webhook
"""

import asyncio
import sys
import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_TOKEN = os.getenv("API_TOKEN") or "8516827967:AAHDYsWDsYrsM3HBna24ceonbpM9a8zb_Yw"

async def setup_webhook(webhook_url: str):
    """Set webhook and display configuration"""
    
    bot = Bot(token=API_TOKEN)
    
    try:
        # Set webhook
        result = await bot.set_webhook(
            url=webhook_url,
            allowed_updates=["message", "callback_query"]
        )
        
        print("=" * 50)
        print("🔗 WEBHOOK SETUP")
        print("=" * 50)
        print(f"✅ Webhook URL: {webhook_url}")
        print(f"📊 Setup result: {result}")
        
        # Get webhook info
        webhook_info = await bot.get_webhook_info()
        print("\n📋 Webhook Info:")
        print(f"  URL: {webhook_info.url}")
        print(f"  Pending updates: {webhook_info.pending_update_count}")
        print(f"  Last error: {webhook_info.last_error_message or 'None'}")
        print(f"  Max connections: {webhook_info.max_connections}")
        
        print("\n✅ Webhook successfully configured!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error setting webhook: {e}")
    finally:
        await bot.session.close()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python setup_webhook.py <webhook_url>")
        print("Example: python setup_webhook.py https://yoursite.com/webhook")
        sys.exit(1)
    
    webhook_url = sys.argv[1]
    asyncio.run(setup_webhook(webhook_url))


if __name__ == "__main__":
    main()
