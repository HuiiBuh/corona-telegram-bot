from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel, Field

from models.Shared import Meta


# District Incidence history
class HistoryIncidenceItem(BaseModel):
    week_incidence: float = Field(alias="weekIncidence")
    date: datetime


class DistrictHistoryIncidence(BaseModel):
    ags: str
    name: str
    history: List[HistoryIncidenceItem]


class InternalHistoryDistrictIncidenceResponse(BaseModel):
    data: Dict[str, DistrictHistoryIncidence]
    meta: Meta


class HistoryDistrictIncidenceResponse(BaseModel):
    data: List[HistoryIncidenceItem]
    ags: str
    name: str


# District cases history
class HistoryCasesItem(BaseModel):
    cases: int
    date: datetime


class DistrictHistoryCases(BaseModel):
    ags: str
    name: str
    history: List[HistoryCasesItem]


class InternalHistoryDistrictCasesResponse(BaseModel):
    data: Dict[str, DistrictHistoryCases]
    meta: Meta


class HistoryDistrictCasesResponse(BaseModel):
    data: List[HistoryCasesItem]
    ags: str
    name: str


# Germany cases history
class HistoryGermanIncidenceResponse(BaseModel):
    data: List[HistoryIncidenceItem]
    meta: Meta


# Vaccination cases history
class VaccinationHistoryItem(BaseModel):
    date: datetime
    vaccinated: int
    firstVaccination: int
    secondVaccination: float


class VaccinationHistory(BaseModel):
    history: List[VaccinationHistoryItem]


class VaccinationHistoryResponse(BaseModel):
    data: VaccinationHistory
    meta: Meta
