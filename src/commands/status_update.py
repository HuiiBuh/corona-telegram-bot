import asyncio
from io import BytesIO

from aiogram.types import ParseMode, MediaGroup, InputMediaPhoto

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

    district_list = await covid_db.get_ordered_district_by_ids(user.districts)
    for district in district_list:
        await send_district(user, district)


async def send_district(user: User, district: Districts):
    message = f"""
    *{district.county}:*
    - R-value: _{await covid_db.calculate_r(district.ags)}_
    - Cases per Hundred Thousand: _{round(district.cases_per100_k)}_
    - Week Incidence: _{round(district.week_incidence)}_
    """.replace("-", "\\-").replace(".", "\\.")
    image = await covid_db.get_incidence_plot(district.ags)
    await bot.send_photo(user.id, image, message, ParseMode.MARKDOWN_V2)


async def send_country_update(user: User) -> None:
    prepare_message = await bot.send_message(user.id, "Preparing image...")

    try:
        covid_map = await covid_db.map()
    except asyncio.exceptions.TimeoutError:
        covid_map = None

    germany = await covid_db.germany()
    message = f"""
    *Germany:*
    - R-value: _{round(germany.r.value, 2)}_
    - Cases per Hundred Thousand: _{round(germany.cases_per100_k)}_
    - Week Incidence: _{round(germany.week_incidence)}_
    """.replace("-", "\\-").replace(".", "\\.")

    media = MediaGroup()

    incidence_graph = await covid_db.get_incidence_plot()
    media.attach(InputMediaPhoto(BytesIO(incidence_graph), message, ParseMode.MARKDOWN_V2))

    vaccinations_graph = await covid_db.get_vaccination_plot()
    media.attach(InputMediaPhoto(BytesIO(vaccinations_graph)))

    if covid_map:
        media.attach_photo(InputMediaPhoto(BytesIO(covid_map)))
        await prepare_message.delete()
    else:
        await prepare_message.edit_text("Could not collect the image")

    await bot.send_media_group(user.id, media=media)
