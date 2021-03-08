from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from storage import UserDatabase, CovidDatabase

user_db = UserDatabase.create()
covid_db = CovidDatabase()
settings_callback = CallbackData("settings", "setting", "data")


async def show_states(query: CallbackQuery):
    buttons = InlineKeyboardMarkup()
    for state in await covid_db.get_sorted_state_list():
        buttons.row(
            InlineKeyboardButton(state.name,
                                 callback_data=settings_callback.new(setting=f"show_districts", data=state.name))
        )
    buttons.row(
        InlineKeyboardButton(
            "Back", callback_data=settings_callback.new(setting="settings", data="None"))
    )
    await query.answer()
    await query.message.edit_text("Select the state the district you want to get get information about is in.",
                                  reply_markup=buttons)


async def show_districts(query: CallbackQuery, callback_data: dict):
    buttons = InlineKeyboardMarkup()

    state_name = callback_data["data"]
    districts = await covid_db.get_district_by_state_name(state_name)

    for district in districts:
        buttons.row(
            InlineKeyboardButton(
                district.name, callback_data=settings_callback.new(setting="add_district", data=district.ags))
        )
    buttons.row(
        InlineKeyboardButton(
            "Back", callback_data=settings_callback.new(setting="show_states", data="None"))
    )
    await query.answer()
    await query.message.edit_text("Select the district you want to get updates from.", reply_markup=buttons)


async def add_district(query: CallbackQuery, callback_data: dict):
    district_id = int(callback_data["data"])

    user = user_db.get_user(query.from_user.id)
    user.districts = list({district_id, *user.districts})
    user_db.save()

    await query.answer("Successfully subscribed to district.")


async def remove_district(query: CallbackQuery, callback_data: dict):
    district_id = int(callback_data["data"])

    user = user_db.get_user(query.from_user.id)
    user.districts = list(filter(lambda i: i != district_id, user.districts))
    user_db.save()

    await query.answer()
    await show_subscriptions(query)


async def show_subscriptions(query: CallbackQuery):
    buttons = InlineKeyboardMarkup()

    user = user_db.get_user(query.from_user.id)
    district_list = await covid_db.get_ordered_district_by_id(user.districts)
    for district in district_list:
        buttons.row(
            InlineKeyboardButton(district.name,
                                 callback_data=settings_callback.new("remove_district", data=district.ags))
        )

    buttons.row(
        InlineKeyboardButton(
            "Back", callback_data=settings_callback.new(setting="settings", data="None"))
    )
    await query.answer()
    await query.message.edit_text("Click on any of these districts to unsubscribe from them", reply_markup=buttons)


async def close_settings(query: CallbackQuery):
    await query.message.delete()
    await query.answer()
