from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    bot_secret: str = Field(env="BOT_SECRET")
    covid_api_url: str = Field(env="COVID_API", default="https://covid-server.unraid.hades/")
    db_location: str = Field(env="DB_LOCATION", default="database/")
    production: bool = Field(env="PRODUCTION", default=False)


SETTINGS = Settings()
