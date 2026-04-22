"""
DTM Bot - Main Entry Point (Python Version)

This is the main execution file for the DTM Bot.
It starts the Telegram bot and all required services.

Previous PHP version: index.php, config.php, webhook.php
Current Python version: bot.py, config.py, setup_webhook.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project directory to path
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

# Import bot
from bot import main as run_bot

def print_banner():
    """Print startup banner"""
    print("""
    ╔════════════════════════════════════════╗
    ║   🤖 DTM BOT - Python Version       ║
    ║   Telegram Lead Collection Bot        ║
    ║   (Converted from PHP)                ║
    ╚════════════════════════════════════════╝
    """)


async def main():
    """Main entry point"""
    print_banner()
    
    print("📋 Starting bot services...")
    print("  - Telegram Bot: aiogram")
    print("  - Storage: JSON files (leads.json, sessions.json)")
    print("  - Mode: Polling")
    print()
    
    # Check if API token is set
    api_token = os.getenv("API_TOKEN")
    if not api_token or api_token.startswith("your_"):
        print("⚠️  WARNING: API_TOKEN not properly configured")
        print("   Set your token in .env file or environment variable")
    
    # Start the bot
    try:
        await run_bot()
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
