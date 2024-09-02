from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot


def yes_no_photos(message: Message) -> None:
	"""
	Функция вызова кнопок "ДА" и "НЕТ" для определения необходимости фотографий отелей.
	:param message: Сообщение, по которому произошел вызов функции.
	:return: None
	"""

	keyboard = [
		[
			InlineKeyboardButton(text='Да', callback_data='photos:yes'),
			InlineKeyboardButton(text='Нет', callback_data='photos:no')
		]
	]
	yes_no_button = InlineKeyboardMarkup(keyboard)
	bot.send_message(message.chat.id, 'Вы хотите увидеть фото отеля?', reply_markup=yes_no_button)

