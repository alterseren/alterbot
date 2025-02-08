from aiogram import types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from keyboards import get_menu_keyboard
from sqlalchemy import select
from models import User, SupportRequest, UploadedFile
from database import SessionLocal
import os
import logging

logger = logging.getLogger(__name__)

async def start(message: types.Message, state: FSMContext):
    await message.answer("🔹 Вітаю! Ось головне меню:", reply_markup=get_menu_keyboard())

async def back(message: types.Message):
    await message.answer("🔙 Повертаємось у головне меню", reply_markup=get_menu_keyboard())

async def delete_user(message: types.Message):
    async with SessionLocal() as session:
        user_result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = user_result.scalar_one_or_none()
        
        if not user:
            await message.answer("⚠️ Ви не зареєстровані!")
            return

        support_requests = await session.execute(select(SupportRequest).where(SupportRequest.telegram_id == message.from_user.id))
        for req in support_requests.scalars():
            await session.delete(req)
        
        uploaded_files = await session.execute(select(UploadedFile).where(UploadedFile.telegram_id == message.from_user.id))
        for file in uploaded_files.scalars():
            await session.delete(file)
            try:
                os.remove(file.file_path)
            except Exception as e:
                logger.error(f"Помилка видалення файлу: {e}")
        
        await session.delete(user)
        await session.commit()
    
    await message.answer("❌ Ваш профіль та всі пов'язані дані видалені!")

async def bot_info(message: types.Message):
    await message.answer(
        "🤖 Цей бот створений для демонстрації можливостей AIogram 3.x\n"
        "⚙️ Основні функції:\n"
        "- Реєстрація користувача\n"
        "- Робота з базою даних\n"
        "- Файловий менеджер\n"
        "- Система підтримки"
    )