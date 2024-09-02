from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    try:
        logging.info("Добавление кастомных фильтров...")
        bot.add_custom_filter(StateFilter(bot))

        logging.info("Установка стандартных команд бота...")
        set_default_commands(bot)

        logging.info("Запуск бота в режиме бесконечного опроса...")
        bot.infinity_polling()
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")