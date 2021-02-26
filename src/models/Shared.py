from datetime import datetime

from pydantic import BaseModel, Field


class Delta(BaseModel):
    cases: int
    deaths: int
    recovered: int


class Meta(BaseModel):
    source: str
    contact: str
    info: str
    last_update: datetime = Field(alias="lastUpdate")
    last_checked_for_update: datetime = Field(alias="lastCheckedForUpdate")


class R(BaseModel):
    value: float
    date: datetime
