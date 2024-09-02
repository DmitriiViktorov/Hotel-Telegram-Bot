import datetime


class User:
    all_users = dict()

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        User.add_user(user_id=user_id, user=self)
        self.command: str = ""
        self.request_time: str = ""
        self.city: str = ""
        self.destination_id: str = ""
        self.hotels_number_to_show = 0
        self.photos_uploaded: dict = {"status": False, "number_of_photos": 0}
        self.arrival_date: datetime.date(0, 0, 0)
        self.departure_date: datetime.date(0, 0, 0)
        self.dict_of_city_id: dict
        self.dict_of_result: dict
        # Далее идут свойства, которые используются только при детализированном поиске
        self.sort_type: str = ""
        self.min_price: int = 0
        self.max_price: int = 0
        self.guestRating: str = ""
        self.stars: str = ""

    def __str__(self):
        return f'User.user_id: {self.user_id},\n' \
                f'User.request_time: {self.request_time},\n' \
                f'User.city: {self.city},\n' \
                f'User.destination_id: {self.destination_id},\n' \
                f'User.hotels_number_to_show: {self.hotels_number_to_show},\n' \
                f'User.photos_uploaded: {self.photos_uploaded},\n' \
                f'User.sort_type: {self.sort_type},\n' \
                f'User.min_price: {self.min_price},\n' \
                f'User.max_price: {self.max_price},\n' \
                f'User.guestRating: {self.guestRating},\n' \
                f'User.stars: {self.stars}.\n' \


    @classmethod
    def add_user(cls, user_id, user):
        cls.all_users[user_id] = user


    @classmethod
    def get_user(cls, user_id):
        cls.request_time = datetime.datetime.now()
        if user_id in cls.all_users:
            return cls.all_users[user_id]
        User(user_id=user_id)
        return cls.all_users[user_id]
