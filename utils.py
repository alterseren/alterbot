import aiohttp
import logging
from config import OPENWEATHERMAP_API_KEY

logger = logging.getLogger(__name__)

async def get_weather(city: str, lang: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang={lang}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    weather_description = data['weather'][0]['description']
                    temperature = data['main']['temp']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']
                    return (
                        f"🌤 Погода в місті {city}:\n"
                        f"📝 Опис: {weather_description}\n"
                        f"🌡 Температура: {temperature}°C\n"
                        f"💧 Вологість: {humidity}%\n"
                        f"🌬 Швидкість вітру: {wind_speed} м/с"
                    )
                else:
                    logger.error(f"Помилка отримання даних про погоду: {response.status}")
                    return "❌ Не вдалося отримати дані про погоду. Перевірте назву міста."
        except aiohttp.ClientError as e:
            logger.error(f"Помилка з'єднання з API погоди: {e}")
            return "❌ Сталася помилка при отриманні даних про погоду."
        except Exception as e:
            logger.error(f"Невідома помилка: {e}")
            return "❌ Сталася помилка при отриманні даних про погоду."

