# -*- coding: utf-8 -*-

from email import message
from telebot.async_telebot import AsyncTeleBot
from telebot.async_telebot import types
import asyncio

from config import TOKEN
from database import Users

from atexit import register
from cgitb import text
from tabnanny import check
from unicodedata import name
from xml.dom.domreg import registered
from random import randint


import datetime


globalVar = {}



bot = AsyncTeleBot(TOKEN, parse_mode="HTML")


# Команда /start
@bot.message_handler(commands=["start"])
async def send_welcome(message):
	user_registered = await check_user_in_globalVar(message.chat.id)

	text = message.from_user.full_name + ", добро пожаловать в наш анонимный чат!"

	if not user_registered:
		await send_message(text, message.chat.id)
		await register(message)
	else:
		await search_interlocutor(message)


# Команда /stop
@bot.message_handler(commands=["stop"])
async def command_stop(message):
	user_registered = await check_user_in_globalVar(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		await stop_search_interlocutor(message)


# Команда /link
@bot.message_handler(commands=["link"])
async def command_link(message):
	user_registered = await check_user_in_globalVar(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		await communication_interlocutor(message, True)

# Команда /menu
@bot.message_handler(commands=["menu"])
async def command_menu(message):
	user_registered = await check_user_in_globalVar(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		await menu(message)

# Команда /help
@bot.message_handler(commands=["help"])
async def command_help(message):
	user_registered = await check_user_in_globalVar(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		await help(message)



@bot.message_handler(content_types=["text"])
async def messages(message):
	await communication_interlocutor(message)









# Клавиатура
async def search_dialog():
	keyboard = types.InlineKeyboardMarkup();

	# Кнопки
	key_stop_search_interlocutor = types.InlineKeyboardButton("❌ Остановить диалог ❌",
		callback_data = "stop_search_interlocutor")
	
	# Добавляем кнопки в клавиатуру
	keyboard.add(key_stop_search_interlocutor)

	txt = "Собеседник найден. Общайтесь!"
	global globalVar



	while True:
		all_id = Users().get_all_id()
		ids_searchs = []


		# --------------- Перебираем всех пользователей, кто сейчас в поиске ---------------
		for id in all_id:
			user_registered = await check_user_in_globalVar(id)
			if globalVar[id]["user_status"] == "Search":
				ids_searchs.append(id)
		# ------------------------------------------------------------------------------------------
		
		
		# --------------- Если в поиске два и больше человек ---------------
		if len(ids_searchs) >= 2:
			rnd1 = randint(0, (len(ids_searchs)-1))
			rnd2 = randint(0, (len(ids_searchs)-1))
			if rnd2 == rnd1:
				while rnd2 == rnd1:
					rnd2 = randint(0, (len(ids_searchs)-1))
			
			id1 = ids_searchs[rnd1]
			id2 = ids_searchs[rnd2]

			if globalVar[id1]["user_status"] == "Search" and globalVar[id2]["user_status"] == "Search":
				Users().set_field(id1, "interlocutor", id2)
				Users().set_field(id2, "interlocutor", id1)

				globalVar[id1]["user_status"] = "Message"
				globalVar[id2]["user_status"] = "Message"

				await send_message(txt, id1, None, keyboard)
				await send_message(txt, id2, None, keyboard)
		# ---------------------------------------------------------------------------

		await asyncio.sleep(1)






async def communication_interlocutor(message, link = False):
	user_registered = await check_user_in_globalVar(message.chat.id)
	if user_registered:
		interlocutor = Users().get_field(message.chat.id, "interlocutor")
		if interlocutor == None:
			await send_message("❌ У вас нет собеседников, кому вы могли бы отправить сообщение!",
				message.chat.id)
		else:
			text = ""
			if link:
				txt = "❌ У вас нет имени пользователя!"
				if message.from_user.username != None:
					text = "🔗 Ссылка на собеседника: " + "@" + message.from_user.username
					txt = "✅ Ссылка успешно отправлена собеседнику!"
				await send_message(txt, message.chat.id)
			else:
				text = message.text
			
			await send_message(text, interlocutor)
	else:
		await register(message)










async def send_message(text, chat_id, message_id = None, keyboard = None):
	if message_id == None:
		await bot.send_message(chat_id, text, reply_markup = keyboard)
	else:
		await bot.edit_message_text(text, chat_id, message_id, reply_markup = keyboard)







# -------------------- База Данных --------------------
async def db_request_sex(user_id):
	# Делаем запрос данных
	sex = Users().get_field(user_id, "sex")
	
	# Пол
	if sex == "sex_male":
		sex = "Мужской"
	else:
		sex = "Женский"
	
	text = "\n🚻 Пол: <i>" + sex + "</i>"

	return text, sex

async def db_request_age(user_id):
	age = Users().get_field(user_id, "age")

	# Возраст
	if age == "age_child":
		age = "До 14 лет"
	elif age == "age_teen":
		age = "14-17 лет"
	else:
		age = "18 лет и старше"
	
	text = "\n🔞 Возраст: <i>" + age + "</i>"

	return text, age

async def db_request_premium(user_id):
	premium = Users().get_field(user_id, "premium")
	premium_time = Users().get_field(user_id, "premium_time")


	txt = ""
	if premium == True:
		premium = "Есть"

		txt = "\nВремя действия до: <i>"
		if premium_time == None:
			txt = txt + "пожизнено</i>"
		else:
			spl_dt = premium_time.split()
			spl_ymd = spl_dt[0].split("-")
			spl_hms = spl_dt[1].split(":")

			txt = txt + f"{spl_ymd[2]}-{spl_ymd[1]}-{spl_ymd[0]} {spl_hms[0]}:{spl_hms[1]}:{spl_hms[2]}</i>"
	else:
		premium = "Нет"
	
	text = "\n\n⚜️ Премиум: <i>" + premium + "</i>" + txt

	return text, premium, premium_time

async def db_request_admin(user_id):
	admin = Users().get_field(user_id, "admin")
	admin_lvl = Users().get_field(user_id, "admin_lvl")

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
	else:
		admin_lvl = "Нет"

	text = "\n\n👑 Администратор\nУровень: <i>" + admin_lvl + "</i>"

	return text, admin, admin_lvl
# ----------------------------------------





# -------------------- Кнопки под сообщениями --------------------
@bot.callback_query_handler(func = lambda call: True)
async def callback_worker(call):
	user_registered = await check_user_in_globalVar(call.message.chat.id)

	# ---------------------------------------- РЕГИСТРАЦИЯ ----------------------------------------
	if call.data == "sex_male" or call.data == "sex_female":										# При изменении пола
		keyboard = types.InlineKeyboardMarkup();		# Клавиатура
		text = ""
		if not user_registered:
			globalVar[call.message.chat.id]["sex"] = call.data

			keyboard = await kb_change_age(keyboard)

			text = "Теперь выбери свой возраст (можно сменить в любой момент в настройках):"
		else:
			Users().set_field(call.message.chat.id, "sex", call.data)

			keyboard = await kb_to_menu(keyboard)

			text = "Ваш пол был изменён!"

		await send_message(text, call.message.chat.id, call.message.message_id, keyboard)
	elif call.data == "age_child" or call.data == "age_teen" or call.data == "age_adult":			# При изменении возраста
		keyboard = types.InlineKeyboardMarkup();		# Клавиатура
		text = ""
		if not user_registered:
			globalVar[call.message.chat.id]["age"] = call.data
			Users().add_id_to_db(call.message.chat.id,
				globalVar[call.message.chat.id]["sex"], globalVar[call.message.chat.id]["age"])

			# Кнопки
			key_start_search_interlocutor = types.InlineKeyboardButton(text = "🔍 Поиск собеседника",
				callback_data = "start_search_interlocutor")

			# Добавляем кнопки в клавиатуру
			keyboard.add(key_start_search_interlocutor)

			keyboard = await kb_to_menu(keyboard)

			text = "Поздравляем с регистрацией! Теперь вы можете общаться в нашем чате."
		else:
			Users().set_field(call.message.chat.id, "age", call.data)

			keyboard = await kb_to_menu(keyboard)

			text = "Ваш возраст был изменён."

		await send_message(text, call.message.chat.id, call.message.message_id, keyboard)
	elif call.data == "end_reg":
		keyboard = types.InlineKeyboardMarkup();		# Клавиатура
	# --------------------------------------------------------------------------------



	# Поиск
	elif call.data == "start_search_interlocutor":													# Поиск собеседника
		await search_interlocutor(call.message, call.message.message_id)
	elif call.data == "stop_search_interlocutor":													# Отмена поиска собеседника
		await stop_search_interlocutor(call.message, call.message.message_id)
	

	# Менюшные
	elif call.data == "profile":																	# Профиль
		await profile(call.message, call.message.message_id)
	elif call.data == "help":
		await help(call.message, call.message.message_id)
	elif call.data == "premium":
		await premium(call.message, call.message.message_id)
	elif call.data == "get_premium":
		await give_premium(call.message.chat.id, 30, call.message, call.message.message_id)
	


	# Другое
	elif call.data == "to_menu":																	# Возврат в меню
		await menu(call.message, call.message.message_id)
# ----------------------------------------------------------------------





async def help(message, message_id = None):
	text = 	"<b>Основные команды:</b>\
			\n/start - начать поиск собеседника\
			\n/stop - остановить поиск / отменить диалог\
			\n/next - отменить диалог и начать новый поиск\
			\n/link - отправить собеседнику ссылку на свой профиль\
			\n/menu - меню\
			\n/help - список команд"
	
	await send_message(text, message.chat.id, message_id)

async def menu(message, message_id = None):
	keyboard = types.InlineKeyboardMarkup();		# Клавиатура
	
	# Кнопки
	key_start_search_interlocutor = types.InlineKeyboardButton(text = "🔍 Поиск собеседника",
		callback_data = "start_search_interlocutor")
	key_profile = types.InlineKeyboardButton(text = "👤 Ваш профиль",
		callback_data = "profile")
	key_help = types.InlineKeyboardButton(text = "📙 Помощь",
		callback_data = "help")
	key_premium = types.InlineKeyboardButton(text = "⚜️ Премиум",
		callback_data = "premium")

	# Добавляем кнопки в клавиатуру
	keyboard.add(key_start_search_interlocutor)
	keyboard.add(key_profile)
	keyboard.add(key_help)
	keyboard.add(key_premium)
	
	text = "🗂 <b>Меню</b> 🗂\n\nВыбери действие:"

	await send_message(text, message.chat.id, message_id, keyboard)

async def premium(message, message_id = None):
	keyboard = types.InlineKeyboardMarkup();		# Клавиатура
	
	txt_premium, premium, premium_time = await db_request_premium(message.chat.id)
	txt_admin, admin, admin_lvl = await db_request_admin(message.chat.id)
	
	text = "🗂 <b>Премиум</b> 🗂"

	if admin:
		text = text + txt_admin
	else:
		if premium == "Есть":
			text = text + txt_premium
		else:
			text = text + "\n\nУ вас нет премиум статуса.\nПолучить?."

			# Кнопки
			key_get_premium = types.InlineKeyboardButton(text = "⚜️ Получить!", callback_data = "get_premium")

			# Добавляем кнопки в клавиатуру
			keyboard.add(key_get_premium)



	keyboard = await kb_to_menu(keyboard)
	await send_message(text, message.chat.id, message_id, keyboard)



async def profile(message, message_id = None):
	keyboard = types.InlineKeyboardMarkup();		# Клавиатура

	text = "💼 <b>Профиль</b> 💼\n"

	txt_sex, sex = await db_request_sex(message.chat.id)
	txt_age, age = await db_request_age(message.chat.id)
	txt_premium, premium, premium_time = await db_request_premium(message.chat.id)
	txt_admin, admin, admin_lvl = await db_request_admin(message.chat.id)


	text = text + txt_sex + txt_age
	if admin:
		text = text + txt_admin
	else:
		text = text + txt_premium

	keyboard = await kb_to_menu(keyboard)
	await send_message(text, message.chat.id, message_id, keyboard)



async def give_premium(user, time, message, message_id = None):
	user_registered = await check_user_in_globalVar(user)
	if user_registered:
		keyboard = types.InlineKeyboardMarkup();		# клавиатура
		txt_premium, premium, premium_time = await db_request_premium(user)
		txt_admin, admin, admin_lvl = await db_request_admin(user)


		if premium_time != None:
			spl_dt = premium_time.split()
			spl_ymd = spl_dt[0].split("-")
			spl_hms = spl_dt[1].split(":")

			str_premium_time = f"{spl_ymd[2]}-{spl_ymd[1]}-{spl_ymd[0]} {spl_hms[0]}:{spl_hms[1]}:{spl_hms[2]}"


		text = ""
		if admin:
			text = "У вас уже есть права администратора уровня: <i>" + admin_lvl + "</i>!"
		else:
			if premium == "Есть":
				text - "У вас уже есть премиум до: <i>" + str_premium_time + "</i>!"
			else:
				date = await now_date()

				delta = datetime.timedelta(days = time)
				need_date = date + delta

				# Обновляем
				Users().set_field(user, "premium", True)
				Users().set_field(user, "premium_time", need_date)

				if message.chat.id == user:
					text = "Поздравляем с получением премиума на: <i>" + str(time) + " дней</i>!"
				else:
					text = "Пользователь с id \"<i>" + user + "</i>\" получил премиум на \"<i>" + str(time) + " дней</i>\"."
					txt = "⚜️ Вы получили премиум статус на \"<i>" + str(time) +" дней</i>\" \
						от администратора с уровнем \"<i>" + admin_lvl + "</i>\"!"
					await send_message(txt, user)

		keyboard = await kb_to_menu(keyboard)
		await send_message(text, message.chat.id, message_id, keyboard)
	else:
		text = "Пользователь с id \"<i>" + user + "</i>\" не зарегестрирован!"
		await send_message(text, message.chat.id, message_id)




# Проверка регистрации
async def check_register(chat_id):
	user_registered = False
	all_id = Users().get_all_id()
	for id in all_id:
		if id == chat_id:
			user_registered = True
			break
	return user_registered
#

# -------------------- РЕГИСТРАЦИЯ --------------------
async def register(message, message_id = None):
	text = "🔒 Сначала нужно пройти регистрацию!\
		\n\nВыберите ваш пол (можно сменить в любой момент в настройках):"

	keyboard = types.InlineKeyboardMarkup();		# Клавиатура

	keyboard = await kb_change_sex(keyboard)

	await send_message(text, message.chat.id, message_id, keyboard)
# ----------------------------------------------------------------------





async def search_interlocutor(message, message_id = None):
	user_registered = await check_user_in_globalVar(message.chat.id)
	if user_registered:
		interlocutor = Users().get_field(message.chat.id, "interlocutor")
		
		text = ""
		btn_txt = "❌ Отменить поиск ❌"

		if interlocutor == None:
			if globalVar[message.chat.id]["user_status"] == "None":
				globalVar[message.chat.id]["user_status"] = "Search"
				text = "🔍 Ищем собеседника..."
			elif globalVar[message.chat.id]["user_status"] == "Search":
				text = "Поиск собеседника уже идёт!\nОтменить?"
		else:
			btn_txt = "❌ Остановить диалог ❌"
			text = "Вы уже в диалоге. Остановить его?"
		

		keyboard = types.InlineKeyboardMarkup();		# Клавиатура

		# Кнопки
		key_stop_search_interlocutor = types.InlineKeyboardButton(text = btn_txt,
			callback_data = "stop_search_interlocutor")
		
		# Добавляем кнопки в клавиатуру
		keyboard.add(key_stop_search_interlocutor)
		
		await send_message(text, message.chat.id, message_id, keyboard)
	else:
		await register(message)

async def stop_search_interlocutor(message, message_id = None):
	user_registered = await check_user_in_globalVar(message.chat.id)
	if user_registered:
		interlocutor = Users().get_field(message.chat.id, "interlocutor")

		keyboard = types.InlineKeyboardMarkup();		# Клавиатура

		# Кнопки
		key_search = types.InlineKeyboardButton(text = "🔍 Начать поиск", callback_data = "start_search_interlocutor")

		# Добавляем кнопки в клавиатуру
		keyboard.add(key_search)

		keyboard = await kb_to_menu(keyboard)

		text = ""
		if interlocutor == None:
			if globalVar[message.chat.id]["user_status"] == "None":
				text = "У вас нет активного поиска / диалога!"
			elif globalVar[message.chat.id]["user_status"] == "Search":
				globalVar[message.chat.id]["user_status"] = "None"
				text = "❌ Поиск собеседника остановлен!"
		else:
			# Останавливаем диалог собеседнику и пользователю
			Users().set_field(message.chat.id, "interlocutor", None)
			Users().set_field(interlocutor, "interlocutor", None)

			globalVar[message.chat.id]["user_status"] = "None"
			globalVar[interlocutor]["user_status"] = "None"


			text = "❌ Диалог остановлен!"
			await send_message("❌ Собеседник остановил диалог.", interlocutor, None, keyboard)
		
		await send_message(text, message.chat.id, message_id, keyboard)
	else:
		await register(message)





async def kb_to_menu(keyboard):
	# Кнопки
	key_to_menu = types.InlineKeyboardButton(text = "⬅️ Вернуться в меню", callback_data = "to_menu")

	# Добавляем кнопки в клавиатуру
	keyboard.add(key_to_menu)

	return keyboard


async def kb_change_sex(keyboard):
	# Кнопки
	key_sex_male = types.InlineKeyboardButton(text = "🚹 Мужской 🚹", callback_data = "sex_male")
	key_sex_female= types.InlineKeyboardButton(text = "🚺 Женский 🚺", callback_data = "sex_female")

	# Добавляем кнопки в клавиатуру
	keyboard.add(key_sex_male)
	keyboard.add(key_sex_female)

	return keyboard

async def kb_change_age(keyboard):
	# Кнопки
	key_age_child = types.InlineKeyboardButton(text = "До 14 лет", callback_data = "age_child")
	key_age_teen = types.InlineKeyboardButton(text = "14-17 лет", callback_data = "age_teen")
	key_age_adult = types.InlineKeyboardButton(text = "18 лет и старше", callback_data = "age_adult")

	# Добавляем кнопки в клавиатуру
	keyboard.add(key_age_child)
	keyboard.add(key_age_teen)
	keyboard.add(key_age_adult)

	return keyboard







async def check_user_in_globalVar(user_id):
	in_base = False
	for id in globalVar:
		if id == user_id:
			in_base = True
			break
	
	if not in_base:
		globalVar[user_id] = {"sex":"None", "age":"None", "user_status":"None",}
	
	user_registered = await check_register(user_id)
	if user_registered:
		interlocutor = Users().get_field(user_id, "interlocutor")
		if interlocutor != None:
			globalVar[user_id]["user_status"] = "Message"
	
	return user_registered



async def now_date():
	now = datetime.datetime.now()

	date = datetime.date(now.year, now.month, now.day)
	time = datetime.time(now.hour, now.minute)
	now_date = datetime.datetime.combine(date, time)

	return now_date






async def main():
	task1 = asyncio.create_task(bot.polling())
	task2 = asyncio.create_task(search_dialog())

	await task1
	await task2


asyncio.run(main())