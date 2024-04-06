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
        # Проверка на регистрацию
        user_registered = await AllUsers().check_register(message.chat.id)
        if not user_registered:
            await AllUsers().register(message)
        else:
            partner = database.Chats().get(message.chat.id, "partner_user_id").fetchone()
            if partner is None:
                keyboard = await InlineButtons().start_search(types.InlineKeyboardMarkup())
                keyboard = await InlineButtons().to_menu(keyboard)
                await self.send_message(LOCALIZATION['RU']['send_message_partner_none'], message.chat.id, None, keyboard)
            else:
                if not link:
                    await BOT.copy_message(partner[0], message.chat.id, message.message_id)
                else:
                    text = LOCALIZATION['RU']['username_none']
                    if message.from_user.username is not None:
                        partner_text = f"🔗 Ссылка на собеседника: @{message.from_user.username}"
                        await self.send_message(partner_text, partner)
                        text = LOCALIZATION['RU']['username_send']
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
            text = LOCALIZATION['RU']['search_stop_question']
            btn_txt = LOCALIZATION['RU']['search_stop_button']

            searchStatus = database.Searches().get(message.chat.id, "search").fetchone()
            if searchStatus is not None and (bool)(searchStatus[0]) is False:
                database.Searches().post(message.chat.id, "search", 1)
                text = LOCALIZATION['RU']['search_started']
            else:
                partner = database.Chats().get(message.chat.id, "partner_user_id").fetchone()
                if partner is not None and partner[0] is not None:
                    text = LOCALIZATION['RU']['dialog_stop_question']
                    btn_txt = LOCALIZATION['RU']['dialog_stop_button']

            keyboard = await InlineButtons().stop_search(types.InlineKeyboardMarkup(), btn_txt)
            await self.send_message(text, message.chat.id, message_id, keyboard)

    # Остановить диалог/поиск собеседника
    async def stop_search_partner(self, message, message_id = None):
        # Проверка регистрации
        user_registered = await AllUsers().check_register(message.chat.id)
        if not user_registered:
            await AllUsers().register(message)
        else:
            text = LOCALIZATION['RU']['search_none']
            keyboard = await InlineButtons().start_search(types.InlineKeyboardMarkup())
            keyboard = await InlineButtons().to_menu(keyboard)
            
            searchStatus = database.Searches().get(message.chat.id, "search").fetchone()
            if searchStatus is not None and searchStatus[0] == 1:
                database.Searches().post(message.chat.id, "search", 0)
                text = LOCALIZATION['RU']['search_stoped']
            else:
                partner = database.Chats().get(message.chat.id, "partner_user_id").fetchone()
                if partner is not None and partner[0] is not None:
                    database.Chats().delete(message.chat.id)
                    database.Chats().delete(partner[0])
                    await self.send_message(LOCALIZATION['RU']['dialog_stoped_partner'], partner[0], None, keyboard)
                    text = LOCALIZATION['RU']['dialog_stoped']

            await self.send_message(text, message.chat.id, message_id, keyboard)
    
    # Остановить диалог и начать поиск собеседника
    async def next_search_partner(self, message, message_id = None):
        # Проверка регистрации
        user_registered = await AllUsers().check_register(message.chat.id)
        if not user_registered:
            await AllUsers().register(message)
        else:
            keyboard = await InlineButtons().start_search(types.InlineKeyboardMarkup())
            keyboard = await InlineButtons().to_menu(keyboard)

            partner = database.Chats().get(message.chat.id, "partner_user_id").fetchone()
            if partner is not None and partner[0] is not None:
                database.Chats().delete(message.chat.id)
                database.Chats().delete(partner[0])
                await self.send_message(LOCALIZATION['RU']['dialog_stoped_partner'], partner[0], None, keyboard)
                await self.send_message(LOCALIZATION['RU']['dialog_stoped'], message.chat.id, message_id)
            await self.start_search_partner(message)
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
        GLOBALDATA[message.chat.id] = {"gender":"None", "age":"None"}
        keyboard = await InlineButtons().change_gender(types.InlineKeyboardMarkup())
        await Default().send_message(LOCALIZATION['RU']['not_register'], message.chat.id, message_id, keyboard)
    #endregion ----------------------------------------
    

    #region -------------------- ФУНКЦИИ --------------------
    # Помощь
    async def help(self, message, message_id = None):
        text = f"<b>{LOCALIZATION['RU']['help_title']}</b>\
            \n/start - {LOCALIZATION['RU']['help_start']}\
            \n/stop - {LOCALIZATION['RU']['help_stop']}\
            \n/next - {LOCALIZATION['RU']['help_next']}\
            \n/link - {LOCALIZATION['RU']['help_link']}\
            \n/menu - {LOCALIZATION['RU']['help_menu']}\
            \n/help - {LOCALIZATION['RU']['help_help']}\
            \n/profile - {LOCALIZATION['RU']['help_profile']}\
            \n/premium - {LOCALIZATION['RU']['help_premium']}"
        
        # Клавиатура
        keyboard = await InlineButtons().to_menu(types.InlineKeyboardMarkup())
        await Default().send_message(text, message.chat.id, message_id, keyboard)

    # Меню
    async def menu(self, message, message_id = None):
        # Клавиатура
        keyboard = await InlineButtons().start_search(types.InlineKeyboardMarkup())
        keyboard = await InlineButtons().menu(keyboard)
        
        text = f"<b>{LOCALIZATION['RU']['menu']}</b>\n\n{LOCALIZATION['RU']['select_action']}"
        await Default().send_message(text, message.chat.id, message_id, keyboard)

    # Профиль
    async def profile(self, message, message_id = None):
        gender = await self.db_request_gender(message.chat.id)
        age = await self.db_request_age(message.chat.id)

        text = f"<b>{LOCALIZATION['RU']['profile']}</b>\n\
            \n🆔 ID: <code>{message.chat.id}</code>\
            \n🚻 {LOCALIZATION['RU']['gender']}: <i>{gender}</i>\
            \n🔞 {LOCALIZATION['RU']['age']}: <i>{age}</i>"

        # Клавиатура
        keyboard = await InlineButtons().edit_data(types.InlineKeyboardMarkup())
        keyboard = await InlineButtons().to_menu(keyboard)
        await Default().send_message(text, message.chat.id, message_id, keyboard)
    
    # Премиум
    async def premium(self, message, message_id = None):
        type, date, end_date = await self.db_request_premium(message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        text = f"{LOCALIZATION['RU']['premium_none']}\n{LOCALIZATION['RU']['premium_get']}"
        if type is not None:
            text = f"⚜️ <b>{LOCALIZATION['RU']['premium']}</b> ⚜️\n\
                \{LOCALIZATION['RU']['premium_type']}: <i>{LOCALIZATION['RU'][type]}</i>\
                \n{LOCALIZATION['RU']['premium_date']}: <i>{date}</i>\
                \{LOCALIZATION['RU']['premium_date_end']}: <i>{end_date}</i>"
        keyboard = await InlineButtons().to_menu(keyboard)
        await Default().send_message(text, message.chat.id, message_id, keyboard)


    # Смена пола
    async def change_gender(self, message, message_id = None):
        text = LOCALIZATION['RU']['gender_select']
        keyboard = await InlineButtons().change_gender(types.InlineKeyboardMarkup())
        keyboard = await InlineButtons().to_profile(keyboard, LOCALIZATION['RU']['back_button'])
        await Default().send_message(text, message.chat.id, message_id, keyboard)

    # Смена возраста
    async def change_age(self, message, message_id = None):
        text = LOCALIZATION['RU']['age_select']
        keyboard = await InlineButtons().change_age(types.InlineKeyboardMarkup())
        keyboard = await InlineButtons().to_profile(keyboard, LOCALIZATION['RU']['back_button'])
        await Default().send_message(text, message.chat.id, message_id, keyboard)
    #endregion ----------------------------------------
    
    
    #region -------------------- ДАННЫЕ ПОЛЬЗОВАТЕЛЯ --------------------
    # Получить пол
    async def db_request_gender(self, user_id):
        # Делаем запрос данных
        result = database.Users().get(user_id, "gender").fetchone()
        if result is not None:
            return LOCALIZATION['RU'][result[0]]

    # Получить возраст
    async def db_request_age(self, user_id):
        result = database.Users().get(user_id, "age").fetchone()
        if result is not None:
            return LOCALIZATION['RU'][result[0]]
    
    # Получить премиум
    async def db_request_premium(self, user_id):
        result = database.Premiums().get(user_id, "*").fetchone()
        if result is not None:
            date = datetime.strptime(result[2], '%Y-%m-%d').date()
            end_date = "Навсегда"
            if result[3] != 0:
                end_date = date + datetime.timedelta(days=result[3])
            
            return result[1], date, end_date
        else:
            return None, None, None
    #endregion ----------------------------------------