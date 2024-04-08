import datetime
from telebot.async_telebot import types

from config import BOT
from config import GLOBALDATA
from config import LOCALIZATION
from modules.keyboard import InlineButtons
import modules.database as database


class Default:
    #region -------------------- СООБЩЕНИЯ --------------------
    # Отправить сообщение пользователю
    async def send_message(self, text, chat_id, message_id = None, keyboard = None):
        if message_id == None:
            await BOT.send_message(chat_id, text, reply_markup = keyboard)
        else:
            await BOT.edit_message_text(text, chat_id, message_id, reply_markup = keyboard)

    # Общение с собеседником
    async def communication_partner(self, message, link = False):
        partner = database.Chats().get(message.chat.id, "partner_user_id").fetchone()
        if partner is None:
            user_language = await self.get_language(message.chat.id)
            keyboard = await InlineButtons().start_search(user_language, types.InlineKeyboardMarkup())
            keyboard = await InlineButtons().to_menu(user_language, keyboard)
            await self.send_message(LOCALIZATION[user_language]['send_message_partner_none'], message.chat.id, None, keyboard)
        else:
            if not link:
                await BOT.copy_message(partner[0], message.chat.id, message.message_id)
            else:
                text = LOCALIZATION[user_language]['username_none']
                if message.from_user.username is not None:
                    partner_text = f"🔗 Ссылка на собеседника: @{message.from_user.username}"
                    await self.send_message(partner_text, partner)
                    text = LOCALIZATION[user_language]['username_send']
                await self.send_message(text, message.chat.id)
    #endregion ----------------------------------------

    
    #region -------------------- ПОИСК --------------------
    # Поиск собеседника
    async def start_search_partner(self, message, message_id = None):
        # Проверка регистрации
        user_registered = await AllUsers().check_register(message.chat.id)
        if not user_registered:
            await AllUsers().register(message)
        else:
            user_language = await self.get_language(message.chat.id)
            text = LOCALIZATION[user_language]['search_stop_question']
            btn_txt = LOCALIZATION[user_language]['search_stop_button']

            searchStatus = database.Searches().get(message.chat.id, "search").fetchone()
            if searchStatus is not None and (bool)(searchStatus[0]) is False:
                database.Searches().post(message.chat.id, "search", 1)
                text = LOCALIZATION[user_language]['search_started']
            else:
                partner = database.Chats().get(message.chat.id, "partner_user_id").fetchone()
                if partner is not None and partner[0] is not None:
                    text = LOCALIZATION[user_language]['dialog_stop_question']
                    btn_txt = LOCALIZATION[user_language]['dialog_stop_button']

            keyboard = await InlineButtons().stop_search(types.InlineKeyboardMarkup(), btn_txt)
            await self.send_message(text, message.chat.id, message_id, keyboard)

    # Остановить диалог/поиск собеседника
    async def stop_search_partner(self, message, message_id = None):
        # Проверка регистрации
        user_registered = await AllUsers().check_register(message.chat.id)
        if not user_registered:
            await AllUsers().register(message)
        else:
            user_language = await self.get_language(message.chat.id)
            text = LOCALIZATION[user_language]['search_none']
            keyboard = await InlineButtons().start_search(user_language, types.InlineKeyboardMarkup())
            keyboard = await InlineButtons().to_menu(user_language, keyboard)
            
            searchStatus = database.Searches().get(message.chat.id, "search").fetchone()
            if searchStatus is not None and searchStatus[0] == 1:
                database.Searches().post(message.chat.id, "search", 0)
                text = LOCALIZATION[user_language]['search_stoped']
            else:
                partner = database.Chats().get(message.chat.id, "partner_user_id").fetchone()
                if partner is not None and partner[0] is not None:
                    database.Chats().delete(message.chat.id)
                    database.Chats().delete(partner[0])
                    await self.send_message(LOCALIZATION[user_language]['dialog_stoped_partner'], partner[0], None, keyboard)
                    text = LOCALIZATION[user_language]['dialog_stoped']

            await self.send_message(text, message.chat.id, message_id, keyboard)
    
    # Остановить диалог и начать поиск собеседника
    async def next_search_partner(self, message, message_id = None):
        # Проверка регистрации
        user_registered = await AllUsers().check_register(message.chat.id)
        if not user_registered:
            await AllUsers().register(message)
        else:
            user_language = await self.get_language(message.chat.id)
            
            keyboard = await InlineButtons().start_search(user_language, types.InlineKeyboardMarkup())
            keyboard = await InlineButtons().to_menu(user_language, keyboard)

            partner = database.Chats().get(message.chat.id, "partner_user_id").fetchone()
            if partner is not None and partner[0] is not None:
                database.Chats().delete(message.chat.id)
                database.Chats().delete(partner[0])
                await self.send_message(LOCALIZATION[user_language]['dialog_stoped_partner'], partner[0], None, keyboard)
                await self.send_message(LOCALIZATION[user_language]['dialog_stoped'], message.chat.id, message_id)
            await self.start_search_partner(message)
    #endregion ----------------------------------------


    #region -------------------- ЯЗЫК --------------------
    # Запрос языка
    async def get_language(self, chat_id, convert_to_code = True, search = False):
        language = None
        user_registered = await AllUsers().check_register(chat_id)
        if not user_registered:
            if len(GLOBALDATA) != 0 and GLOBALDATA[chat_id] is not None:
                language = GLOBALDATA[chat_id]['language']
        else:
            if search:
                language = database.Searches().get(chat_id, "language").fetchone()
            else:
                language = database.Users().get(chat_id, "language").fetchone()
            language = language[0]
            
        if convert_to_code is True:
            language = await self.language_to_code(language)
        return language
    
    # Перевести название языка в его кодовую часть
    async def language_to_code(self, language):
        code = "RU"
        if language == "language_english":
            code = "EN"
        return code
    
    # Перевести название языка в его название
    async def language_name(self, user_language, language):
        code = await self.language_to_code(language)
        if language == "all":
            language = LOCALIZATION[user_language]['any']
        else:
            language = LOCALIZATION[code]['language']
        return language
    #endregion ----------------------------------------






class AllUsers:
    #region -------------------- РЕГИСТРАЦИЯ --------------------
    # Проверка регистрации
    async def check_register(self, chat_id):
        user_registered = False
        result = database.Users().get(chat_id).fetchone()
        if result is not None and result[0] == chat_id:
            user_registered = True
        return user_registered

    # Регистрация
    async def register(self, message, message_id = None):
        GLOBALDATA[message.chat.id] = {"gender":"None", "age":"None", "language":"None"}
        keyboard = await InlineButtons().change_language(types.InlineKeyboardMarkup())
        text = f"{LOCALIZATION['RU']['not_register']}\n{LOCALIZATION['RU']['register_language']}\
            \n\n{LOCALIZATION['EN']['not_register']}\n{LOCALIZATION['EN']['register_language']}"
        await Default().send_message(text, message.chat.id, message_id, keyboard)
    #endregion ----------------------------------------


    #region -------------------- ФУНКЦИИ --------------------
    # Помощь
    async def help(self, message, message_id = None):
        user_language = await Default().get_language(message.chat.id)
        text = f"<b>{LOCALIZATION[user_language]['help_title']}</b>\
            \n/start - {LOCALIZATION[user_language]['help_start']}\
            \n/stop - {LOCALIZATION[user_language]['help_stop']}\
            \n/next - {LOCALIZATION[user_language]['help_next']}\
            \n/link - {LOCALIZATION[user_language]['help_link']}\
            \n/menu - {LOCALIZATION[user_language]['help_menu']}\
            \n/help - {LOCALIZATION[user_language]['help_help']}\
            \n/profile - {LOCALIZATION[user_language]['help_profile']}\
            \n/premium - {LOCALIZATION[user_language]['help_premium']}"
        
        # Клавиатура
        keyboard = await InlineButtons().to_menu(user_language, types.InlineKeyboardMarkup())
        await Default().send_message(text, message.chat.id, message_id, keyboard)

    # Меню
    async def menu(self, message, message_id = None):
        user_language = await Default().get_language(message.chat.id)

        # Клавиатура
        keyboard = await InlineButtons().start_search(user_language, types.InlineKeyboardMarkup())
        keyboard = await InlineButtons().menu(user_language, keyboard)
        
        text = f"<b>{LOCALIZATION[user_language]['menu']}</b>\n\n{LOCALIZATION[user_language]['select_action']}"
        await Default().send_message(text, message.chat.id, message_id, keyboard)

    # Профиль
    async def profile(self, message, message_id = None):
        user_language = await Default().get_language(message.chat.id)

        # Получить язык в БД пользователя
        language = await Default().get_language(message.chat.id, False)
        # Получить название языка
        language = await Default().language_name(user_language, language)
        gender = await self.db_request_gender(message.chat.id)
        age = await self.db_request_age(message.chat.id)

        text = f"<b>{LOCALIZATION[user_language]['profile']}</b>\n\
            \n🆔 <code>{message.chat.id}</code>\
            \n🌐 {LOCALIZATION[user_language]['language_text']}: <i>{language}</i>\
            \n🚻 {LOCALIZATION[user_language]['gender']}: <i>{gender}</i>\
            \n🔞 {LOCALIZATION[user_language]['age']}: <i>{age}</i>"

        keyboard = await InlineButtons().edit_data(user_language, types.InlineKeyboardMarkup())
        keyboard = await InlineButtons().to_menu(user_language, keyboard)
        await Default().send_message(text, message.chat.id, message_id, keyboard)
    
    # Премиум
    async def premium(self, message, message_id = None):
        user_language = await Default().get_language(message.chat.id)

        type, date, end_date = await self.db_request_premium(message.chat.id)
        text = f"{LOCALIZATION[user_language]['premium_none']}\n{LOCALIZATION[user_language]['premium_get']}"
        if type is not None:
            text = f"⚜️ <b>{LOCALIZATION[user_language]['premium']}</b> ⚜️\n\
                \{LOCALIZATION[user_language]['premium_type']}: <i>{LOCALIZATION[user_language][type]}</i>\
                \n{LOCALIZATION[user_language]['premium_date']}: <i>{date}</i>\
                \{LOCALIZATION[user_language]['premium_date_end']}: <i>{end_date}</i>"
        keyboard = await InlineButtons().to_menu(user_language, types.InlineKeyboardMarkup())
        await Default().send_message(text, message.chat.id, message_id, keyboard)

    # Настройки поиска
    async def search_settings(self, message, message_id = None):
        user_language = await Default().get_language(message.chat.id)

        # Получить язык в БД поиска
        language = await Default().get_language(message.chat.id, False, True)
        # Получить название языка поиска
        language = await Default().language_name(user_language, language)
        gender = await self.db_request_gender(message.chat.id, True)
        age = await self.db_request_age(message.chat.id, True)

        text = f"<b>{LOCALIZATION[user_language]['search_settings']}</b>\n\
            \n🌐 {LOCALIZATION[user_language]['language_text']}: <i>{language}</i>\
            \n🚻 {LOCALIZATION[user_language]['gender']}: <i>{gender}</i>\
            \n🔞 {LOCALIZATION[user_language]['age']}: <i>{age}</i>"
        
        keyboard = await InlineButtons().edit_data(user_language, types.InlineKeyboardMarkup(), True)
        keyboard = await InlineButtons().to_menu(user_language, keyboard)
        await Default().send_message(text, message.chat.id, message_id, keyboard)



    # Смена языка
    async def change_language(self, message, message_id = None, search_settings = False):
        user_language = await Default().get_language(message.chat.id)

        text = LOCALIZATION[user_language]['language_select']
        keyboard = await InlineButtons().change_language(types.InlineKeyboardMarkup(), search_settings, user_language)
        if search_settings:
            keyboard = await InlineButtons().to_search_settings(user_language, keyboard, LOCALIZATION[user_language]['back_button'])
        else:
            keyboard = await InlineButtons().to_profile(user_language, keyboard, LOCALIZATION[user_language]['back_button'])
        await Default().send_message(text, message.chat.id, message_id, keyboard)

    # Смена пола
    async def change_gender(self, message, message_id = None, search_settings = False):
        user_language = await Default().get_language(message.chat.id)

        text = LOCALIZATION[user_language]['gender_select']
        keyboard = await InlineButtons().change_gender(user_language, types.InlineKeyboardMarkup(), search_settings)
        if search_settings:
            keyboard = await InlineButtons().to_search_settings(user_language, keyboard, LOCALIZATION[user_language]['back_button'])
        else:
            keyboard = await InlineButtons().to_profile(user_language, keyboard, LOCALIZATION[user_language]['back_button'])
        await Default().send_message(text, message.chat.id, message_id, keyboard)

    # Смена возраста
    async def change_age(self, message, message_id = None, search_settings = False):
        user_language = await Default().get_language(message.chat.id)

        text = LOCALIZATION[user_language]['age_select']
        keyboard = await InlineButtons().change_age(user_language, types.InlineKeyboardMarkup(), search_settings)
        if search_settings:
            keyboard = await InlineButtons().to_search_settings(user_language, keyboard, LOCALIZATION[user_language]['back_button'])
        else:
            keyboard = await InlineButtons().to_profile(user_language, keyboard, LOCALIZATION[user_language]['back_button'])
        await Default().send_message(text, message.chat.id, message_id, keyboard)
    #endregion ----------------------------------------
    
    
    #region -------------------- ДАННЫЕ ПОЛЬЗОВАТЕЛЯ --------------------
    # Получить пол
    async def db_request_gender(self, user_id, search = False):
        user_language = await Default().get_language(user_id)
        result = ""
        if search:
            result = database.Searches().get(user_id, "gender").fetchone()
        else:
            result = database.Users().get(user_id, "gender").fetchone()
        if result is not None:
            if result[0] == "all":
                return LOCALIZATION[user_language]["any"]
            else:
                return LOCALIZATION[user_language][result[0]]

    # Получить возраст
    async def db_request_age(self, user_id, search = False):
        user_language = await Default().get_language(user_id)
        if search:
            result = database.Searches().get(user_id, "age").fetchone()
        else:
            result = database.Users().get(user_id, "age").fetchone()
        if result is not None:
            if result[0] == "all":
                return LOCALIZATION[user_language]["any"]
            else:
                return LOCALIZATION[user_language][result[0]]
    
    # Получить премиум
    async def db_request_premium(self, user_id):
        result = database.Premiums().get(user_id, "*").fetchone()
        if result is not None:
            user_language = await Default().get_language(user_id)

            date = datetime.strptime(result[2], '%Y-%m-%d').date()
            end_date = LOCALIZATION[user_language]['forever']
            if result[3] != 0:
                end_date = date + datetime.timedelta(days=result[3])
            
            return result[1], date, end_date
        else:
            return None, None, None
    #endregion ----------------------------------------