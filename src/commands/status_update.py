from aiogram.types import ParseMode

from globals import bot
from models.Districts import Districts
from storage.covid_database import CovidDatabase
from storage.user_database import UserDatabase, User

user_db = UserDatabase.create()
covid_db = CovidDatabase()


async def send_status_update():
    user_dict = user_db.get_all_users()

    for user in user_dict.values():
        await send_country_update(user)
        await send_district_update(user)


async def send_district_update(user: User, scip_district_check=True):
    if len(user.districts) == 0 and not scip_district_check:
        return await bot.send_message(user.id, "*You did not subscribe to any districts.*\n"
                                               "Go into /settings to subscribe to districts you want information from "
                                               "or /start to see which commands are available.", ParseMode.MARKDOWN)

    district_list = await covid_db.get_ordered_district_by_id(user.districts)
    for district in district_list:
        await send_district(user, district)


async def send_district(user: User, district: Districts):
    message = f"""
    *{district.name}:*
    - Cases per Hundred Thousand: _{round(district.cases_per100_k)}_
    - Week Incidence: _{round(district.week_incidence)}_
    """.replace("-", "\\-")
    await bot.send_message(user.id, message, ParseMode.MARKDOWN_V2)


async def send_country_update(user: User) -> None:
    prepare_message = await bot.send_message(user.id, "Preparing image...")

    germany = await covid_db.germany
    covid_map = await covid_db.map
    message = f"""
    *Germany:*
    - R-value: _{round(germany.r.value)}_
    - Cases per Hundred Thousand: _{round(germany.cases_per100_k)}_
    - Week Incidence: _{round(germany.week_incidence)}_
    """.replace("-", "\\-")

    await bot.send_photo(user.id, covid_map, message, ParseMode.MARKDOWN_V2)
    await bot.delete_message(user.id, prepare_message.message_id)
