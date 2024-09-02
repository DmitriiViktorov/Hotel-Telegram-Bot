from telebot.types import Message
from loader import bot
from utils.find_hotels import find_city_id


@bot.message_handler(commands=['highquality'])
def highquality_start(message: Message):
	"""
	Функция, которая инициирует поиск отелей по максимальному рейтингу, отзывам и звездности.
	:param message: Сообщение, по которому произошел вызов функции.
	:return: None.
	"""
	bot.reply_to(message, f'Вы выбрали поиск отелей самого высокого класса.\nКакой город вы хотите посетить?')
	bot.register_next_step_handler(message, find_city_id, search_parameter='highquality')


