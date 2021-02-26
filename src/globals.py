import asyncio

from aiogram import Bot, Dispatcher

from commands import message_handlers
from settings import SETTINGS
from storage.database import Database

database = Database()

event_loop = asyncio.get_event_loop()
bot = Bot(token=SETTINGS.bot_secret, loop=event_loop)
dispatcher = Dispatcher(bot)

for handler in message_handlers:
    dispatcher.register_message_handler(**handler)
