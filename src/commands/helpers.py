from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from storage import CovidDatabase

covid_db = CovidDatabase()
settings_callback = CallbackData("settings", "setting", "data")


async def get_states_keyboard(callback: str, back_button: str, button_text: str = "Back") -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    for state in await covid_db.get_sorted_state_list():
        buttons.row(
            InlineKeyboardButton(state.name,
                                 callback_data=settings_callback.new(setting=callback, data=state.name))
        )
    buttons.row(
        InlineKeyboardButton(button_text, callback_data=settings_callback.new(setting=back_button, data="None"))
    )
    return buttons


async def get_district_keyboard(callback: str, state_name: str, back_button: str) -> InlineKeyboardMarkup:
    buttons = InlineKeyboardMarkup()
    districts = await covid_db.get_district_by_state_name(state_name)

    for district in districts:
        buttons.row(
            InlineKeyboardButton(
                district.county, callback_data=settings_callback.new(setting=callback, data=district.ags))
        )
    buttons.row(
        InlineKeyboardButton(
            "Back", callback_data=settings_callback.new(setting=back_button, data="None"))
    )
    return buttons
