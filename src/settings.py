from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    bot_secret: str = Field(env="BOT_SECRET")
    covid_api_url: str = Field(env="COVID_API", default="https://v2.rki.marlon-lueckert.de/")
    db_location: str = Field(env="DB_LOCATION", default="database/")
    production: bool = Field(env="PRODUCTION", default=False)


SETTINGS = Settings()
