from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot


def hotel_url_button(message: Message, hotel_url, hotel_name: str) -> None:
	"""
	Вызов кнопки перехода к бронированию указанного отеля.
	:param message: Сообщение, по которому произошел вызов функции.
	:param hotel_url: Ссылка на сайт отеля для бронирования.
	:param hotel_name: Наименование отеля.
	:return: None.
	"""
	reply_markup = InlineKeyboardMarkup()
	reply_markup.add(InlineKeyboardButton(text=hotel_name, url=hotel_url))
	bot.send_message(message.chat.id, text='Перейти к бронированию', reply_markup=reply_markup)

