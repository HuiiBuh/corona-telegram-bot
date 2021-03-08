from aiogram.utils.callback_data import CallbackData

from commands.callbacks import subscribe_state, subscribe_district, subscribe_add_district
from commands.commands import start, country, settings, district, update
from helpers.message_handler import register_message_handler, register_callback_handler

message_handler_list = [
    register_message_handler(start, commands=["start", "help"]),
    register_message_handler(country, commands=["country"]),
    register_message_handler(district, commands=["district"]),
    register_message_handler(update, commands=["update"]),
    register_message_handler(settings, commands=["settings"])
]

settings_callback = CallbackData("settings", "setting", "data")
callback_handler_list = [
    register_callback_handler(subscribe_state, settings_callback.filter(setting=["subscribe_state"])),
    register_callback_handler(subscribe_district, settings_callback.filter(setting=["subscribe_district"])),
    register_callback_handler(subscribe_add_district, settings_callback.filter(setting=["add_district"])),
]
