import logging
import asyncio
import os
from dotenv import load_dotenv
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

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@registan_abituriyent")
GROUP_ID = int(os.getenv("GROUP_ID", "-1003890628671"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()


# STATE
class Form(StatesGroup):
    name = State()
    phone = State()
    extra_phone = State()


# OBUNA TEKSHIRISH
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# START
@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):

    if not await check_sub(message.from_user.id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url="https://t.me/registan_abituriyent")],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
        ])

        await message.answer(
            "❗️Avval kanalga obuna bo‘ling:",
            reply_markup=keyboard
        )
        return

    await message.answer("📝 Ism va familiyangizni kiriting:")
    await state.set_state(Form.name)


# TEKSHIRISH
@router.callback_query(F.data == "check_sub")
async def check_callback(callback: types.CallbackQuery, state: FSMContext):
    if await check_sub(callback.from_user.id):
        await callback.message.answer("📝 Ism va familiyangizni kiriting:")
        await state.set_state(Form.name)
    else:
        await callback.answer("❌ Hali obuna bo‘lmadingiz", show_alert=True)


# ISM
@router.message(Form.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )

    await message.answer("📞 Telefon raqamingizni yuboring:", reply_markup=kb)
    await state.set_state(Form.phone)


# TELEFON
@router.message(Form.phone, F.contact)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)

    await message.answer("📱 Qo‘shimcha raqam kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.extra_phone)


# QO‘SHIMCHA TELEFON (VALIDATSIYA BILAN)
@router.message(Form.extra_phone)
async def get_extra(message: types.Message, state: FSMContext):

    phone = message.text.strip()

    # faqat raqam
    if not phone.isdigit():
        await message.answer("❌ Faqat raqam kiriting! (masalan: 901234567)")
        return

    # uzunlik tekshirish
    if len(phone) < 7:
        await message.answer("❌ Raqam juda qisqa!")
        return

    data = await state.get_data()

    text = (
        f"🧾 Yangi LID\n\n"
        f"👤 Ism: {data['name']}\n"
        f"📞 Asosiy: {data['phone']}\n"
        f"📱 Qo‘shimcha: {phone}\n\n"
        f"📍 Manba: Telegram bot"
    )

    await bot.send_message(GROUP_ID, text)
    await message.answer("✅ Tabriklaymiz siz ro‘yxatdan o‘tdingiz! Tez orada siz bilan administratorlarimiz bog‘lanishadi.")
    await state.clear()


# RUN
async def main():
    dp.include_router(router)

    # LOCAL uchun muhim
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())