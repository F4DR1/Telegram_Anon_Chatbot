from telebot.async_telebot import types
from config import LOCALIZATION


class InlineButtons:
    # Изменить пол
    async def change_gender(self, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["gender_male"], callback_data = "gender_male"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["gender_female"], callback_data = "gender_female"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["gender_other"], callback_data = "gender_other"))
        return keyboard

    # Изменить возраст
    async def change_age(self, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["age_child"], callback_data = "age_child"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["age_teen"], callback_data = "age_teen"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["age_adult"], callback_data = "age_adult"))
        return keyboard
    
    # Редактировать данные
    async def edit_data(self, keyboard):
        keyboard.add(
            types.InlineKeyboardButton(text=LOCALIZATION["RU"]["edit_gender_button"], callback_data="edit_gender"),
            types.InlineKeyboardButton(text=LOCALIZATION["RU"]["edit_age_button"], callback_data="edit_age")
        )
        return keyboard
    
    
    # Меню
    async def menu(self, keyboard):
        keyboard = await self.to_profile(keyboard, LOCALIZATION["RU"]["profile"])
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["help"], callback_data = "help"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["premium"], callback_data = "premium"))
        return keyboard

    # В меню
    async def to_profile(self, keyboard, text = LOCALIZATION["RU"]["default_to_profile_button"]):
        keyboard.add(types.InlineKeyboardButton(text, callback_data = "profile"))
        return keyboard
    
    # В профиль
    async def to_menu(self, keyboard, text = LOCALIZATION["RU"]["default_to_menu_button"]):
        keyboard.add(types.InlineKeyboardButton(text, callback_data = "menu"))
        return keyboard
    
    
    # Начать поиск
    async def start_search(self, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["search_start_button"], callback_data = "search_start_partner"))
        return keyboard
    
    # Остановить поиск
    async def stop_search(self, keyboard, btn_txt):
        keyboard.add(types.InlineKeyboardButton(text = btn_txt, callback_data = "search_stop_partner"))
        return keyboard