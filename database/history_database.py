from database.models import *
import datetime
from states.user_data import User

initialize_db(Visitor)
initialize_db(SearchParameters)
initialize_db(HotelInformation)


def get_visitor(user_name, user_id):
	"""
	Функция добавления нового пользователя в базу данных. Проверяет, есть ли в базе данных ID пользователя.
	Если ID не найден - создает запись о новом пользователе.
	:param user_name: Имя пользователя.
	:param user_id: Уникальный телеграмм-ID пользователя.
	:return: None
	"""
	with history_db:
		if Visitor.select().where(Visitor.user_id == user_id):
			pass
		else:
			Visitor.create(
				user_name=user_name,
				user_id=user_id,
				registration_date=datetime.datetime.now(),
				request_counter=0,
				last_request_id=0
			)


def get_search_parameters(user: User, request: str):
	"""
	Функция добавляет запись в базу данных с информацией о поисковом запросе пользователя.
	:param user: Пользователь с набором его параметров поиска.
	:param request: Полный текст запроса к API Hotels.
	:return: None
	"""
	with history_db:
		search = SearchParameters.create(
			user_id=user.user_id,
			search_date=datetime.datetime.now(),
			search_type=user.command,
			city=user.city,
			city_id=user.destination_id,
			hotels_to_show=user.hotels_number_to_show,
			hotels_photos=user.photos_uploaded["number_of_photos"],
			arrival_date=user.arrival_date,
			departure_date=user.departure_date,
			sorting=user.sort_type,
			min_cost=user.min_price,
			max_cost=user.max_price,
			guest_rating=user.guestRating,
			stars=user.stars,
			text_request=request
		)
		if Visitor.select().where(Visitor.user_id == user.user_id):
			update = Visitor.update({Visitor.last_request_id: search.id,
									Visitor.request_counter: Visitor.request_counter + 1}) \
									.where(Visitor.user_id == user.user_id)
			update.execute()


def get_hotel_information(user_id, hotel_info: dict):
	"""
	Функция добавляет информацию о каждом найденном отеле в базу данных.
	:param user_id: Уникальный телеграмм-ID пользователя.
	:param hotel_info: словарь, содержащий всё информацию об отеле.
	:return: None
	"""
	with history_db:
		request_id = Visitor.select(Visitor.last_request_id).where(Visitor.user_id == user_id)
		HotelInformation.create(
			request_id=request_id,
			hotel_id=hotel_info['id'],
			hotel_name=hotel_info['name'],
			hotel_summary=hotel_info['summary'],
			cost_per_night=hotel_info['cost'],
			total_cost=hotel_info['total_cost'],
			adress=hotel_info['adress'],
			review=hotel_info['review'],
			hotel_url=hotel_info['hotel_url'],
			photos_url=' '.join(hotel_info['photos_url'])
		)
