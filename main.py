# -*- coding: utf-8 -*-

import telebot
from telebot import types

from config import TOKEN

bot = telebot.TeleBot(TOKEN, parse_mode="MarkdownV2")

from database import Users


from atexit import register
from cgitb import text
from tabnanny import check
from unicodedata import name
from xml.dom.domreg import registered


sex = None
age = None
search = False


@bot.message_handler(commands=["start"])
def send_welcome(message):
	user_registered = check_register(message.from_user.id)

	text = message.from_user.full_name + ", добро пожаловать в наш анонимный чат\!"

	if not user_registered:
		bot.send_message(message.from_user.id, text)
		register(message.from_user.id)
	else:
		search_interlocutor(message.from_user.id)


@bot.message_handler(commands=["help"])
def command_help(message):
	help(message.from_user.id)


@bot.message_handler(commands=["stop"])
def command_stop(message):
	stop_search_interlocutor(message.from_user.id)

@bot.message_handler(commands=["menu"])
def command_menu(message):
	menu(message.from_user.id)










# -------------------- База Данных --------------------
def db_request_sex(chat_id):
	# Делаем запрос данных
	sex = Users().get_field(chat_id, "sex")
	
	# Пол
	if sex == "sex_male":
		sex = "Мужской"
	else:
		sex = "Женский"
	
	text = "\n🚻 Пол\: __" + sex + "__"

	return text, sex

def db_request_age(chat_id):
	age = Users().get_field(chat_id, "age")

	# Возраст
	if age == "age_child":
		age = "До 14 лет"
	elif age == "age_teen":
		age = "14-17 лет"
	else:
		age = "18 лет и старше"
	
	text = "\n🔞 Возраст\: __" + age + "__"

	return text, age

def	db_request_premium(chat_id):
	premium = Users().get_field(chat_id, "premium")
	premium_time = Users().get_field(chat_id, "premium_time")

	if premium == True:
		premium = "Есть"
	else:
		premium = "Нет"
	
	text = "\n⚜️ Премиум\: __" + premium + "__"

	return text, premium, premium_time

def db_request_admin(chat_id):
	admin = Users().get_field(chat_id, "admin")
	admin_lvl = Users().get_field(chat_id, "admin_lvl")

	if admin_lvl == "trainee":
		admin_lvl = "Стажёр"
	elif admin_lvl == "junior":
		admin_lvl = "Младший администратор"
	elif admin_lvl == "senior":
		admin_lvl = "Старший администратор"
	elif admin_lvl == "head":
		admin_lvl = "Глава администраторов"
	elif admin_lvl == "premium":
		admin_lvl = "premium персона"
	elif admin_lvl == "owner":
		admin_lvl = "Владелец"

	text = "\n\n👑 Администратор\nУровень\: __" + admin_lvl + "__"

	return text, admin, admin_lvl
# ----------------------------------------





def send_message(text, chat_id, message_id, keyboard = None):
	if message_id == None:
		bot.send_message(chat_id, text, reply_markup = keyboard)
	else:
		bot.edit_message_text(text, chat_id, message_id, reply_markup = keyboard)





# -------------------- Кнопки под сообщениями --------------------
@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call):
	user_registered = check_register(call.message.chat.id)

	# ---------------------------------------- РЕГИСТРАЦИЯ ----------------------------------------
	if call.data == "sex_male" or call.data == "sex_female":										# При изменении пола
		if not user_registered:
			global sex
			sex = call.data

			keyboard = kb_change_age()

			bot.edit_message_text("Теперь выбери свой возраст (можно сменить в любой момент в настройках)\:", call.message.chat.id, call.message.message_id, reply_markup = keyboard)
		else:
			Users().set_field(call.message.chat.id, "sex", call.data)

			keyboard = types.InlineKeyboardMarkup();		# Клавиатура
			keyboard = kb_to_menu(keyboard)

			bot.send_message(call.message.chat.id, "Ваш пол был изменён\!", reply_markup = keyboard)
	elif call.data == "age_child" or call.data == "age_teen" or call.data == "age_adult":			# При изменении возраста
		if not user_registered:
			Users().add_id_to_db(call.message.chat.id, sex, call.data)

			keyboard = types.InlineKeyboardMarkup();		# Клавиатура

			# Кнопки
			key_start_search_interlocutor = types.InlineKeyboardButton(text = "🔍 Поиск собеседника",
				callback_data = "start_search_interlocutor")

			# Добавляем кнопки в клавиатуру
			keyboard.add(key_start_search_interlocutor)

			keyboard = kb_to_menu(keyboard)

			bot.edit_message_text("Поздравляем с регистрацией\! Теперь вы можете общаться в нашем чате\.", call.message.chat.id, call.message.message_id, reply_markup = keyboard)
		else:
			Users().set_field(call.message.chat.id, "age", call.data)

			keyboard = types.InlineKeyboardMarkup();		# Клавиатура
			keyboard = kb_to_menu(keyboard)

			bot.edit_message_text("Ваш возраст был изменён\.", call.message.chat.id, call.message.message_id, reply_markup = keyboard)
	# --------------------------------------------------------------------------------



	# Поиск
	elif call.data == "start_search_interlocutor":													# Поиск собеседника
		search_interlocutor(call.message.chat.id, call.message.message_id)
	elif call.data == "stop_search_interlocutor":													# Отмена поиска собеседника
		stop_search_interlocutor(call.message.chat.id, call.message.message_id)
	
	

	# Менюшные
	elif call.data == "profile":																	# Профиль
		profile(call.message.chat.id, call.message.message_id)
	elif call.data == "help":
		help(call.message.chat.id, call.message.message_id)
	elif call.data == "premium":
		premium(call.message.chat.id, call.message.message_id)
	


	# Другое
	elif call.data == "to_menu":																	# Возврат в меню
		menu(call.message.chat.id, call.message.message_id)
# ----------------------------------------------------------------------





def help(chat_id, message_id = None):
	text = 	"*Основные команды\:*\
			\n/start \- начать поиск собеседника\
			\n/stop \- остановить поиск / отменить диалог\
			\n/next \- отменить диалог и начать новый поиск\
			\n/link \- отправить собеседнику ссылку на свой профиль\
			\n/menu \- меню\
			\n/help \- список команд"
	
	send_message(text, chat_id, message_id)

def menu(chat_id, message_id = None):
	keyboard = types.InlineKeyboardMarkup();		# Клавиатура
	
	# Кнопки
	key_start_search_interlocutor = types.InlineKeyboardButton(text = "🔍 Поиск собеседника",
	callback_data = "start_search_interlocutor")
	key_profile = types.InlineKeyboardButton(text = "👤 Ваш профиль",
	callback_data = "profile")
	key_help = types.InlineKeyboardButton(text = "📙 Помощь",
	callback_data = "help")
	key_premium = types.InlineKeyboardButton(text = "👑 Премиум",
	callback_data = "premium")

	# Добавляем кнопки в клавиатуру
	keyboard.add(key_start_search_interlocutor)
	keyboard.add(key_profile)
	keyboard.add(key_help)
	keyboard.add(key_premium)
	
	text = "🗂 *Меню* 🗂\n\nВыбери действие\:"

	send_message(text, chat_id, message_id, keyboard)

def premium(chat_id, message_id = None):
	keyboard = types.InlineKeyboardMarkup();		# Клавиатура
	keyboard = kb_to_menu(keyboard)
	
	txt_premium, premium, premium_time = db_request_premium(chat_id)
	txt_admin, admin, admin_lvl = db_request_admin(chat_id)
	
	text = "🗂 *Премиум* 🗂\n\n"

	if admin:
		text = text + "У вас имеются права администратора уровня\: __" + admin_lvl + "__\!"
	else:
		if premium:
			text = text + "У вас уже есть премиум статус до\: __" + premium_time + "__\!"
		else:
			text = text + "У вас нет премиум статуса\. К сожалению, его пока что невозможно получить автоматическим путём\."


	send_message(text, chat_id, message_id, keyboard)



def profile(chat_id, message_id = None):
	keyboard = types.InlineKeyboardMarkup();		# Клавиатура
	keyboard = kb_to_menu(keyboard)

	text = "💼 *Профиль* 💼\n"

	txt_sex, sex = db_request_sex(chat_id)
	txt_age, age = db_request_age(chat_id)
	txt_premium, premium, premium_time = db_request_premium(chat_id)
	txt_admin, admin, admin_lvl = db_request_admin(chat_id)


	text = text + txt_sex + txt_age
	if admin:
		text = text + txt_admin
	else:
		text = text + txt_premium


	send_message(text, chat_id, message_id, keyboard)





# Проверка регистрации
def check_register(user_id):
	user_registered = False

	all_id = Users().get_all_id()
	for id in all_id:
		if id == user_id:
			user_registered = True
			break
	return user_registered
#

# -------------------- РЕГИСТРАЦИЯ --------------------
def register(chat_id, message_id = None):
	text = "🔒 Сначала нужно пройти регистрацию\!\
		\n\nВыберите ваш пол (можно сменить в любой момент в настройках)\:"

	keyboard = kb_change_sex()

	send_message(text, chat_id, message_id, keyboard)
# ----------------------------------------------------------------------





def search_interlocutor(chat_id, message_id = None):
	user_registered = check_register(chat_id)
	if user_registered:
		keyboard = types.InlineKeyboardMarkup();		# Клавиатура

		# Кнопки
		key_start_search_interlocutor = types.InlineKeyboardButton(text = "❌ Отменить поиск ❌",
			callback_data = "stop_search_interlocutor")
		
		# Добавляем кнопки в клавиатуру
		keyboard.add(key_start_search_interlocutor)
		
		global search
		text = ""
		if not search:
			search = True

			# Поиск собеседника (в ассинхронном режиме???)

			text = "🔍 Ищем собеседника\.\.\."
		else:
			text = "Поиск собеседника уже идёт\! Отменить\?"
		

		send_message(text, chat_id, message_id, keyboard)
	else:
		text = register(chat_id, message_id)

def stop_search_interlocutor(chat_id, message_id = None):
	global search
	search = False

	text = "❌ Поиск собеседника остановлен\!"

	keyboard = types.InlineKeyboardMarkup();		# Клавиатура
	keyboard = kb_to_menu(keyboard)

	send_message(text, chat_id, message_id, keyboard)





def kb_to_menu(keyboard):
	# Кнопки
	key_to_menu = types.InlineKeyboardButton(text = "⬅️ Вернуться в меню", callback_data = "to_menu")

	# Добавляем кнопки в клавиатуру
	keyboard.add(key_to_menu)

	return keyboard


def kb_change_sex():
	keyboard = types.InlineKeyboardMarkup();		# Клавиатура

	# Кнопки
	key_sex_male = types.InlineKeyboardButton(text = "🚹 Мужской 🚹", callback_data = "sex_male")
	key_sex_female= types.InlineKeyboardButton(text = "🚺 Женский 🚺", callback_data = "sex_female")

	keyboard = kb_to_menu(keyboard)

	# Добавляем кнопки в клавиатуру
	keyboard.add(key_sex_male)
	keyboard.add(key_sex_female)

	return keyboard

def kb_change_age():
	keyboard = types.InlineKeyboardMarkup();		# Клавиатура

	# Кнопки
	key_age_child = types.InlineKeyboardButton(text = "До 14 лет", callback_data = "age_child")
	key_age_teen = types.InlineKeyboardButton(text = "14-17 лет", callback_data = "age_teen")
	key_age_adult = types.InlineKeyboardButton(text = "18 лет и старше", callback_data = "age_adult")

	keyboard = kb_to_menu(keyboard)

	# Добавляем кнопки в клавиатуру
	keyboard.add(key_age_child)
	keyboard.add(key_age_teen)
	keyboard.add(key_age_adult)

	return keyboard



bot.infinity_polling(none_stop = True, interval = 0)