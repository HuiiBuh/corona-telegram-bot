from aiogram import types
from aiogram.utils.callback_data import CallbackData

from storage import UserDatabase, CovidDatabase

user_db = UserDatabase.create()
covid_db = CovidDatabase()

settings_callback = CallbackData("settings", "setting", "data")


async def subscribe_state(query: types.CallbackQuery):
    keyboard_markup = types.InlineKeyboardMarkup()
    for state in await covid_db.get_sorted_state_list():
        keyboard_markup.row(
            types.InlineKeyboardButton(state.name,
                                       callback_data=settings_callback.new(setting=f"subscribe_district",
                                                                           data=state.name))
        )
    await query.message.edit_text("Select a state", reply_markup=keyboard_markup)


async def subscribe_district(query: types.CallbackQuery, callback_data: dict):
    keyboard_markup = types.InlineKeyboardMarkup()

    state_name = callback_data["data"]
    districts = await covid_db.get_district_by_state_name(state_name)

    for district in districts:
        keyboard_markup.row(
            types.InlineKeyboardButton(district.name,
                                       callback_data=settings_callback.new(setting="add_district",
                                                                           data=district.ags))
        )
    await query.message.edit_text("Select a district", reply_markup=keyboard_markup)


async def subscribe_add_district(query: types.CallbackQuery, callback_data: dict):
    district_id = int(callback_data["data"])

    user = user_db.get_user(query.from_user.id)
    user.districts = list({district_id, *user.districts})
    user_db.save()

    await query.answer("Successfully subscribed to district")
