from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot


def possible_location_list(message: Message, city_result_dict: dict) -> None:
	"""
	Вызов кнопки возможной локации.
	:param message: Сообщение, по которому произошел вызов функции.
	:param city_result_dict: Словарь возможных городов. Содержит перечень названий городов и их ID в API Hotels.
	:return: None.
	"""
	markup = InlineKeyboardMarkup()
	for city_elem in city_result_dict:
		markup.add(InlineKeyboardButton(text=city_result_dict[city_elem], callback_data='city_id:' + city_elem))
	bot.send_message(message.chat.id, "Выберите локацию ", reply_markup=markup)
