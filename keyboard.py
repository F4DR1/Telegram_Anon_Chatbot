from telebot.async_telebot import types

class Buttons:
    # Изменить пол
    async def change_gender(self, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = "🚹 Мужской 🚹", callback_data = "gender_male"))
        keyboard.add(types.InlineKeyboardButton(text = "🚺 Женский 🚺", callback_data = "gender_female"))
        keyboard.add(types.InlineKeyboardButton(text = "🚺 Другой 🚺", callback_data = "gender_other"))
        return keyboard

    # Изменить возраст
    async def change_age(self, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = "До 14 лет", callback_data = "age_child"))
        keyboard.add(types.InlineKeyboardButton(text = "14-17 лет", callback_data = "age_teen"))
        keyboard.add(types.InlineKeyboardButton(text = "18 лет и старше", callback_data = "age_adult"))
        return keyboard
    
    

    # В меню
    async def to_menu(self, keyboard):
        keyboard.add(types.InlineKeyboardButton(text = "⬅️ Вернуться в меню", callback_data = "to_menu"))
        return keyboard
    
    # Начать поиск
    async def start_search(self, keyboard, btn_txt):
        keyboard.add(types.InlineKeyboardButton(text = "🔍 Начать поиск", callback_data = "start_search_partner"))
        return keyboard
    
    # Остановить поиск
    async def stop_search(self, keyboard, btn_txt):
        keyboard.add(types.InlineKeyboardButton(text = btn_txt, callback_data = "stop_search_partner"))
        return keyboard