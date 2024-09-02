from telebot.types import Message
from loader import bot
from keyboards.inline import select_sort_parameters_button, guest_rating_button, stars_rating_button
from states.user_data import *
import utils.find_hotels
import re


def get_sort_type(message: Message):
	"""
	Фунция вызова кнопок со способами сортировки полученного результата.
	:param message: Сообщение от пользователя.
	:return: Кнопки с выбором способа сортировки.
	"""
	bot.send_message(message.chat.id, 'Выберите тип сортировки результатов.')
	return select_sort_parameters_button.select_sort_type(message)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'sort')
def set_sort_type(call):
	"""
	Функция-отклик на выбор способа сортировки. Присваивает значению user.sort_type выбранный тип сортировки.
	Отправляет сообщение пользователю о необходимости указать ценовой диапазон. Если выбран способ сортировки по самым
	дешевым отелям - игнорирует запрос цены и сразу переходит к запросу оценки посетителей.
	:param call: Отклик на нажатие кнопки с типом сортировки.
	:return: Функцию с анализом введенного ценового диапазона или вызов кнопок с выбором рейтинга посетителей.
	"""
	user = User.get_user(call.from_user.id)
	user.sort_type = call.data.split(':')[1]
	if user.sort_type != 'PRICE_LOW_TO_HIGH':
		bot.send_message(
			call.message.chat.id,
			'Минимальная и максимальная цена в $ за ночь пребывания?\n'
			'(введите два числа через дефис, например: "25-70"')
		bot.delete_message(call.message.chat.id, call.message.message_id)
		return bot.register_next_step_handler(call.message, set_price_range, user)
	else:
		user.max_price = 2000
		user.min_price = 1
		bot.send_message(call.message.chat.id, 'Выберите рейтинг посетителей.')
		return guest_rating_button.select_guest_rating(call.message)


def set_price_range(message: Message, user):
	"""
	Функция установки ценового диапазона для поиска отелей. Анализирует сообщение пользователя с ценовым диапазоном.
	Если пользователь верно ввел ценовой диапазон - записывает данные в состояние пользователя и переходит к
	вызову кнопок с выбором рейтинга пользователей. Если выбран способ сортировки по самым высоким оценкам пользователей,
	то сразу переходит к вызову кнопок с выбором количества звезд у отеля.
	:param message: Сообщение от пользователя.
	:param user: Пользователь с набором его параметров.
	:return: Вызов кнопок с выбором рейтинга посетителей или с выбором количества звезд у отеля.
	"""
	price_range = message.text
	if re.match(r'[\d]+-+[\d]', price_range) and 0 <= int(price_range.split('-')[0]) < int(price_range.split('-')[1]):
		user.min_price = int(price_range.split('-')[0])
		user.max_price = int(price_range.split('-')[1])
		if user.sort_type != 'REVIEW':
			bot.send_message(message.chat.id, 'Выберите рейтинг посетителей.')
			return guest_rating_button.select_guest_rating(message)
		else:
			user.guestRating = ['40', '45']
			bot.send_message(message.chat.id, 'Выберите количество звезд отеля')
			return stars_rating_button.select_stars_rating(message)
	else:
		bot.send_message(
			message.chat.id,
			'Кажется, произошла ошибка в диапазоне цен.\n'
			'попробуйте ещё раз. Два числа через дефис')
		bot.register_next_step_handler(message, set_price_range, user)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'rating')
def set_guest_rating(call):
	"""
	Функция-отклик на выбор рейтинга пользователей. Присваивает значению user.guestRating выбранный рейтинг.
	Вызывает кнопки выбора количества звезд у отеля. Если выбран способ сортировки по самому большому количеству звезд,
	то сразу переходит к вызову функции формирования окончательного запроса.
	:param call: Отклик на нажатие кнопки с рейтингом посетителей.
	:return: Вызов кнопок с выбором количества звезд у отеля или вызывает функцию, которая формирует окончательный запрос.
	"""
	user = User.get_user(call.from_user.id)
	bot.delete_message(call.message.chat.id, call.message.message_id)
	user.guestRating = call.data.split(':')[1]
	if user.sort_type != 'PROPERTY_CLASS':
		bot.send_message(call.message.chat.id, 'Выберите количество звезд отеля')
		return stars_rating_button.select_stars_rating(call.message)
	else:
		user.stars = ['40', '50']
		return utils.find_hotels.set_full_request(call.message, user)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'stars')
def set_stars_rating(call):
	"""
	Функция-отклик на выбор количества звезд. Присваивает значению user.stars выбранное количество звезд у отеля.
	Вызывает функцию формирования окончательного запроса.
	:param call: Отклик на нажатие кнопки с количеством звезд отеля.
	:return: Вызов функции, которая формирует окончательный запрос.
	"""
	user = User.get_user(call.from_user.id)
	bot.delete_message(call.message.chat.id, call.message.message_id)
	user.stars = call.data.split(':')[1]
	return utils.find_hotels.set_full_request(call.message, user)
