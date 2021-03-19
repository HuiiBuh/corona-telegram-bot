from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    bot_secret: str = Field(env="BOT_SECRET")
    covid_api_url: str = Field(env="COVID_API", default="https://api.corona-zahlen.org/")
    db_location: str = Field(env="DB_LOCATION", default="database/")
    production: bool = Field(env="PRODUCTION", default=False)
    verify_ssl: bool = Field(env="VERIFY_SSL", default=True)


SETTINGS = Settings()
