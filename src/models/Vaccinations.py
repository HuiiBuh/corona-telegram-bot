from __future__ import annotations

from typing import Optional

from models.Shared import Meta


class Ation:
    age: int
    job: int
    medical: int
    nursingHome: int
    secondVaccination: Optional[Ation] = None


class PurpleVaccination:
    biontech: None
    moderna: None


class BundSecondVaccination:
    vaccinated: None
    vaccination: PurpleVaccination
    delta: None
    quote: int


class DataVaccination:
    biontech: Optional[int] = None
    moderna: Optional[int] = None
    astraZeneca: Optional[int] = None


class SecondVaccination:
    vaccinated: int
    vaccination: DataVaccination
    delta: int
    quote: float


class Bund:
    administeredVaccinations: None
    name: str
    vaccinated: None
    vaccination: DataVaccination
    delta: None
    quote: int
    secondVaccination: BundSecondVaccination
    indication: Ation


class BaseVaccinationData:
    administeredVaccinations: int
    vaccinated: int
    vaccination: DataVaccination
    delta: int
    quote: float
    secondVaccination: SecondVaccination
    indication: Ation


class StateVaccinationData(BaseVaccinationData):
    name: str


class States:
    BY: StateVaccinationData
    BE: StateVaccinationData
    BB: StateVaccinationData
    BW: StateVaccinationData
    HB: StateVaccinationData
    HH: StateVaccinationData
    HE: StateVaccinationData
    MV: StateVaccinationData
    NI: StateVaccinationData
    NW: StateVaccinationData
    RP: StateVaccinationData
    SL: StateVaccinationData
    SN: StateVaccinationData
    ST: StateVaccinationData
    SH: StateVaccinationData
    TH: StateVaccinationData
    Bund: Bund


class VaccinationData(BaseVaccinationData):
    states: States


class Pokedex:
    data: VaccinationData
    meta: Meta
