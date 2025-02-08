from aiogram import types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from sqlalchemy import select
from models import SupportRequest, UploadedFile, User
from database import SessionLocal
from keyboards import services_keyboard
from states import SupportState, UploadFileState
from utils import get_weather
import os
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

async def services(message: types.Message):
    await message.answer("🛠 Оберіть сервіс:", reply_markup=services_keyboard)

async def support(message: types.Message, state: FSMContext):
    await message.answer("📩 Напишіть ваше питання для підтримки:")
    await state.set_state(SupportState.waiting_for_message)

async def handle_support_message(message: types.Message, state: FSMContext):
    async with SessionLocal() as session:
        session.add(SupportRequest(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            message=message.text,
            timestamp=int(datetime.now().timestamp())
        ))
        await session.commit()
    
    await message.answer("📬 Ваше повідомлення надіслано в підтримку")
    await state.clear()

async def request_file(message: types.Message, state: FSMContext):
    await message.answer("📤 Будь ласка, відправте файл:")
    await state.set_state(UploadFileState.waiting_for_file)

async def handle_file_upload(message: types.Message, state: FSMContext, bot: Bot):
    document = message.document
    file_name = document.file_name
    file_id = document.file_id
    file = await bot.get_file(file_id)
    
    timestamp = int(datetime.now().timestamp())
    unique_name = f"{message.from_user.id}_{timestamp}_{file_name}"
    file_path = f"downloads/{unique_name}"
    
    os.makedirs("downloads", exist_ok=True)
    await bot.download_file(file.file_path, file_path)
    
    async with SessionLocal() as session:
        session.add(UploadedFile(
            telegram_id=message.from_user.id,
            file_name=file_name,
            file_path=file_path,
            timestamp=timestamp
        ))
        await session.commit()
    
    await message.answer(f"📁 Файл {file_name} успішно збережено!")
    await state.clear()

async def weather_request(message: types.Message, state: FSMContext):
    await message.answer("🌍 Введіть назву міста для отримання погоди:")
    await state.set_state("waiting_for_city")

async def handle_city(message: types.Message, state: FSMContext):
    city = message.text
    weather_info = await get_weather(city, "ua")
    await message.answer(weather_info)
    await state.clear()