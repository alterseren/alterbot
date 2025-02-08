import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import init_db
from handlers import common, profile, services
from states import EditProfileState, SupportState, UploadFileState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.message.register(common.start, Command("start"))
dp.message.register(common.back, F.text == "🔙 Назад")
dp.message.register(profile.register_user, F.text == "🔹 Реєстрація")
dp.message.register(profile.set_birth_date, StateFilter(EditProfileState.waiting_for_birth_date))
dp.message.register(profile.set_birth_city, StateFilter(EditProfileState.waiting_for_birth_city))
dp.message.register(profile.view_profile, F.text == "📋 Переглянути профіль")
dp.message.register(profile.edit_profile, F.text == "🔧 Редагувати профіль")
dp.message.register(profile.set_new_birth_date, StateFilter(EditProfileState.waiting_for_birth_date))
dp.message.register(profile.set_new_birth_city, StateFilter(EditProfileState.waiting_for_birth_city))
dp.message.register(common.delete_user, F.text == "🗑️ Видалити користувача")
dp.message.register(common.bot_info, F.text == "ℹ️ Інформація про бота") 
dp.message.register(services.services, F.text == "🛠 Сервіси")
dp.message.register(services.support, F.text == "💬 Підтримка")
dp.message.register(services.handle_support_message, StateFilter(SupportState.waiting_for_message))
dp.message.register(services.request_file, F.text == "📂 Завантажити файл")
dp.message.register(services.handle_file_upload, StateFilter(UploadFileState.waiting_for_file))
dp.message.register(services.weather_request, F.text == "🌤 Погода")
dp.message.register(services.handle_city, StateFilter("waiting_for_city"))

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())