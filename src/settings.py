from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    bot_secret: str = Field(env="BOT_SECRET")
    production: bool = Field(env="PRODUCTION", default=False)


SETTINGS = Settings()
