# -*- coding: utf-8 -*-

from telebot.async_telebot import types
import asyncio
import random

import config
from config import BOT
from config import GLOBALDATA
from config import LOCALIZATION
from modules.keyboard import InlineButtons
from modules.keyboard import ReplyButtons
import modules.database as database
import modules.functions as functions




#region -------------------- КОМАНДЫ --------------------
# Команда /start
@BOT.message_handler(commands=['start'])
async def send_welcome(message):
	# Проверка регистрации
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.Default().send_message(f"{message.from_user.full_name}, добро пожаловать в наш анонимный чат!", message.chat.id)
		await functions.AllUsers().register(message)
	else:
		await functions.Default().start_search_partner(message)

# Команда /stop
@BOT.message_handler(commands=['stop'])
async def command_stop(message):
	# Проверка регистрации
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		await functions.Default().stop_search_partner(message)

# Команда /next
@BOT.message_handler(commands=['next'])
async def command_stop(message):
	# Проверка регистрации
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		await functions.Default().next_search_partner(message)

# Команда /link
@BOT.message_handler(commands=['link'])
async def command_link(message):
	# Проверка регистрации
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		await functions.Default().communication_partner(message, True)

# Команда /menu
@BOT.message_handler(commands=['menu'])
async def command_menu(message):
	# Проверка регистрации
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		await functions.AllUsers().menu(message)

# Команда /help
@BOT.message_handler(commands=['help'])
async def command_help(message):
	# Проверка регистрации
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		await functions.AllUsers().help(message)

# Команда /premium
@BOT.message_handler(commands=['premium'])
async def command_help(message):
	# Проверка регистрации
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		await functions.AllUsers().premium(message)

# Команда /profile
@BOT.message_handler(commands=['profile'])
async def command_help(message):
	# Проверка регистрации
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		await functions.AllUsers().profile(message)

# Все сообщения
@BOT.message_handler(content_types=['text", "photo", "video", "video_note", "sticker", "document", "audio", "voice'])
async def messages(message):
	if message.content_type != "text":
		await BOT.copy_message(config.CHANNEL, message.chat.id, message.message_id)
	
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		result = database.Users().get(message.chat.id, "await").fetchone()
		if result is not None:
			if result[0] is None:
				await functions.Default().communication_partner(message)
#endregion ----------------------------------------



#region -------------------- ОБРАБОТЧИК КНОПОК --------------------
@BOT.callback_query_handler(func = lambda call: True)
async def callback_worker(call):
	# Проверка регистрации
	user_registered = await functions.AllUsers().check_register(call.message.chat.id)
	user_language = await functions.Default().get_language(call.message.chat.id)
	keyboard = types.InlineKeyboardMarkup()


	#region ----- Изменение данных -----
	# При изменении языка
	if call.data == "language_russia" or call.data == "language_english":
		text = ""
		if not user_registered:
			if len(GLOBALDATA) == 0 or GLOBALDATA[call.message.chat.id] is None:
				await functions.AllUsers().register(call.message)
			else:
				GLOBALDATA[call.message.chat.id]['language'] = call.data
				user_language = await functions.Default().language_to_code(call.data)
				text = LOCALIZATION[user_language]['register_gender']
				keyboard = await InlineButtons().change_gender(user_language, keyboard)
		else:
			database.Users().post(call.message.chat.id, "language", f"{call.data}")
			text = LOCALIZATION[user_language]['language_edited']
			keyboard = await InlineButtons().to_profile(user_language, keyboard)
			keyboard = await InlineButtons().to_menu(user_language, keyboard)
		reply_keyboard = await ReplyButtons().menu(user_language, types.ReplyKeyboardMarkup(resize_keyboard=True))
		await functions.Default().send_message("edit keyboard", call.message.chat.id, None, reply_keyboard, True)
		await functions.Default().send_message(text, call.message.chat.id, call.message.message_id, keyboard)
	
	# При изменении пола
	elif call.data == "gender_male" or call.data == "gender_female" or call.data == "gender_other":
		text = ""
		if not user_registered:
			if len(GLOBALDATA) == 0 or GLOBALDATA[call.message.chat.id] is None:
				await functions.AllUsers().register(call.message)
			else:
				GLOBALDATA[call.message.chat.id]['gender'] = call.data
				text = LOCALIZATION[user_language]['register_age']
				keyboard = await InlineButtons().change_age(user_language, keyboard)
		else:
			database.Users().post(call.message.chat.id, "gender", f"{call.data}")
			text = LOCALIZATION[user_language]['gender_edited']
			keyboard = await InlineButtons().to_profile(user_language, keyboard)
			keyboard = await InlineButtons().to_menu(user_language, keyboard)
		await functions.Default().send_message(text, call.message.chat.id, call.message.message_id, keyboard)
	
	# При изменении возраста
	elif call.data == "age_child" or call.data == "age_teen" or call.data == "age_adult":
		text = ""
		if not user_registered:
			if len(GLOBALDATA) == 0 or GLOBALDATA[call.message.chat.id] is None:
				await functions.AllUsers().register(call.message)
			else:
				GLOBALDATA[call.message.chat.id]['age'] = call.data
				database.Users().put(call.message.chat.id, GLOBALDATA[call.message.chat.id]['gender'],
					GLOBALDATA[call.message.chat.id]['age'], GLOBALDATA[call.message.chat.id]['language'])
				database.Searches().put(call.message.chat.id, "RU")
				text = LOCALIZATION[user_language]['register_finish']
				keyboard = await InlineButtons().start_search(user_language, keyboard)
				keyboard = await InlineButtons().to_menu(user_language, keyboard, LOCALIZATION[user_language]['to_menu_button'])
		else:
			database.Users().post(call.message.chat.id, "age", f"{call.data}")
			text = LOCALIZATION[user_language]['age_edited']
			keyboard = await InlineButtons().to_profile(user_language, keyboard)
			keyboard = await InlineButtons().to_menu(user_language, keyboard)
		await functions.Default().send_message(text, call.message.chat.id, call.message.message_id, keyboard)
	#endregion ---------------


	#region ----- Меню -----
	# Профиль
	elif call.data == "profile":
		await functions.AllUsers().profile(call.message, call.message.message_id)
	# Помощь
	elif call.data == "help":
		await functions.AllUsers().help(call.message, call.message.message_id)
	# Премиум
	elif call.data == "premium":
		await functions.AllUsers().premium(call.message, call.message.message_id)
	

	# Смена пола
	elif call.data == "edit_gender":
		await functions.AllUsers().change_gender(call.message, call.message.message_id)
	# Смена возраста
	elif call.data == "edit_age":
		await functions.AllUsers().change_age(call.message, call.message.message_id)
	#endregion ---------------
	

	#region ----- Поиск собеседника -----
	# Поиск
	elif call.data == "search_start_partner":
		await functions.Default().start_search_partner(call.message, call.message.message_id)
	# Отмена поиска
	elif call.data == "search_stop_partner":
		await functions.Default().stop_search_partner(call.message, call.message.message_id)
	#endregion ---------------
	

	# Возврат в меню
	elif call.data == "menu":
		await functions.AllUsers().menu(call.message, call.message.message_id)


@BOT.message_handler(func = lambda message: True)
async def handle_button_click(message):
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		user_language = await functions.Default().get_language(message.chat.id)
		if message.text == LOCALIZATION[user_language]['search_start_button']:
			await functions.Default().next_search_partner(message)
		if message.text == LOCALIZATION[user_language]['menu']:
			await functions.AllUsers().menu(message)
		if message.text == LOCALIZATION[user_language]['profile']:
			await functions.AllUsers().profile(message)
		elif message.text == LOCALIZATION[user_language]['premium']:
			await functions.AllUsers().premium(message)
		elif message.text == LOCALIZATION[user_language]['help']:
			await functions.AllUsers().help(message)
#endregion ----------------------------------------






# Поиск собеседников (отдельная задача, работающая всегда)
async def search_partners():
	print("Поиск запущен!")
	while True:
		await asyncio.sleep(1)

		# Получаем список статусов поиска пользователей
		searchesUsers = database.Searches().get(None, "user_id, search").fetchall()
		if searchesUsers is None or len(searchesUsers) < 2:
			continue

		# Перебираем всех пользователей, кто сейчас в поиске
		searchQueue = []
		for user in searchesUsers:
			if bool(user[1]) is True:
				searchQueue.append(user[0])
		
		# Если в поиске два и больше человек
		if len(searchQueue) >= 2:
			# Рандомно выбираем двух человек для беседы
			users = random.sample(searchQueue, 2)
			
			# Ещё раз на всякий случай проверяем статус поиска
			searchStatus1 = database.Searches().get(users[0], "search").fetchone()
			searchStatus2 = database.Searches().get(users[1], "search").fetchone()
			if bool(searchStatus1[0]) is True and bool(searchStatus2[0]) is True:
				database.Searches().post(users[0], "search", 0)
				database.Searches().post(users[1], "search", 0)

				database.Chats().put(users[0], users[1])
				database.Chats().put(users[1], users[0])

				
				user_language = await functions.Default().get_language(users[0])
				keyboard = await InlineButtons().stop_search(types.InlineKeyboardMarkup(),
					LOCALIZATION[user_language]['dialog_stop_button'])
				await functions.Default().send_message(LOCALIZATION[user_language]['searched'], users[0], None, keyboard)

				
				user_language = await functions.Default().get_language(users[1])
				keyboard = await InlineButtons().stop_search(types.InlineKeyboardMarkup(),
					LOCALIZATION[user_language]['dialog_stop_button'])
				await functions.Default().send_message(LOCALIZATION[user_language]['searched'], users[1], None, keyboard)


async def main():
	# Стартуем бота
	asyncio.create_task(BOT.polling())
	print("Бот запущен!")
	# Стартуем поиск собеседников
	await asyncio.create_task(search_partners())


asyncio.run(main())