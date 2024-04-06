import json
import os
from telebot.async_telebot import AsyncTeleBot


with open('data\\localization.json', 'r', encoding='utf-8') as file:
    LOCALIZATION = json.load(file)

with open('data\\bot_data.json', 'r', encoding='utf-8') as file:
    DATA = json.load(file)

BOT = AsyncTeleBot(DATA["token"], parse_mode="HTML", protect_content=True)
DATABASE = os.path.dirname(os.path.abspath(__file__)) + "\\" + DATA["database"]
CHANNEL = DATA["channel"]

GLOBALDATA = {}