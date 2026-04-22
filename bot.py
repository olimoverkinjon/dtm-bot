# 🤖 DTM BOT - COMPLETE PYTHON VERSION (Converted from PHP)
# Full functionality with file-based storage, sessions, and admin panel
# Based on: config.php, index.php, webhook.php, status.php

import logging
import asyncio
import os
import json
from datetime import datetime
from pathlib import Path
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove, Message, CallbackQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiohttp import web
import re

# ==================
# 🔥 CONFIGURATION
# ==================

API_TOKEN = os.getenv("API_TOKEN") or "8516827967:AAHDYsWDsYrsM3HBna24ceonbpM9a8zb_Yw"
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME") or "@registan_abituriyent"
GROUP_ID = int(os.getenv("GROUP_ID") or "-1003890628671")
ADMIN_ID = int(os.getenv("ADMIN_ID") or "6653845419")

# File paths for data storage (replaces PHP file operations)
LEADS_FILE = Path(__file__).parent / "leads.json"
SESSIONS_FILE = Path(__file__).parent / "sessions.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# ==================
# 📊 STATE MANAGEMENT
# ==================

class Form(StatesGroup):
    """State machine for user registration flow"""
    name = State()
    phone = State()
    extra_phone = State()


# ==================
# 💾 HELPER FUNCTIONS (from config.php)
# ==================

def get_leads() -> list:
    """Get leads from JSON file (replaces getLeads in PHP)"""
    if LEADS_FILE.exists():
        try:
            with open(LEADS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f) or []
        except Exception as e:
            logger.error(f"Error reading leads: {e}")
            return []
    return []


def save_leads(leads: list):
    """Save leads to JSON file (replaces saveLeads in PHP)"""
    try:
        with open(LEADS_FILE, 'w', encoding='utf-8') as f:
            json.dump(leads, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving leads: {e}")


def add_lead(name: str, phone: str, extra_phone: str):
    """Add new lead to storage (replaces addLead in PHP)"""
    leads = get_leads()
    leads.append({
        'name': name,
        'phone': phone,
        'extra': extra_phone,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_leads(leads)


def get_sessions() -> dict:
    """Get all sessions from JSON file"""
    if SESSIONS_FILE.exists():
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f) or {}
        except Exception as e:
            logger.error(f"Error reading sessions: {e}")
            return {}
    return {}


def get_session(user_id: int) -> dict:
    """Get specific user session (replaces getSession in PHP)"""
    sessions = get_sessions()
    return sessions.get(str(user_id), {})


def save_session(user_id: int, state: str, data: dict = None):
    """Save user session (replaces saveSession in PHP)"""
    sessions = get_sessions()
    sessions[str(user_id)] = {
        'state': state,
        'data': data or {}
    }
    try:
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving session: {e}")


def delete_session(user_id: int):
    """Delete user session (replaces deleteSession in PHP)"""
    sessions = get_sessions()
    if str(user_id) in sessions:
        del sessions[str(user_id)]
    try:
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error deleting session: {e}")


# ==================
# 🔍 SUBSCRIPTION CHECK
# ==================

async def check_subscription(user_id: int) -> bool:
    """Check if user is subscribed to channel (replaces checkSubscription in PHP)"""
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False


# ==================
# 🎯 MESSAGE HANDLERS
# ==================

@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    """Handle /start command (replaces handleStart from index.php)"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # Check subscription
    if not await check_subscription(user_id):
        channel = CHANNEL_USERNAME.lstrip('@')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=f"https://t.me/{channel}")],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
        ])
        await bot.send_message(chat_id, "❗️Avval kanalga obuna bo'ling:", reply_markup=keyboard)
        return
    
    # Clear session
    delete_session(user_id)
    
    # Ask for name
    await bot.send_message(chat_id, "📝 Ism va familiyangizni kiriting:")
    await state.set_state(Form.name)


@router.message(Command("admin"))
async def handle_admin(message: Message):
    """Handle /admin command (replaces handleAdmin from index.php)"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if user_id != ADMIN_ID:
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="stat")],
        [InlineKeyboardButton(text="📥 Oxirgi lidlar", callback_data="leads")]
    ])
    
    await bot.send_message(chat_id, "👨‍💼 Admin panel:", reply_markup=keyboard)


@router.message(Form.name)
async def handle_name(message: Message, state: FSMContext):
    """Handle name input (replaces handleName from index.php)"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    name = message.text
    
    # Save name to state
    await state.update_data(name=name)
    
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )
    
    await bot.send_message(chat_id, "📞 Telefon raqamingizni yuboring:", reply_markup=kb)
    await state.set_state(Form.phone)


@router.message(Form.phone, F.contact)
async def handle_phone(message: Message, state: FSMContext):
    """Handle phone input (replaces handlePhone from index.php)"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    phone = message.contact.phone_number
    
    # Save phone to state
    await state.update_data(phone=phone)
    
    await bot.send_message(chat_id, "📱 Qo'shimcha raqam kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.extra_phone)


@router.message(Form.extra_phone)
async def handle_extra_phone(message: Message, state: FSMContext):
    """Handle extra phone input (replaces handleExtraPhone from index.php)"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    extra_phone = message.text.strip()
    
    # Validate: Only digits
    if not extra_phone.isdigit():
        await bot.send_message(chat_id, "❌ Faqat raqam kiriting! (masalan: 901234567)")
        return
    
    # Validate: Length
    if len(extra_phone) < 7:
        await bot.send_message(chat_id, "❌ Raqam juda qisqa!")
        return
    
    # Get data from state
    data = await state.get_data()
    
    # Save lead to file
    add_lead(data['name'], data['phone'], extra_phone)
    
    # Send notification to group
    text = (
        f"🧾 <b>Yangi LID</b>\n\n"
        f"👤 <b>Ism:</b> {data['name']}\n"
        f"📞 <b>Asosiy:</b> {data['phone']}\n"
        f"📱 <b>Qo'shimcha:</b> {extra_phone}\n\n"
        f"📍 <b>Manba:</b> Telegram bot"
    )
    
    await bot.send_message(GROUP_ID, text, parse_mode="HTML")
    
    # Confirm to user
    await bot.send_message(chat_id, "✅ Ro'yxatdan o'tdingiz! Tez orada administratorlarimiz siz bilan bog'lanishadi.")
    
    # Clear state
    await state.clear()
    delete_session(user_id)


# ==================
# 🔘 CALLBACK HANDLERS
# ==================

@router.callback_query(F.data == "check_sub")
async def handle_check_sub(callback: CallbackQuery, state: FSMContext):
    """Handle subscription check callback (replaces handleCheckSub from index.php)"""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    callback_id = callback.id
    
    if not await check_subscription(user_id):
        await bot.answer_callback_query(callback_id, "❌ Hali obuna bo'lmadingiz", show_alert=True)
        return
    
    await bot.answer_callback_query(callback_id, "✅ Tekshirildi!", show_alert=False)
    
    # Clear session
    delete_session(user_id)
    
    # Ask for name
    await bot.send_message(chat_id, "📝 Ism va familiyangizni kiriting:")
    await state.set_state(Form.name)


@router.callback_query(F.data == "stat")
async def handle_stats(callback: CallbackQuery):
    """Handle statistics callback (replaces handleStats from index.php)"""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    
    if user_id != ADMIN_ID:
        await bot.answer_callback_query(callback.id, "❌ Faqat admin uchun!", show_alert=True)
        return
    
    leads = get_leads()
    count = len(leads)
    
    await bot.send_message(chat_id, f"📊 <b>Jami lidlar:</b> <code>{count}</code>", parse_mode="HTML")


@router.callback_query(F.data == "leads")
async def handle_leads(callback: CallbackQuery):
    """Handle leads callback (replaces handleLeads from index.php)"""
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    
    if user_id != ADMIN_ID:
        await bot.answer_callback_query(callback.id, "❌ Faqat admin uchun!", show_alert=True)
        return
    
    leads = get_leads()
    
    if not leads:
        await bot.send_message(chat_id, "❌ Hozircha lid yo'q")
        return
    
    # Get last 5 leads
    recent_leads = leads[-5:]
    
    text = "📥 <b>Oxirgi lidlar:</b>\n\n"
    
    for lead in recent_leads:
        text += f"👤 {lead['name']} | 📞 {lead['phone']} | 📱 {lead['extra']}\n"
    
    await bot.send_message(chat_id, text, parse_mode="HTML")


# ==================
# 🌐 WEB SERVER (for Render/deployment)
# ==================

async def handle_health(request):
    """Health check endpoint (from status.php)"""
    return web.Response(text="Bot ishlayapti ✅", status=200)


async def handle_webhook(request):
    """Webhook endpoint for receiving updates"""
    try:
        data = await request.json()
        await dp.feed_update(bot, types.Update(**data))
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return web.Response(status=200)


async def start_web_server():
    """Start web server (replaces PHP web server)"""
    port = int(os.environ.get("PORT", 8000))
    
    app = web.Application()
    app.router.add_get("/", handle_health)
    app.router.add_post("/webhook", handle_webhook)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    logger.info(f"✅ Web server started on port {port}")
    print(f"🚀 Bot is running! Webhook URL: https://yoursite.com/webhook")


# ==================
# 🚀 MAIN EXECUTION
# ==================

async def main():
    """Main bot entry point"""
    dp.include_router(router)
    
    # Delete old webhook and use polling (or webhook for production)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Start web server
    asyncio.create_task(start_web_server())
    
    # Start polling
    logger.info("🤖 Bot started with polling mode")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
