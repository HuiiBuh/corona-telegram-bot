from aiogram.utils.callback_data import CallbackData

from commands.callbacks import show_states, show_districts, add_district, show_subscriptions, remove_district, \
    close_settings
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
    register_callback_handler(show_states, settings_callback.filter(setting=["show_states"])),
    register_callback_handler(show_districts, settings_callback.filter(setting=["show_districts"])),
    register_callback_handler(add_district, settings_callback.filter(setting=["add_district"])),
    register_callback_handler(remove_district, settings_callback.filter(setting=["remove_district"])),
    register_callback_handler(show_subscriptions, settings_callback.filter(setting=["show_subscriptions"])),
    register_callback_handler(settings, settings_callback.filter(setting=["settings"])),
    register_callback_handler(close_settings, settings_callback.filter(setting=["close_settings"])),
]
