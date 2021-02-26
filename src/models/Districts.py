from typing import Dict

from pydantic import BaseModel, Field

from models.Shared import Meta, Delta


class Districts(BaseModel):
    ags: int
    name: str
    county: str
    state: str
    population: int
    cases: int
    deaths: int
    cases_per_week: int = Field(alias="casesPerWeek")
    deaths_per_week: int = Field(alias="deathsPerWeek")
    stateAbbreviation: str
    recovered: int
    week_incidence: float = Field(alias="weekIncidence")
    cases_per100_k: float = Field(alias="casesPer100k")
    delta: Delta


class DistrictsResponse(BaseModel):
    data: Dict[str, Districts]
    meta = Meta
