from telebot.types import Message
from loader import bot
from database.history_database import *
from keyboards.inline import guest_rating_button, select_sort_parameters_button, stars_rating_button
from keyboards.inline.repeat_request import repeat_request_button as rrb
from utils.find_hotels import send_hotel_info_to_user
import time


@bot.message_handler(commands=['history'])
def history_start(message: Message):
	bot.reply_to(message, 'Вы выбрали просмотр истории ваших поисковых запросов.')
	with history_db:
		query = (Visitor.select(Visitor.request_counter).where(Visitor.user_id == message.from_user.id).get())
		search_counter = query.request_counter
	if search_counter == 0:
		bot.send_message(
			message.chat.id,
			'Кажется, вы у нас впервые. На данный момент ваша история запросов пуста.\n'
			'Для поиска отеля воспользуйтесь меню или командой /help')
	else:
		if search_counter in [2, 3, 4]:
			text = ' раза.'
		else:
			text = ' раз.'
		bot.send_message(message.chat.id, f'Вы искали отели с помощью нашего телеграмм-бота уже {search_counter}' + text)
		if search_counter <= 10:
			text = 'Вы увидите все ваши поисковые запросы с'
		else:
			text = 'Вы увидите последние 10 ваших поисковых запросов с'
		bot.send_message(
			message.chat.id,
			text + ' описанием города, который планировали '
			'посетить, количество отелей и фотографий, даты прибытия и отъезда и прочие '
			'параметры, если вы их указывали. При желании вы сможете посмотреть результаты '
			'поиска по каждому запросу.')
		if search_counter > 10:
			search_counter = 10
		time.sleep(3)
		get_history_of_requests(search_counter, message)


def get_history_of_requests(counter, message):
	sorting = {v: k for k, v in select_sort_parameters_button.possible_sort_types.items()}
	rating = {v: k for k, v in guest_rating_button.possible_guest_rating.items()}
	stars = {v: k for k, v in stars_rating_button.stars_rating.items()}
	with history_db:
		request_list = (
			SearchParameters.select().where(SearchParameters.user_id == message.chat.id)
			.order_by(SearchParameters.id.desc()).limit(counter)
		)
		for i_request in request_list:
			if i_request.search_type == 'customfilters':
				custom_filters_parameters = f'Тип сортировки : {sorting[i_request.sorting]},\n'
				if i_request.sorting != 'PRICE_LOW_TO_HIGH':
					custom_filters_parameters += f'Диапазон цены: {i_request.min_cost} - {i_request.max_cost}$,\n'
				elif i_request.sorting != 'REVIEW':
					custom_filters_parameters += f'Рейтинг гостей: {rating[i_request.guest_rating]},\n'
				elif i_request.sorting != 'PROPERTY_CLASS':
					custom_filters_parameters += f'Количество звезд: {stars[i_request.stars]},\n'
			else:
				custom_filters_parameters = ''
			bot.send_message(
				message.chat.id,
				f'Дата поиска: {i_request.search_date.strftime("%d.%m.%Y")},\n'
				f'Тип поиска: {i_request.search_type},\n'
				f'Город: {i_request.city},\n'
				f'Количество отелей: {i_request.hotels_to_show},\n'
				f'Количество фотографий: {i_request.hotels_photos},\n'
				f'Даты поездки: {i_request.arrival_date.strftime("%d.%m.%Y")} - {i_request.departure_date.strftime("%d.%m.%Y")},\n'
				+ custom_filters_parameters, reply_markup=rrb(i_request.id)
				)


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'repeat')
def repeat_hotel_info(call):
	request_id = call.data.split(':')[1]
	with history_db:
		hotels_list = (HotelInformation.select().where(HotelInformation.request_id == request_id))
		if len(hotels_list):
			hotel_number = 0
			for i_hotel in hotels_list:
				i_hotel_info = {
					'id': i_hotel.hotel_id,
					'name': i_hotel.hotel_name,
					'summary': i_hotel.hotel_summary,
					'cost': i_hotel.cost_per_night,
					'total_cost': i_hotel.total_cost,
					'adress': i_hotel.adress,
					'review': i_hotel.review,
					'hotel_url': i_hotel.hotel_url,
					'photos_url': i_hotel.photos_url.split(' ')
				}
				send_hotel_info_to_user(call.message, hotel_info=i_hotel_info, hotel_number=hotel_number)
				hotel_number += 1
		else:
			bot.reply_to(call.message, 'Кажется, по этому запросу результат в базе данных отсутствует.')
