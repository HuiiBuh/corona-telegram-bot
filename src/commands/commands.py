from typing import Union

from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils.callback_data import CallbackData

from commands.status_update import send_country_update, send_district_update
from storage import CovidDatabase, UserDatabase

user_db = UserDatabase.create()
covid_db = CovidDatabase()
settings_callback = CallbackData("settings", "setting", "data")


async def test_command(message: types.Message):
    image = await covid_db.get_incidence_plot("11007")
    await message.bot.send_photo(message.chat.id, image)


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


async def settings(message: Union[types.Message, types.CallbackQuery]):
    keyboard_markup = types.InlineKeyboardMarkup()
    keyboard_markup.row(
        types.InlineKeyboardButton("Subscribe to District",
                                   callback_data=settings_callback.new(setting="show_states", data="None")),
    )
    keyboard_markup.row(
        types.InlineKeyboardButton("Unsubscribe from Districts",
                                   callback_data=settings_callback.new(setting="show_subscriptions", data="None")),
    )
    keyboard_markup.row(
        types.InlineKeyboardButton("Manage notifications",
                                   callback_data=settings_callback.new(setting="show_notification", data="None")),
    )
    keyboard_markup.row(
        types.InlineKeyboardButton("View on Github", url="https://github.com/HuiiBuh/corona-telegram-bot"),
    )
    keyboard_markup.row(
        types.InlineKeyboardButton("Close settings",
                                   callback_data=settings_callback.new(setting="close_settings", data="None")),
    )

    if isinstance(message, types.Message):
        await message.answer("Modify your settings:", reply_markup=keyboard_markup)
    elif isinstance(message, types.CallbackQuery):
        await message.answer()
        await message.message.edit_text("Modify your settings:", reply_markup=keyboard_markup)
