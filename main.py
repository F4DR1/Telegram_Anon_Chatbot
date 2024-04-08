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
@BOT.message_handler(content_types=['text', 'photo', 'video', 'video_note', 'sticker', 'document', 'audio', 'voice'])
async def messages(message):
	if message.content_type != "text":
		await BOT.copy_message(config.CHANNEL, message.chat.id, message.message_id)
	
	user_registered = await functions.AllUsers().check_register(message.chat.id)
	if not user_registered:
		await functions.AllUsers().register(message)
	else:
		user_language = await functions.Default().get_language(message.chat.id)
		if message.text == LOCALIZATION[user_language]['search_start_button']:
			await functions.Default().next_search_partner(message)
		elif message.text == LOCALIZATION[user_language]['menu']:
			await functions.AllUsers().menu(message)
		elif message.text == LOCALIZATION[user_language]['profile']:
			await functions.AllUsers().profile(message)
		elif message.text == LOCALIZATION[user_language]['search_settings']:
			await functions.AllUsers().search_settings(message)
		elif message.text == LOCALIZATION[user_language]['premium']:
			await functions.AllUsers().premium(message)
		elif message.text == LOCALIZATION[user_language]['help']:
			await functions.AllUsers().help(message)

		
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
			user_language = await functions.Default().get_language(call.message.chat.id)
			text = LOCALIZATION[user_language]['language_edited']
			keyboard = await InlineButtons().to_profile(user_language, keyboard)
			keyboard = await InlineButtons().to_menu(user_language, keyboard)
		reply_keyboard = await ReplyButtons().menu(user_language, types.ReplyKeyboardMarkup(resize_keyboard=True))
		await functions.Default().send_message(
			LOCALIZATION[user_language]['edit_reply_keyboard'], call.message.chat.id, None, reply_keyboard)
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
				database.Searches().put(call.message.chat.id, GLOBALDATA[call.message.chat.id]['language'])
				text = LOCALIZATION[user_language]['register_finish']
				keyboard = await InlineButtons().start_search(user_language, keyboard)
				keyboard = await InlineButtons().to_menu(user_language, keyboard, LOCALIZATION[user_language]['to_menu_button'])
		else:
			database.Users().post(call.message.chat.id, "age", f"{call.data}")
			text = LOCALIZATION[user_language]['age_edited']
			keyboard = await InlineButtons().to_profile(user_language, keyboard)
			keyboard = await InlineButtons().to_menu(user_language, keyboard)
		await functions.Default().send_message(text, call.message.chat.id, call.message.message_id, keyboard)
	
	
	
	else:
		if not user_registered:
			await functions.AllUsers().register(call.message, call.message.message_id)
		else:
			# При изменении языка поиска
			if call.data == "search_language_all" or call.data == "search_language_russia" or \
				call.data == "search_language_english":

				language = (call.data)[7:]
				if language == "language_all":
					language = "all"

				database.Searches().post(call.message.chat.id, "language", language)
				text = LOCALIZATION[user_language]['language_search_edited']
				keyboard = await InlineButtons().to_search_settings(user_language, keyboard)
				keyboard = await InlineButtons().to_menu(user_language, keyboard)
				await functions.Default().send_message(text, call.message.chat.id, call.message.message_id, keyboard)
			
			# При изменении пола поиска
			elif call.data == "search_gender_all" or call.data == "search_gender_male" or \
				call.data == "search_gender_female" or call.data == "search_gender_other":

				gender = (call.data)[7:]
				if gender == "gender_all":
					gender = "all"

				database.Searches().post(call.message.chat.id, "gender", f"{gender}")
				text = LOCALIZATION[user_language]['gender_search_edited']
				keyboard = await InlineButtons().to_search_settings(user_language, keyboard)
				keyboard = await InlineButtons().to_menu(user_language, keyboard)
				await functions.Default().send_message(text, call.message.chat.id, call.message.message_id, keyboard)
			
			# При изменении возраста поиска
			elif call.data == "search_age_all" or call.data == "search_age_child" or \
				call.data == "search_age_teen" or call.data == "search_age_adult":

				age = (call.data)[7:]
				if age == "age_all":
					age = "all"

				database.Searches().post(call.message.chat.id, "age", f"{age}")
				text = LOCALIZATION[user_language]['age_search_edited']
				keyboard = await InlineButtons().to_search_settings(user_language, keyboard)
				keyboard = await InlineButtons().to_menu(user_language, keyboard)
				await functions.Default().send_message(text, call.message.chat.id, call.message.message_id, keyboard)
	#endregion ---------------


			#region ----- Меню -----
			# Возврат в меню
			elif call.data == "menu":
				await functions.AllUsers().menu(call.message, call.message.message_id)

			
			# Профиль
			elif call.data == "profile":
				await functions.AllUsers().profile(call.message, call.message.message_id)
			# Помощь
			elif call.data == "help":
				await functions.AllUsers().help(call.message, call.message.message_id)
			# Премиум
			elif call.data == "premium":
				await functions.AllUsers().premium(call.message, call.message.message_id)
			# Настройки поиска
			elif call.data == "search_settings":
				await functions.AllUsers().search_settings(call.message, call.message.message_id)
			

			# Смена языка
			elif call.data == "edit_language":
				await functions.AllUsers().change_language(call.message, call.message.message_id)
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
			

			# Смена языка
			elif call.data == "edit_search_language":
				await functions.AllUsers().change_language(call.message, call.message.message_id, True)
			# Смена пола
			elif call.data == "edit_search_gender":
				await functions.AllUsers().change_gender(call.message, call.message.message_id, True)
			# Смена возраста
			elif call.data == "edit_search_age":
				await functions.AllUsers().change_age(call.message, call.message.message_id, True)
			#endregion ---------------
#endregion ----------------------------------------







# Поиск собеседников (отдельная задача, работающая всегда)
async def random_search_partners():
	print("Поиск запущен!")
	while True:
		# Ожидание в 2 секунду (для работы других функций бота)
		await asyncio.sleep(2)

		# Получаем список статусов поиска пользователей
		searches_users = database.Searches().get(None, "*").fetchall()
		if searches_users is None or len(searches_users) < 2:
			continue

		# Перебираем всех пользователей, кто сейчас в поиске
		search_queue = []
		for user in searches_users:
			if bool(user[1]) is True:
				search_queue.append(user)
		

		# Если в поиске два и больше человек
		if len(search_queue) >= 2:
			# ищем собеседников
			user_first = random.choice(search_queue)
			user_second = user_first

			matching = False
			counter = 0
			while counter < 4:
				counter += 1
				
				user_second = random.choice(search_queue)
				if user_second == user_first:
					continue

				# Язык
				first_language = database.Users().get(user_first[0], "language").fetchone()
				second_language = database.Users().get(user_second[0], "language").fetchone()
				if user_first[4] != second_language[0] and user_first[4] != "all":
					continue
				if user_second[4] != first_language[0] and user_second[4] != "all":
					continue
				
				# Возраст
				first_age = database.Users().get(user_first[0], "age").fetchone()
				second_age = database.Users().get(user_second[0], "age").fetchone()
				if user_first[3] != second_age[0] and user_first[3] != "all":
					continue
				if user_second[3] != first_age[0] and user_second[3] != "all":
					continue

				# Пол
				first_gender = database.Users().get(user_first[0], "gender").fetchone()
				second_gender = database.Users().get(user_second[0], "gender").fetchone()
				if user_first[2] != second_gender[0] and user_first[2] != "all":
					continue
				if user_second[2] != first_gender[0] and user_second[2] != "all":
					continue

				# В поиске ли (повторная проверка перед соединением)
				search_status1 = database.Searches().get(user_first[0], "search").fetchone()
				search_status2 = database.Searches().get(user_second[0], "search").fetchone()
				if bool(search_status1[0]) is False or bool(search_status2[0]) is False:
					continue
				

				# Если дошли - значит критерии сходятся
				matching = True
				break
			

			# Если все критерии поиска совпадают и оба собеседника в поиске - соединяем
			if matching:
				# Убираем поиск пользователям
				database.Searches().post(user_first[0], "search", 0)
				database.Searches().post(user_second[0], "search", 0)

				# Создаём чат
				database.Chats().put(user_first[0], user_second[0])
				database.Chats().put(user_second[0], user_first[0])

				

				# Сообщение о соединение на языке пользователя (1 пользователь)
				user_language = await functions.Default().get_language(user_first[0])
				keyboard = await InlineButtons().stop_search(types.InlineKeyboardMarkup(),
					LOCALIZATION[user_language]['dialog_stop_button'])
				await functions.Default().send_message(LOCALIZATION[user_language]['searched'], user_first[0], None, keyboard)
				
				# Сообщение о соединение на языке пользователя (2 пользователь)
				user_language = await functions.Default().get_language(user_second[0])
				keyboard = await InlineButtons().stop_search(types.InlineKeyboardMarkup(),
					LOCALIZATION[user_language]['dialog_stop_button'])
				await functions.Default().send_message(LOCALIZATION[user_language]['searched'], user_second[0], None, keyboard)


async def main():
	# Стартуем бота
	asyncio.create_task(BOT.polling())
	print("Бот запущен!")
	# Стартуем поиск собеседников
	await asyncio.create_task(random_search_partners())


asyncio.run(main())