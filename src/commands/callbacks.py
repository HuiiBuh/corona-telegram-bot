from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from commands.helpers import get_states_keyboard, get_district_keyboard
from commands.status_update import send_district
from storage import UserDatabase, CovidDatabase

user_db = UserDatabase.create()
covid_db = CovidDatabase()
settings_callback = CallbackData("settings", "setting", "data")


async def show_states(query: CallbackQuery):
    buttons = await get_states_keyboard("show_districts", "settings")
    await query.answer()
    await query.message.edit_text("Select the state the district belongs to",
                                  reply_markup=buttons)


async def show_districts(query: CallbackQuery, callback_data: dict):
    state_name = callback_data["data"]
    buttons = await get_district_keyboard("add_district", state_name, "show_states")
    await query.answer()
    await query.message.edit_text("Select the district you want to get updates from.", reply_markup=buttons)


async def select_district(query: CallbackQuery, callback_data: dict):
    state_name = callback_data["data"]
    buttons = await get_district_keyboard("show_district_graph", state_name, "show_one_district")
    await query.answer()
    await query.message.edit_text("Select the state the district belongs to", reply_markup=buttons)


async def show_district_graph(query: CallbackQuery, callback_data: dict):
    await query.answer()
    district = await covid_db.get_district_by_id(callback_data["data"])
    user = user_db.get_user(query.from_user.id)
    await send_district(user, district)


async def add_district(query: CallbackQuery, callback_data: dict):
    district_id = callback_data["data"]

    user = user_db.get_user(query.from_user.id)
    user.districts = list({district_id, *user.districts})
    user_db.save()

    await query.answer("Successfully subscribed to district.")


async def remove_district(query: CallbackQuery, callback_data: dict):
    district_id = callback_data["data"]

    user = user_db.get_user(query.from_user.id)
    user.districts = list(filter(lambda i: i != district_id, user.districts))
    user_db.save()

    await query.answer()
    await show_subscriptions(query)


async def show_subscriptions(query: CallbackQuery):
    buttons = InlineKeyboardMarkup()

    user = user_db.get_user(query.from_user.id)
    district_list = await covid_db.get_ordered_district_by_ids(user.districts)
    for district in district_list:
        buttons.row(
            InlineKeyboardButton(district.county,
                                 callback_data=settings_callback.new("remove_district", data=district.ags))
        )

    buttons.row(
        InlineKeyboardButton(
            "Back", callback_data=settings_callback.new(setting="settings", data="None"))
    )
    await query.answer()
    await query.message.edit_text("Click on any of these districts to unsubscribe from them", reply_markup=buttons)


async def show_notification(query: CallbackQuery):
    user = user_db.get_user(query.from_user.id)
    buttons = InlineKeyboardMarkup()
    buttons.row(
        InlineKeyboardButton("Disable notification" if user.notification_active else "Enable notification",
                             callback_data=settings_callback.new("toggle_notification", data="None"))
    )
    buttons.row(
        InlineKeyboardButton(
            "Back", callback_data=settings_callback.new(setting="settings", data="None"))
    )
    await query.answer()
    await query.message.edit_text(
        "If you want daily notifications about the status enable this feature. Otherwise disable it.",
        reply_markup=buttons)


async def toggle_notification(query: CallbackQuery):
    user = user_db.get_user(query.from_user.id)
    user.notification_active = not user.notification_active
    user_db.save()

    await query.answer()
    await show_notification(query)


async def close(query: CallbackQuery):
    await query.message.delete()
    await query.answer()
