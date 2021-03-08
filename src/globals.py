import asyncio

from aiogram import Bot, Dispatcher

from settings import SETTINGS
from storage import CovidDatabase, UserDatabase

event_loop = asyncio.get_event_loop()
bot = Bot(token=SETTINGS.bot_secret, loop=event_loop)
dispatcher = Dispatcher(bot)


async def initialize_database():
    covid_db = CovidDatabase()
    covid_db.initialize()
    user_db = UserDatabase.create()
    user_db.load()
