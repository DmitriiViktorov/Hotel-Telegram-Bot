from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot

possible_guest_rating = {
	'Любой': 'ANY',
	'Хорошо 7+': '35',
	'Очень хорошо 8+': '40',
	'Прекрасно 9+': '45'
}


def select_guest_rating(message: Message):
	"""
	Функция вызова кнопок для выбора рейтинга посетителей.
	Значение из callback_data используется при формировании запроса к API Hotels.
	:param message: Сообщение, по которому произошел вызов функции.
	:return: Сообщение и кнопки с выбором рейтинга посетителей.
	"""

	sort_type_markup = InlineKeyboardMarkup()
	for sort_type in possible_guest_rating:
		sort_type_markup.add(InlineKeyboardButton(text=sort_type, callback_data='rating:' + possible_guest_rating[sort_type]))
	return bot.send_message(message.chat.id, 'Рейтинг посетителей.', reply_markup=sort_type_markup)

