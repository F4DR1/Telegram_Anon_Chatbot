# -*- coding: utf-8 -*-

from telebot.async_telebot import AsyncTeleBot
import asyncio

from config import TOKEN

bot = AsyncTeleBot(TOKEN, parse_mode="MarkdownV2")


from atexit import register
from cgitb import text
from tabnanny import check
from unicodedata import name
from xml.dom.domreg import registered
from random import randint




@bot.message_handler(commands=["start"])
async def send_welcome(message):

	text = message.from_user.full_name + ", добро пожаловать в наш анонимный чат\!"

	await bot.send_message(message.from_user.id, text)




asyncio.run(bot.polling())