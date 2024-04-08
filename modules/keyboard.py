from telebot.async_telebot import types
from config import LOCALIZATION


class InlineButtons:
    # Изменить пол
    async def change_language(self, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["RU"]["language"], callback_data = "language_russia"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION["EN"]["language"], callback_data = "language_english"))
        return keyboard

    # Изменить пол
    async def change_gender(self, language, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION[language]["gender_male"], callback_data = "gender_male"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION[language]["gender_female"], callback_data = "gender_female"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION[language]["gender_other"], callback_data = "gender_other"))
        return keyboard

    # Изменить возраст
    async def change_age(self, language, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION[language]["age_child"], callback_data = "age_child"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION[language]["age_teen"], callback_data = "age_teen"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION[language]["age_adult"], callback_data = "age_adult"))
        return keyboard
    
    # Редактировать данные
    async def edit_data(self, language, keyboard):
        keyboard.row(
            types.InlineKeyboardButton(text=LOCALIZATION[language]["edit_gender_button"], callback_data="edit_gender"),
            types.InlineKeyboardButton(text=LOCALIZATION[language]["edit_age_button"], callback_data="edit_age")
        )
        return keyboard
    
    
    # Меню
    async def menu(self, language, keyboard):
        keyboard = await self.to_profile(language, keyboard, LOCALIZATION[language]["profile"])
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION[language]["premium"], callback_data = "premium"))
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION[language]["help"], callback_data = "help"))
        return keyboard

    # В меню
    async def to_profile(self, language, keyboard, text = None):
        default_text = LOCALIZATION[language]["default_to_profile_button"]
        if text is None:
            text = default_text
        keyboard.add(types.InlineKeyboardButton(text, callback_data = "profile"))
        return keyboard
    
    # В профиль
    async def to_menu(self, language, keyboard, text = None):
        default_text = LOCALIZATION[language]["default_to_menu_button"]
        if text is None:
            text = default_text
        keyboard.add(types.InlineKeyboardButton(text, callback_data = "menu"))
        return keyboard
    
    
    # Начать поиск
    async def start_search(self, language, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = LOCALIZATION[language]["search_start_button"], callback_data = "search_start_partner"))
        return keyboard
    
    # Остановить поиск
    async def stop_search(self, keyboard, btn_txt):
        keyboard.add(types.InlineKeyboardButton(text = btn_txt, callback_data = "search_stop_partner"))
        return keyboard





class ReplyButtons:
    # Меню
    async def menu(self, language, keyboard):
        keyboard.add(types.KeyboardButton(text = LOCALIZATION[language]["search_start_button"]))
        keyboard.add(types.KeyboardButton(text = LOCALIZATION[language]["menu"]))
        keyboard.add(types.KeyboardButton(text = LOCALIZATION[language]["profile"]))
        keyboard.row(types.KeyboardButton(text = LOCALIZATION[language]["premium"]),
                     types.KeyboardButton(text = LOCALIZATION[language]["help"]))
        return keyboard