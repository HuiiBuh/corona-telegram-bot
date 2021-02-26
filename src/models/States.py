from typing import Dict

from pydantic import BaseModel, Field

from models.Shared import Delta, Meta


class States(BaseModel):
    id: int
    name: str
    population: int
    cases: int
    deaths: int
    cases_per_week: int = Field(alias="casesPerWeek")
    deaths_per_week: int = Field(alias="deathsPerWeek")
    recovered: int
    abbreviation: str
    week_incidence: float = Field(alias="weekIncidence")
    cases_per100_k: float = Field(alias="casesPer100k")
    delta: Delta


class StatesResponse(BaseModel):
    data: Dict[str, States]
    meta = Meta
