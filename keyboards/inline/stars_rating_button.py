from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot


stars_rating = {
	'Любое': 'ANY',
	'★': '10',
	'★★': '20',
	'★★★': '30',
	'★★★★': '40',
	'★★★★★': '50'
}


def select_stars_rating(message: Message) -> None:
	"""
	Функция вызова кнопок для выбора рейтинга посетителей.
	Значение из callback_data используется при формировании запроса к API Hotels.
	:param message: Сообщение, по которому произошел вызов функции.
	:return: Сообщение и кнопки с выбором количества звезд.
	"""

	sort_type_markup = InlineKeyboardMarkup()
	for sort_type in stars_rating:
		sort_type_markup.add(InlineKeyboardButton(text=sort_type, callback_data='stars:' + stars_rating[sort_type]))
	return bot.send_message(message.chat.id, 'Количество звезд у отеля', reply_markup=sort_type_markup)

