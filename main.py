# -*- coding: utf-8 -*-

from telebot.async_telebot import AsyncTeleBot
from telebot.async_telebot import types
import asyncio
import random

from config import TOKEN
from keyboard import Buttons
from database import Users
from database import Chats


globalVar = {}


# Сам бот
bot = AsyncTeleBot(TOKEN, parse_mode="HTML")



# -------------------- СООБЩЕНИЯ --------------------
# Отправить сообщение пользователю
async def send_message(text, chat_id, message_id = None, keyboard = None):
	if message_id == None:
		await bot.send_message(chat_id, text, reply_markup = keyboard)
	else:
		await bot.edit_message_text(text, chat_id, message_id, reply_markup = keyboard)

# Общение с собеседником
async def communication_partner(message, link = False):
	# Проверка на регистрацию
	user_registered = await check_register(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		partner = Chats().get(message.chat.id, "partner_user_id").fetchone()
		if partner[0] is None:
			await send_message("❌ У вас нет собеседников, кому вы могли бы отправить сообщение!", message.chat.id)
		else:
			if link:
				text = "❌ У вас нет имени пользователя!"
				if message.from_user.username is not None:
					partner_text = f"🔗 Ссылка на собеседника: @{message.from_user.username}"
					await send_message(partner_text, partner)
					text = "✅ Ссылка успешно отправлена собеседнику!"
				await send_message(text, message.chat.id)
			else:
				await send_message(message.text, partner)
# ----------------------------------------



# -------------------- КОМАНДЫ --------------------
# Команда /start
@bot.message_handler(commands=["start"])
async def send_welcome(message):
	# Проверка регистрации
	user_registered = await check_register(message.chat.id)
	if not user_registered:
		await send_message(f"{message.from_user.full_name}, добро пожаловать в наш анонимный чат!", message.chat.id)
		await register(message)
	else:
		await start_search_partner(message)

# Команда /stop
@bot.message_handler(commands=["stop"])
async def command_stop(message):
	# Проверка регистрации
	user_registered = await check_register(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		await stop_search_partner(message)

# Команда /link
@bot.message_handler(commands=["link"])
async def command_link(message):
	# Проверка регистрации
	user_registered = await check_register(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		await communication_partner(message, True)

# Команда /menu
@bot.message_handler(commands=["menu"])
async def command_menu(message):
	# Проверка регистрации
	user_registered = await check_register(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		await menu(message)

# Команда /help
@bot.message_handler(commands=["help"])
async def command_help(message):
	# Проверка регистрации
	user_registered = await check_register(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		await help(message)

# Все остальные сообщения
@bot.message_handler(content_types=["text"])
async def messages(message):
	await communication_partner(message)
# ----------------------------------------



# -------------------- ОБРАБОТЧИК КНОПОК --------------------
@bot.callback_query_handler(func = lambda call: True)
async def callback_worker(call):
	# Проверка регистрации
	user_registered = await check_register(call.message.chat.id)
	keyboard = types.InlineKeyboardMarkup()


	# ----- Изменение данных -----
	# При изменении пола
	if call.data == "gender_male" or call.data == "gender_female" or call.data == "gender_other":
		text = ""
		if not user_registered:
			globalVar[call.message.chat.id]["gender"] = call.data
			text = "Теперь выбери свой возраст (можно сменить в любой момент в настройках):"
			keyboard = await Buttons().change_age(keyboard)
		else:
			Users().post(call.message.chat.id, "gender", call.data)
			text = "Ваш пол был изменён!"
			keyboard = await Buttons().to_menu(keyboard)
		await send_message(text, call.message.chat.id, call.message.message_id, keyboard)
	
	# При изменении возраста
	elif call.data == "age_child" or call.data == "age_teen" or call.data == "age_adult":
		text = ""
		if not user_registered:
			# Вносим данные
			globalVar[call.message.chat.id]["age"] = call.data
			Users().put(call.message.chat.id, globalVar[call.message.chat.id]["gender"], globalVar[call.message.chat.id]["age"])
			text = "Поздравляем с регистрацией! Теперь вы можете общаться в нашем чате."
			keyboard = await Buttons().start_search(keyboard)
			keyboard = await Buttons().to_menu(keyboard)
		else:
			Users().post(call.message.chat.id, "age", call.data)
			text = "Ваш возраст был изменён."
			keyboard = await Buttons().to_menu(keyboard)
		await send_message(text, call.message.chat.id, call.message.message_id, keyboard)
	# ---------------

	

	# ----- Меню -----
	# Профиль
	elif call.data == "profile":
		await profile(call.message, call.message.message_id)
	# Помощь
	elif call.data == "help":
		await help(call.message, call.message.message_id)
	# ---------------
	
	

	# ----- Поиск собеседника -----
	# Поиск
	elif call.data == "start_search_partner":
		await start_search_partner(call.message, call.message.message_id)
	# Отмена поиска
	elif call.data == "stop_search_partner":
		await stop_search_partner(call.message, call.message.message_id)
	# ---------------
	

	# Возврат в меню
	elif call.data == "to_menu":
		await menu(call.message, call.message.message_id)
# ----------------------------------------



# -------------------- ФУНКЦИИ --------------------
# Помощь
async def help(message, message_id = None):
	text = 	"<b>Основные команды:</b>\
			\n/start - начать поиск собеседника\
			\n/stop - остановить поиск / отменить диалог\
			\n/next - отменить диалог и начать новый поиск\
			\n/link - отправить собеседнику ссылку на свой профиль\
			\n/menu - меню\
			\n/help - список команд"
	
	# Клавиатура
	keyboard = await Buttons().to_menu(types.InlineKeyboardMarkup())
	await send_message(text, message.chat.id, message_id, keyboard)


# Меню
async def menu(message, message_id = None):
	# Клавиатура
	keyboard = await Buttons().start_search(types.InlineKeyboardMarkup())
	keyboard.add(types.InlineKeyboardButton(text = "👤 Ваш профиль", callback_data = "profile"))
	keyboard.add(types.InlineKeyboardButton(text = "📙 Помощь", callback_data = "help"))
	
	text = "🗂 <b>Меню</b> 🗂\n\nВыберите действие:"
	await send_message(text, message.chat.id, message_id, keyboard)


# Профиль
async def profile(message, message_id = None):
	txt_gender, gender = await db_request_gender(message.chat.id)
	txt_age, age = await db_request_age(message.chat.id)

	text = f"💼 <b>Профиль</b> 💼\n{txt_gender}\n{txt_age}"

	# Клавиатура
	keyboard = await Buttons().to_menu(types.InlineKeyboardMarkup())
	await send_message(text, message.chat.id, message_id, keyboard)
# ----------------------------------------



# -------------------- ДАННЫЕ ПОЛЬЗОВАТЕЛЯ --------------------
# Получить пол
async def db_request_gender(user_id):
	# Делаем запрос данных
	result = Users().get(user_id, "gender").fetchone()
	gender = result[0]

	# Пол
	if gender == "gender_male":
		gender = "Мужской"
	elif gender == "gender_female":
		gender = "Женский"
	else:
		gender = "Другой"

	text = f"\n🚻 Пол: <i>{gender}</i>"
	return text, gender

# Получить возраст
async def db_request_age(user_id):
	result = Users().get(user_id, "age").fetchone()
	age = result[0]

	# Возраст
	if age == "age_child":
		age = "До 14 лет"
	elif age == "age_teen":
		age = "14-17 лет"
	else:
		age = "18 лет и старше"

	text = f"\n🔞 Возраст: <i>{age}</i>"
	return text, age
# ----------------------------------------



# -------------------- РЕГИСТРАЦИЯ --------------------
# Проверка регистрации
async def check_register(chat_id):
	user_registered = False
	result = Users().get(chat_id).fetchone()
	if result[0] is not None:
		user_registered = True
	return user_registered

# Регистрация
async def register(message, message_id = None):
	globalVar[message.chat.id] = {"gender":"None", "age":"None"}
	text = "🔒 Сначала нужно пройти регистрацию!\n\nВыберите ваш пол (можно сменить в любой момент в настройках):"
	keyboard = await Buttons().change_gender(types.InlineKeyboardMarkup())
	await send_message(text, message.chat.id, message_id, keyboard)
# ----------------------------------------









# -------------------- ПОИСК --------------------
# Поиск собеседника
async def start_search_partner(message, message_id = None):
	# Проверка регистрации
	user_registered = await check_register(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		text = "Поиск собеседника уже идёт!\nОтменить?"
		btn_txt = "❌ Отменить поиск ❌"

		searchStatus = Users().get(message.chat.id, "search").fetchone()
		if searchStatus[0] == 0:
			Users().post(message.chat.id, "search", 1)
			text = "🔍 Ищем собеседника..."
		
		partner = Chats().get(message.chat.id, "partner_user_id").fetchone()
		if partner[0] is not None:
			text = "Вы уже в диалоге. Остановить его?"
			btn_txt = "❌ Остановить диалог ❌"

		# Клавиатура
		keyboard = await Buttons().stop_search(types.InlineKeyboardMarkup(), btn_txt)
		await send_message(text, message.chat.id, message_id, keyboard)

# Остановить диалог/поиск собеседника
async def stop_search_partner(message, message_id = None):
	# Проверка регистрации
	user_registered = await check_register(message.chat.id)
	if not user_registered:
		await register(message)
	else:
		text = "У вас нет активного поиска / диалога!"
		
		searchStatus = Users().get(message.chat.id, "search").fetchone()
		if searchStatus[0] == 1:
			Users().post(message.chat.id, "search", 0)
			text = "❌ Поиск собеседника остановлен!"

		partner = Chats().get(message.chat.id, "partner_user_id").fetchone()
		if partner[0] is not None:
			Chats().delete(message.chat.id)
			Chats().delete(partner[0])
			await send_message("❌ Собеседник остановил диалог.", partner[0], None, keyboard)
			text = "❌ Диалог остановлен!"

		# Клавиатура
		keyboard = await Buttons().start_search(types.InlineKeyboardMarkup())
		keyboard = await Buttons().to_menu(keyboard)
		await send_message(text, message.chat.id, message_id, keyboard)
# ----------------------------------------

# Поиск собеседников (отдельная задача, работающая всегда)
async def search_partners():
	keyboard = Buttons().stop_search(types.InlineKeyboardMarkup(), "❌ Остановить диалог ❌")
	txt = "Собеседник найден. Общайтесь!"
	
	while True:
		await asyncio.sleep(1)

		# Получаем список статусов поиска пользователей
		searchesUsers = Users().get(None, "id, search").fetchall()
		if len(searchesUsers) == 0:
			continue

		# Перебираем всех пользователей, кто сейчас в поиске
		searchQueue = []
		for user in searchesUsers:
			if user[1] is True:
				searchQueue.append(user[0])
		
		
		# Если в поиске два и больше человек - соединяем
		if len(searchQueue) >= 2:
			# Рандомно выбираем двух человек для беседы
			users = random.sample(searchQueue, 2)
			
			# Ещё раз на всякий случай проверяем статус поиска
			searchStatus1 = Users().get(users[0], "search").fetchone()
			searchStatus2 = Users().get(users[1], "search").fetchone()
			if searchStatus1[0] == 1 and searchStatus2[0] == 1:
				Users().post(users[0], "search", 0)
				Users().post(users[1], "search", 0)

				Chats().put(users[0], users[1])
				Chats().put(users[1], users[0])
				await send_message(txt, users[0], None, keyboard)
				await send_message(txt, users[1], None, keyboard)


async def main():
	# Стартуем бота
	await asyncio.create_task(bot.polling())
	# Стартуем поиск собеседников
	await asyncio.create_task(search_partners())
	print("Бот успешно запущен!")


asyncio.run(main())