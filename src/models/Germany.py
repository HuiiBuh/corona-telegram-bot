from pydantic import BaseModel, Field

from models.Shared import Delta, R, Meta


class GermanyResponse(BaseModel):
    cases: int
    deaths: int
    recovered: int
    week_incidence: float = Field(alias="weekIncidence")
    cases_per_week: int = Field(alias="casesPerWeek")
    cases_per100_k: float = Field(alias="casesPer100k")

    delta: Delta
    r: R
    meta: Meta
