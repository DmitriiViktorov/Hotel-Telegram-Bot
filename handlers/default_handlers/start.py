from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
	bot.reply_to(
				message, f"Здравствуйте, {message.from_user.full_name}!" + '\n'
				+ 'Вас приветствует телеграмм-бот "Время Путешествий!' + '\n'
				+ 'Мы поможем вам найти отель Вашей мечты для отдыха в любой точке мира!' + '\n'
				+ 'Для поиска отеля воспользуйтесь меню или командой /help'
				)
