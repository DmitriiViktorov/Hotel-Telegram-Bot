from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config

if not config.BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Проверьте файл .env и убедитесь, что переменная установлена.")

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
