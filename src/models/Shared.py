from datetime import datetime
from typing import Optional

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


class DateValue(BaseModel):
    date: datetime
    value: Optional[float]


class R(BaseModel):
    value: Optional[float]
    date: Optional[datetime]
    r_value_4_days: DateValue = Field(alias="rValue4Days")
    r_value_7_days: DateValue = Field(alias="rValue7Days")
