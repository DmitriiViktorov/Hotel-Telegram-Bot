from loader import bot
from telegram_bot_calendar import DetailedTelegramCalendar
from states.user_data import *
from datetime import timedelta, date
import utils.find_hotels


def set_arrival_date(message):
    calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                              current_date=date.today(),
                                              min_date=date.today(),
                                              max_date=date.today() + timedelta(days=365),
                                              locale="ru").build()
    bot.send_message(message.chat.id,
                     "Введите дату заезда.",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def handle_arrival_date(call):
    user = User.get_user(call.from_user.id)
    result, key, step = DetailedTelegramCalendar(calendar_id=1,
                                                 current_date=date.today(),
                                                 min_date=date.today(),
                                                 max_date=date.today() + timedelta(days=365),
                                                 locale="ru").process(call.data)
    if not result and key:
        bot.edit_message_text(f"Введите дату заезда.",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        user.arrival_date = result
        bot.edit_message_text(f"Дата заезда {user.arrival_date}",
                              call.message.chat.id,
                              call.message.message_id)

        calendar, step = DetailedTelegramCalendar(calendar_id=2,
                                                  min_date=user.arrival_date + timedelta(days=1),
                                                  max_date=user.arrival_date + timedelta(days=365),
                                                  locale="ru").build()
        bot.send_message(user.user_id,
                         "Выберите дату выезда.",
                         reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def handle_departure_date(call):
    user = User.get_user(call.from_user.id)
    result, key, step = DetailedTelegramCalendar(calendar_id=2,
                                                 min_date=user.arrival_date + timedelta(days=1),
                                                 max_date=user.arrival_date + timedelta(days=365),
                                                 locale="ru").process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите дату выезда", user.user_id, call.message.message_id, reply_markup=key)
    elif result:
        user.departure_date = result
        bot.send_message(call.message.chat.id, f"Дата выезда {user.departure_date}")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return utils.find_hotels.check_additional_filters(call.message, user)
