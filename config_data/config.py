import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены, так как отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

if not BOT_TOKEN or not RAPID_API_KEY:
    exit('Ошибка: Не все переменные окружения загружены. Проверьте файл .env.')

DEFAULT_COMMANDS = {
    ('help', "Вывести справку"),
    ('lowprice', "Поиск отелей по самой низкой цене"),
    ('highquality', "Поиск отелей самого высокого класса"),
    ('customfilters', "Детализированный поиск отелей"),
    ('history', "История поиска")
}
