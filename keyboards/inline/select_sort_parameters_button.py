from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot


possible_sort_types = {
		'Самые популярные': 'PRICE_RELEVANT',
		'Высокий рейтинг гостей': 'REVIEW',
		'Самые близкие к центру города': 'DISTANCE',
		'Самая низкая цена': 'PRICE_LOW_TO_HIGH',
		'Больше всего звезд': 'PROPERTY_CLASS',
		'Наши рекомендации': 'RECOMMENDED'
	}


def select_sort_type(message: Message):
	"""
	Функция вызова кнопок для выбора способа сортировки.
	Значение из callback_data используется при формировании запроса к API Hotels.
	:param message: Сообщение, по которому произошел вызов функции.
	:return: Сообщение и кнопки с выбором способа сортировки результатов поиска.
	"""


	sort_type_markup = InlineKeyboardMarkup()
	for sort_type in possible_sort_types:
		sort_type_markup.add(InlineKeyboardButton(
			text=sort_type,
			callback_data='sort:' + possible_sort_types[sort_type]))
	return bot.send_message(message.chat.id, 'Типы сортировки результатов.', reply_markup=sort_type_markup)

