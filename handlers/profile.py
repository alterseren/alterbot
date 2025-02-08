from aiogram import types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from sqlalchemy import select
from models import User
from database import SessionLocal
from states import EditProfileState

async def register_user(message: types.Message, state: FSMContext):
    await message.answer("📅 Введіть вашу дату народження (у форматі ДД.ММ.РРРР):")
    await state.set_state(EditProfileState.waiting_for_birth_date)

async def set_birth_date(message: types.Message, state: FSMContext):
    birth_date = message.text
    await state.update_data(birth_date=birth_date)
    await message.answer("🏙️ Введіть місто, де ви народилися:")
    await state.set_state(EditProfileState.waiting_for_birth_city)

async def set_birth_city(message: types.Message, state: FSMContext):
    birth_city = message.text
    await state.update_data(birth_city=birth_city)
    
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        
        if user:
            await message.answer("✅ Ви вже зареєстровані!")
        else:
            user_data = await state.get_data()
            new_user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                birth_date=user_data['birth_date'],
                birth_city=user_data['birth_city']
            )
            session.add(new_user)
            await session.commit()
            await message.answer("🎉 Ви успішно зареєстровані!")
    
    await state.clear()

async def view_profile(message: types.Message, state: FSMContext):
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        
        if user:
            response = (
                f"🆔 Ваш Telegram ID: {user.telegram_id}\n"
                f"👤 Ім'я користувача: {user.username or 'Не вказано'}\n"
                f"📅 Дата народження: {user.birth_date or 'Не вказано'}\n"
                f"🏙️ Місто народження: {user.birth_city or 'Не вказано'}"
            )
            await message.answer(response)
        else:
            await message.answer("⚠️ Ви ще не зареєстровані! Натисніть '🔹 Реєстрація' для реєстрації.")

async def edit_profile(message: types.Message, state: FSMContext):
    await message.answer("📅 Введіть вашу нову дату народження (у форматі ДД.ММ.РРРР):")
    await state.set_state(EditProfileState.waiting_for_birth_date)

async def set_new_birth_date(message: types.Message, state: FSMContext):
    birth_date = message.text
    await state.update_data(birth_date=birth_date)
    await message.answer("🏙️ Введіть нове місто, де ви народилися:")
    await state.set_state(EditProfileState.waiting_for_birth_city)

async def set_new_birth_city(message: types.Message, state: FSMContext):
    birth_city = message.text
    await state.update_data(birth_city=birth_city)
    
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        
        if user:
            user_data = await state.get_data()
            user.birth_date = user_data['birth_date']
            user.birth_city = user_data['birth_city']
            await session.commit()
            await message.answer("🎉 Ваш профіль успішно оновлено!")
        else:
            await message.answer("⚠️ Ви ще не зареєстровані! Натисніть '🔹 Реєстрація' для реєстрації.")
    
    await state.clear()