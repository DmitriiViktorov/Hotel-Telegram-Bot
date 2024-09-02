from requests import request

from config_data.config import RAPID_API_KEY
import requests
from states.user_data import *


def get_city(city_name: str):
	"""
	Первый по очередности запрос к API Hotels.
	На основе ответа пользователя формирует параметры запроса поиска ID города.
	:param city_name: Название города, в котором пользователь хочет найти отели.
	:return: Сформированные данные для запроса к API Hotels.
	"""
	url = "https://hotels4.p.rapidapi.com/locations/v3/search"
	querystring = {
		"q": city_name,
		"locale": "ru_RU",
		"langid": "1033",
		"siteid": "300000001"}

	headers = {
		"X-RapidAPI-Key": RAPID_API_KEY,
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	return get_request("GET", url, headers, params=querystring)


def get_hotels_list(user: User):
	"""
	Второй по очередности запрос к API Hotels.
	На основе ответа пользователя формирует параметры запроса для поиска отелей в городе.
	Запросы отличаются в зависимости от критериев поиска, которые выбрал пользователь, влияет на параметр "payload".
	:param user: Состояние пользователя с параметрами поиска отелей.
	:return: Сформированные данные для запроса к API Hotels.
	"""

	url = "https://hotels4.p.rapidapi.com/properties/v2/list"
	if user.command == 'lowprice':

		payload = {
			"currency": "USD",
			"eapid": 1,
			"locale": "ru_RU",
			"siteId": 300000001,
			"destination": {"regionId": user.destination_id},
			"checkInDate": {
				"day": int(user.arrival_date.day),
				"month": int(user.arrival_date.month),
				"year": int(user.arrival_date.year)
			},
			"checkOutDate": {
				"day": int(user.departure_date.day),
				"month": int(user.departure_date.month),
				"year": int(user.departure_date.year)
			},
			"rooms": [{"adults": 2}],
			"resultsStartingIndex": 0,
			"resultsSize": user.hotels_number_to_show,
			"sort": 'PRICE_LOW_TO_HIGH'
		}

	elif user.command == 'highquality':
		payload = {
			"currency": "USD",
			"eapid": 1,
			"locale": "ru_RU",
			"siteId": 300000001,
			"destination": {"regionId": user.destination_id},
			"checkInDate": {
				"day": int(user.arrival_date.day),
				"month": int(user.arrival_date.month),
				"year": int(user.arrival_date.year)
			},
			"checkOutDate": {
				"day": int(user.departure_date.day),
				"month": int(user.departure_date.month),
				"year": int(user.departure_date.year)
			},
			"rooms": [{"adults": 2}],
			"resultsStartingIndex": 0,
			"resultsSize": user.hotels_number_to_show,
			"sort": 'PROPERTY_CLASS',
			"filters": {
				'stars': "50",
				"guestRating": "45"
			}
		}

	elif user.command == 'customfilters':
		payload = {
			"currency": "USD",
			"eapid": 1,
			"locale": "ru_RU",
			"siteId": 300000001,
			"destination": {"regionId": user.destination_id},
			"checkInDate": {
				"day": int(user.arrival_date.day),
				"month": int(user.arrival_date.month),
				"year": int(user.arrival_date.year)
			},
			"checkOutDate": {
				"day": int(user.departure_date.day),
				"month": int(user.departure_date.month),
				"year": int(user.departure_date.year)
			},
			"rooms": [{"adults": 2}],
			"resultsStartingIndex": 0,
			"resultsSize": user.hotels_number_to_show,
			"sort": user.sort_type,
			"filters": {
				"price": {
					"max": user.max_price,
					"min": user.min_price
				},
				"guestRating": user.guestRating,
				'stars': user.stars,
				"availableFilter": "SHOW_AVAILABLE_ONLY"
			}
		}
	else:
		payload = {}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": RAPID_API_KEY,
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	return get_request(method='POST', url=url, json=payload, headers=headers)


def get_hotel_info(i_hotel_id: str):
	"""
	Третий по очереди запрос к API Hotels.
	На основе ID отеля формирует запрос с подробной информацией.
	:param i_hotel_id: ID отеля из списка, сформированного на основе запроса пользователя.
	:return: Сформированные данные для запроса к API Hotels.
	"""

	url = "https://hotels4.p.rapidapi.com/properties/v2/get-summary"
	payload = {
		"currency": "USD",
		"eapid": 1,
		"locale": "en_US",
		"siteId": 300000001,
		"propertyId": i_hotel_id
	}

	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": RAPID_API_KEY,
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	return get_request(method='POST', url=url, json=payload, headers=headers)


def get_request(method, url, headers, params=None, json=None):
	"""
	Функция отправляет запрос по сформированным параметрам и если статус запроса удовлетворительный - возвращает запрос.
	:param method: Метод получения данных от API
	:param url: Раздел поиска.
	:param params: Параметры поиска, в котором содержится название города.
	:param json: Набор параметров поиска для списка отелей и подробной информации про отель.
	:param headers: Заголовки с личным ключом пользователя для сайта Rapidapi.com от API Hotels.
	:return: Результат запроса для дальнейшей десериализации.
	"""
	try:
		response = requests.request(method, url=url, headers=headers, json=json, params=params, timeout=15)
		if response.status_code == requests.codes.ok:
			return response
		elif response.status_code == 403:
			return 'Произошла ошибка: Отказано в доступе.\n' \
					'Возможно, неправильно введен ключ доступа к hotels.API.'
		elif response.status_code == 429:
			return 'Произошла ошибка: Отказано в доступе.\n' \
					'Возможно, закончились доступные бесплатные запросы к hotels.API.'
		else:
			return f'Произошла ошибка при формировании запроса к серверу.\n' \
					f'Статус запроса: {response.status_code}. \n' \
					f'Информация передана администратору чат-бота.\n' \
					f'Пожалуйста, попробуйте повторить свой запрос через некоторое время.'

	except requests.exceptions.Timeout:
		return 'Произошла ошибка: Время ожидания сервера истекло.\n' \
				'Пожалуйста, попробуйте повторить свой запрос через некоторое время.'
