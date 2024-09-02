from peewee import *

history_db = SqliteDatabase('database/history.db')


class BaseModel(Model):
	id = PrimaryKeyField(unique=True)

	class Meta:
		database = history_db


class Visitor(BaseModel):
	"""
	Модель Пользователя. Содержит информацию о пользователе.
	"""
	user_name = CharField(default='Visitor')
	user_id = IntegerField(unique=True)
	registration_date = DateField()
	request_counter = IntegerField()
	last_request_id = IntegerField()


class SearchParameters(BaseModel):
	"""
	Модель Параметры поиска. Содержит параметры поиска с использованием внешнего ключа по телеграмм-ID Пользователя.
	"""
	user_id = ForeignKeyField(Visitor)
	search_date = DateTimeField()
	search_type = CharField()
	city = CharField()
	city_id = IntegerField()
	hotels_to_show = IntegerField()
	hotels_photos = IntegerField()
	arrival_date = DateField()
	departure_date = DateField()
	text_request = CharField()
	sorting = CharField(default='')
	min_cost = IntegerField(default=0)
	max_cost = IntegerField(default=0)
	guest_rating = CharField(default='')
	stars = CharField(default='')


class HotelInformation(BaseModel):
	"""
	Модель Информация об отеле. Содержит результат поиска по каждому найденному отелю
	с использованием внешнего ключа по номеру запроса из модели Параметры поиска.
	"""
	request_id = ForeignKeyField(SearchParameters)
	hotel_id = IntegerField()
	hotel_name = CharField()
	hotel_summary = CharField()
	cost_per_night = FloatField()
	total_cost = FloatField()
	adress = CharField()
	review = CharField(default='')
	hotel_url = CharField()
	photos_url = CharField(default=None)


def initialize_db(class_type):
	history_db.connect()
	history_db.create_tables([class_type], safe=True)
	history_db.close()
