import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiohttp import web

# 🔥 CONFIG
API_TOKEN = os.getenv("API_TOKEN") or "API_TOKEN = 8516827967:AAHDYsWDsYrsM3HBna24ceonbpM9a8zb_Yw"
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME") or "@registan_abituriyent"
GROUP_ID = int(os.getenv("GROUP_ID") or "-1003890628671")
ADMIN_ID = int(os.getenv("ADMIN_ID") or "6653845419")  # o'zingni ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# 🔥 LID SAQLASH (RAM)
leads = []

# STATE
class Form(StatesGroup):
    name = State()
    phone = State()
    extra_phone = State()


# 🔍 OBUNA TEKSHIRISH
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# 🚀 START
@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):

    if not await check_sub(message.from_user.id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url="https://t.me/registan_abituriyent")],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
        ])

        await message.answer("❗️Avval kanalga obuna bo‘ling:", reply_markup=keyboard)
        return

    await message.answer("📝 Ism va familiyangizni kiriting:")
    await state.set_state(Form.name)


# ✅ TEKSHIRISH
@router.callback_query(F.data == "check_sub")
async def check_callback(callback: types.CallbackQuery, state: FSMContext):
    if await check_sub(callback.from_user.id):
        await callback.message.answer("📝 Ism va familiyangizni kiriting:")
        await state.set_state(Form.name)
    else:
        await callback.answer("❌ Hali obuna bo‘lmadingiz", show_alert=True)


# 👤 ISM
@router.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )

    await message.answer("📞 Telefon raqamingizni yuboring:", reply_markup=kb)
    await state.set_state(Form.phone)


# 📞 TELEFON
@router.message(Form.phone, F.contact)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)

    await message.answer("📱 Qo‘shimcha raqam kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.extra_phone)


# 📱 QO‘SHIMCHA TELEFON
@router.message(Form.extra_phone)
async def get_extra(message: types.Message, state: FSMContext):

    phone = message.text.strip()

    if not phone.isdigit():
        await message.answer("❌ Faqat raqam kiriting!")
        return

    if len(phone) < 7:
        await message.answer("❌ Raqam juda qisqa!")
        return

    data = await state.get_data()

    # 🔥 LID SAQLASH
    leads.append({
        "name": data['name'],
        "phone": data['phone'],
        "extra": phone
    })

    text = (
        f"🧾 Yangi LID\n\n"
        f"👤 Ism: {data['name']}\n"
        f"📞 Asosiy: {data['phone']}\n"
        f"📱 Qo‘shimcha: {phone}\n\n"
        f"📍 Manba: Telegram bot"
    )

    await bot.send_message(GROUP_ID, text)
    await message.answer("✅ Ro‘yxatdan o‘tdingiz!")
    await state.clear()


# =====================
# 🔥 ADMIN PANEL
# =====================

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="stat")],
        [InlineKeyboardButton(text="📥 Oxirgi lidlar", callback_data="leads")]
    ])

    await message.answer("👨‍💼 Admin panel:", reply_markup=kb)


# 📊 STAT
@router.callback_query(F.data == "stat")
async def stat_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    await callback.message.answer(f"📊 Jami lidlar: {len(leads)}")


# 📥 LIDLAR
@router.callback_query(F.data == "leads")
async def leads_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    if not leads:
        await callback.message.answer("❌ Hozircha lid yo‘q")
        return

    text = "📥 Oxirgi lidlar:\n\n"

    for lead in leads[-5:]:
        text += f"{lead['name']} - {lead['phone']}\n"

    await callback.message.answer(text)


# =====================
# 🌐 WEB SERVER (RENDER)
# =====================

async def handle(request):
    return web.Response(text="Bot ishlayapti")


async def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()


# 🚀 RUN
async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    await start_web_server()  # 🔥 Render uchun

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())