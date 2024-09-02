from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def repeat_request_button(request_id: int) -> InlineKeyboardMarkup:
	"""
	Функция-кнопка, добавляет к сообщению кнопку, в callback которой хранится id-номер запроса из базы данных.
	:param request_id: id-номер поискового запроса, который необходимо повторить.
	:return: кнопка под сообщением
	"""
	reply_markup = InlineKeyboardMarkup()
	reply_markup.add(InlineKeyboardButton(text='Показать результаты поиска', callback_data='repeat:' + str(request_id)))
	return reply_markup


