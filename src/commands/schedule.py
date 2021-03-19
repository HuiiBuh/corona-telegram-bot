from commands.status_update import send_country_update, send_district_update
from storage import CovidDatabase, UserDatabase

user_db = UserDatabase.create()
covid_db = CovidDatabase()


async def send_status_update():
    user_dict = user_db.get_all_users()

    for user in user_dict.values():
        if user.notification_active:
            await send_country_update(user)
            await send_district_update(user)
