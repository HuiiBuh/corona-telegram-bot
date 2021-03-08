from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils.callback_data import CallbackData

from commands.status_update import send_country_update, send_district_update
from storage import CovidDatabase, UserDatabase

user_db = UserDatabase.create()
covid_db = CovidDatabase()
settings_callback = CallbackData("settings", "setting", "data")


async def start(message: types.Message):
    user_db.create_if_not_exist(message.from_user.id)
    response = """
    *Commands:*
    - /country Get status
    - /district Get status
    - /update Get country and district
    - /settings Subscribe to districts
    """.replace("-", "\\-")
    await message.reply(response, ParseMode.MARKDOWN_V2)


async def country(message: types.Message):
    user = user_db.get_user(message.from_user.id)
    await send_country_update(user)


async def district(message: types.Message):
    user = user_db.get_user(message.from_user.id)
    await send_district_update(user, scip_district_check=False)


async def update(message: types.Message):
    user = user_db.get_user(message.from_user.id)
    await send_country_update(user)
    await send_district_update(user)


async def settings(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.row(
        types.InlineKeyboardButton("Subscribe to District",
                                   callback_data=settings_callback.new(setting="subscribe_state", data="None")),
    )
    keyboard_markup.row(
        types.InlineKeyboardButton("Unsubscribe from Districts",
                                   callback_data=settings_callback.new(setting="unsubscribe_state", data="None")),
    )
    keyboard_markup.row(
        types.InlineKeyboardButton("Manage notifications",
                                   callback_data=settings_callback.new(setting="notification", data="None")),
    )

    await message.answer("Modify your settings:", reply_markup=keyboard_markup)
