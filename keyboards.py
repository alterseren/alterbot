from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔹 Реєстрація"), KeyboardButton(text="📋 Переглянути профіль")],
            [KeyboardButton(text="🔧 Редагувати профіль"), KeyboardButton(text="ℹ️ Інформація про бота")],
            [KeyboardButton(text="🗑️ Видалити користувача"), KeyboardButton(text="🛠 Сервіси")],
            [KeyboardButton(text="🌤 Погода")]
        ],
        resize_keyboard=True
    )

services_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Підтримка"), KeyboardButton(text="📂 Завантажити файл")],
        [KeyboardButton(text="🔙 Назад")],
    ], 
    resize_keyboard=True
)