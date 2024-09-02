from telebot.types import Message
from loader import bot
from utils.find_hotels import find_city_id


@bot.message_handler(commands=['customfilters'])
def customfilters_start(message: Message):
	"""
	Функция, которая инициирует поиск отелей с возможностью указать точные параметры поиска.
	:param message: Сообщение, по которому произошел вызов функции.
	:return: None.
	"""
	bot.reply_to(
		message, 'Вы выбрали поиск отелей с выбором дополнительных параметров поиска.'
		'\nКакой город вы хотите посетить?'
	)
	bot.register_next_step_handler(message, find_city_id, search_parameter='customfilters')

