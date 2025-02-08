import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задано в змінних оточення")

DATABASE_URL = os.getenv("DATABASE_URL")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
if not OPENWEATHERMAP_API_KEY:
    raise ValueError("OPENWEATHERMAP_API_KEY не задано в змінних оточення")