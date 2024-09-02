from telebot.types import Message, InputMediaPhoto
from states import calendar
from loader import bot
from states.user_data import User
from keyboards.inline import check_in, location_list_button, yes_no_photo_button
import utils.additional_filters as add_filt
from utils.get_request_utils import get_request
from database import history_database
import re


def find_city_id(message, search_parameter: str):
	"""
	Функция поиска отелей. Получает от пользователя город в виде message.text и параметр поиска в search_parameter
	в зависимости от типа поиска, который выбрал пользователь.
	Ищет город в API Hotels и отправляет пользователю набор кнопок с возможными городами с таким же названием
	для уточнения и выбора.
	:param message: Сообщение пользователя - содержит город, в котором будет проводиться поиск отелей.
	:param search_parameter: Тип поиска, определяет тип запроса к API Hotels.
	:return: None
	"""
	user = User.get_user(message.from_user.id)
	user.command = search_parameter
	if re.search(r'[\*\+\d\/\{\}\[\]&^%$#@!?\\,]', message.text):
		bot.send_message(message.chat.id, 'Название города не может содержать специальные символы.\n'
										  'Попробуйте ещё раз.')
		bot.register_next_step_handler(message, find_city_id, search_parameter)
	else:
		telegramm_user_name = str(message.chat.first_name) + str(message.chat.last_name)
		history_database.get_visitor(user_name=telegramm_user_name, user_id=user.user_id)
		response = get_request.get_city(message.text)

		if isinstance(response, str):
			bot.send_message(message.chat.id, response)

		else:
			response = response.json()
			city_results = dict()
			for i_name in range(len(response['sr'])):
				if response['sr'][i_name]['type'] == 'CITY':
					city_results[response['sr'][i_name]['gaiaId']] = response['sr'][i_name]['regionNames']['fullName']

			if len(city_results) == 0:
				bot.send_message(
								message.chat.id,
								"По Вашему запросу ничего не найдено.\n"
								"Пожалуйста, проверьте, правильно ли указан город."
								)
				bot.register_next_step_handler(message, find_city_id, search_parameter=user.command)
			else:
				bot.send_message(message.chat.id, f'Итак, вы планируете посетить город {message.text}.')
				user.dict_of_city_id = city_results
				location_list_button.possible_location_list(message, city_result_dict=city_results)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'city_id')
def location_selection(call):
	"""
	Функция-отклик на нажатие кнопки с уточненным городом. Получает на вход ID города.
	:param call: Отклик на нажатие кнопки с названием города, в callback_data содержится ID города.
	:return: None
	"""
	city_id = call.data.split(':')[1]
	user = User.get_user(call.from_user.id)
	user.destination_id = city_id
	user.city = user.dict_of_city_id[city_id]
	bot.send_message(call.message.chat.id, 'Сколько отелей вы хотите увидеть? \n(не больше 10 штук в каждом запросе)')
	bot.delete_message(call.message.chat.id, call.message.message_id)
	bot.register_next_step_handler(call.message, set_hotels_counter)


def set_hotels_counter(message: Message):
	"""
	Функция определения количества отелей в запросе к API Hotels. Если пользователь ввел корректное число отелей,
	то происходит вызов кнопок "ДА" и "НЕТ" и сообщения о необходимости фотографий в запросе.
	:param message: Сообщение от пользователя с количеством отелей.
	:return: None.
	"""
	user = User.get_user(message.from_user.id)
	if message.text.isdigit() and 0 < int(message.text) <= 10:
		user.hotels_number_to_show = int(message.text)
		yes_no_photo_button.yes_no_photos(message)
	else:
		bot.reply_to(message, 'Вы ввели неправильное значение, попробуйте ещё раз')
		bot.send_message(
			message.chat.id,
			'Сколько отелей вы хотите увидеть?\n(не больше 10 штук в каждом запросе)')
		bot.register_next_step_handler(message, set_hotels_counter)


@bot.callback_query_handler(func=lambda call: call.data == 'photos:yes')
def photos_answer_button_yes(call):
	"""
	Функция, которая выполняется, если фотографии нужны.
	Ожидает от пользователя сообщение с количеством необходимых фотографий.
	:param call: Отклик на нажатие кнопки с текстом "ДА" - фотографии нужны.
	:return: None
	"""
	try:
		bot.send_message(
						call.message.chat.id, 'Сколько фото вы хотите увидеть?'
						'\n(не больше 5 штук для каждого отеля)')
		bot.delete_message(call.message.chat.id, call.message.message_id)
	except Exception as e:
		bot.send_message(call.message.chat.id, 'что-то пошло не так в получение ответа о количестве фото\n' + str(e))
	bot.register_next_step_handler(call.message, set_photos_counter)


@bot.callback_query_handler(func=lambda call: call.data == 'photos:no')
def photos_answer_button_no(call):
	"""
	Функция, которая выполняется, если фотографии НЕ нужны.
	Запускает функцию-календарь для выбора дат посещения отеля.
	:param call: Отклик на нажатие кнопки с текстом "НЕТ" - фотографии не нужны.
	:return: None
	"""
	user = User.get_user(call.from_user.id)
	try:
		user.photos_uploaded['status'], user.photos_uploaded["number_of_photos"] = False, 0
		bot.delete_message(call.message.chat.id, call.message.message_id)
	except Exception as e:
		bot.send_message(call.message.chat.id, 'что-то пошло не так в получение ответа о количестве фото\n' + str(e))
	calendar.set_arrival_date(call.message)


def set_photos_counter(message: Message):
	"""
	Функция, которая получает на вход сообщение с количеством фотографий для запроса.
	Запускает функцию-календарь для выбора дат посещения отеля.
	:param message: Сообщение от пользователя с количеством фотографий.
	:return:
	"""
	user = User.get_user(message.from_user.id)
	if message.text.isdigit() and 0 < int(message.text) <= 5:
		user.photos_uploaded['status'], user.photos_uploaded["number_of_photos"] = True, int(message.text)
	else:
		bot.reply_to(
			message,
			'Я не совсем понял ваш запрос.\n'
			'Предлагаю посмотреть фото, чтобы выбрать лучший вариант.\n'
			'Вы увидите по 5 фотографий для каждого найденного отеля.')
		user.photos_uploaded['status'], user.photos_uploaded["number_of_photos"] = True, 5
	calendar.set_arrival_date(message)


def check_additional_filters(message: Message, user: User):
	"""
	Функция проверяет нужны ли дополнительные параметры поиска.
	Если дополнительные параметры не нужны - переходит к отправке запроса к API HOTELS.
	:param message: Сообщение от пользователя.
	:param user: Пользователь с набором его параметров.
	:return: None
	"""
	if user.command == 'customfilters':
		add_filt.get_sort_type(message)
	else:
		set_full_request(message, user)


def set_full_request(message: Message, user):
	"""
	Функция окончательного формирования запроса к API HOTELS.
	Функция отправляет запрос по списку отелей в выбранном городе в соответствии со способом поиска и набором параметров.
	В случае, если отели успешно найдены -hotels_to_show['data'] is not None- переходит к подбору информации по
	каждому отелю в получившемся списке. Получив информацию об отеле переходит в функции отправки сообщений пользователю.

	:param message: Сообщение от пользователя.
	:param user: Пользователь с набором своих атрибутов.
	:return: None
	"""

	bot.send_message(message.chat.id, 'Начинаю подбор вариантов.')
	hotels_to_show = get_request.get_hotels_list(user=user)
	if isinstance(hotels_to_show, str):
		bot.send_message(message.chat.id, hotels_to_show)
	else:
		hotels_to_show = hotels_to_show.json()
		if hotels_to_show['data']:
			hotels_counter = len(hotels_to_show['data']['propertySearch']['properties'])
			if hotels_counter < user.hotels_number_to_show:
				bot.send_message(message.chat.id, f'Кажется, по Вашему запросу удалось найти только {hotels_counter} отелей.')
				user.hotels_number_to_show = hotels_counter
			elif hotels_counter == 0:
				bot.send_message(
								message.chat.id,
								f'Кажется, в городе {user.city} нет ни одного отеля, который подходит под ваши требования')
				user.hotels_number_to_show = hotels_counter
			history_database.get_search_parameters(user=user, request=str(hotels_to_show))

			for i_hotel in range(user.hotels_number_to_show):
				abbreviation = hotels_to_show['data']['propertySearch']['properties'][i_hotel]
				i_hotel_id = abbreviation['id']
				i_hotel_name = abbreviation['name']
				i_hotel_cost = round(abbreviation['price']['lead']['amount'], 2)
				total_cost = round(i_hotel_cost * (user.departure_date - user.arrival_date).days, 2)

				hotel_info = get_request.get_hotel_info(i_hotel_id)
				print(hotel_info)
				if isinstance(hotel_info, str):
					bot.send_message(message.chat.id, hotel_info)
				else:
					hotel_info = hotel_info.json()['data']['propertyInfo']
					hotel_summary = hotel_info['summary']['tagline']
					hotel_address = hotel_info['summary']['location']['address']['addressLine']
					hotel_review = hotel_info['reviewInfo']['summary']['overallScoreWithDescriptionA11y']['value']

					photos_url = list()
					if user.photos_uploaded["number_of_photos"] > 0:
						for i_photo in range(user.photos_uploaded["number_of_photos"]):
							photos_url.append(hotel_info['propertyGallery']['images'][i_photo]['image']['url'])
					else:
						photos_url = ''

					hotel_url = f'https://www.hotels.com/Hotel-Search?' \
								f'startDate={user.arrival_date}&' \
								f'endDate={user.departure_date}&' \
								f'adults=1&' \
								f'selected={i_hotel_id}&' \
								f'regionId={user.destination_id}'

					i_hotel_info = {
						'id': i_hotel_id,
						'name': i_hotel_name,
						'summary': hotel_summary,
						'cost': i_hotel_cost,
						'total_cost': total_cost,
						'adress': hotel_address,
						'review': hotel_review,
						'hotel_url': hotel_url,
						'photos_url': photos_url
					}
					history_database.get_hotel_information(user.user_id, i_hotel_info)
					send_hotel_info_to_user(message, hotel_info=i_hotel_info, hotel_number=i_hotel)

		else:
			bot.send_message(
				message.chat.id,
				f'Кажется, в городе {user.city} нет ни одного отеля, который подходит под ваши требования.\n'
				f'Попробуйте ещё раз, изменив стоимость проживания или планируемые даты проживания.')


def send_hotel_info_to_user(message: Message, hotel_info, hotel_number):
	"""
	Функция отправляет пользователю сообщения с подробной информацией о найденный отелях. Данные для отправки сообщений
	формируются в предыдущей функции на основании запросов к API Hotels.
	Второе применение данной функции - отправка
	сообщений пользователю на основе запроса из базы данных в функции /history.
	Про каждый отель пользователю отправляется сообщение с общей информацией об отеле, второе сообщение содержит
	фотографии отеля, отправляется только если пользователь выбрал данную опцию и указал количество фотографий.
	Третье сообщение-кнопка	содержит ссылку на основной сайт hotels.com и предлагает пользователю перейти к
	бронированию данного отеля на выбранные пользователем даты.
	:param message: Сообщение от пользователя.
	:param hotel_info: Словарь, содержащий информацию об отеле.
	:param hotel_number: Порядковый номер отеля в результатах поиска.
	:return: None
	"""
	bot.send_message(
						message.chat.id, text='Отель №' + str(hotel_number + 1) + '\n'
						+ 'Название: ' + str(hotel_info['name']) + '\n'
						+ 'Описание: ' + str(hotel_info['summary']) + '\n'
						+ 'Цена за ночь: ' + str(hotel_info['cost']) + '$\n'
						+ 'Цена за все время: ' + str(hotel_info['total_cost']) + '$\n'
						+ 'Адрес: ' + str(hotel_info['adress']) + '\n'
						+ 'Оценка отеля: ' + str(hotel_info['review']) + '\n'
						)

	if hotel_info['photos_url']:
		try:
			bot.send_media_group(message.chat.id, media=[InputMediaPhoto(i_photo) for i_photo in hotel_info['photos_url']])
		except Exception as exc:
			bot.send_message(
				message.chat.id,
				'Возможно, у отеля ' + str(hotel_info['name']) + f'отсутствуют фотографии.\nОшибка: {exc}')
	check_in.hotel_url_button(message, hotel_url=hotel_info['hotel_url'], hotel_name=hotel_info['name'])
