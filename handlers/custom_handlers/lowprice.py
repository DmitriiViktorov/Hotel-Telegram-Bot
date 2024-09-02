from telebot.types import Message
from loader import bot
from utils.find_hotels import find_city_id


@bot.message_handler(commands=['lowprice'])
def lowprice_start(message: Message):
	"""
	Функция, которая инициирует поиск отелей по минимальной цене.
	:param message: Сообщение, по которому произошел вызов функции.
	:return: None.
	"""
	bot.reply_to(message, f'Вы выбрали поиск отелей по самой низкой цене.\nКакой город вы хотите посетить?')
	bot.register_next_step_handler(message, find_city_id, search_parameter='lowprice')


