from __future__ import annotations

from typing import Optional, Union

from aiohttp import ClientSession, TCPConnector, ClientTimeout, DummyCookieJar

from helpers.singleton import Singleton
from models.Districts import DistrictsResponse
from models.Germany import GermanyResponse
from models.History import HistoryGermanIncidenceResponse, InternalHistoryDistrictCasesResponse, \
    HistoryDistrictIncidenceResponse, HistoryDistrictCasesResponse, InternalHistoryDistrictIncidenceResponse, \
    VaccinationHistoryResponse
from models.States import StatesResponse
from settings import SETTINGS


class ApiClient:
    __metaclass__ = Singleton

    def __init__(self, base_url: str, request_timeout: int, request_limit: int):
        self._timeout: ClientTimeout = ClientTimeout(total=request_timeout)
        self._connector: TCPConnector = TCPConnector(limit=request_limit,
                                                     enable_cleanup_closed=True,
                                                     verify_ssl=SETTINGS.verify_ssl
                                                     )
        self._client_session: Optional[ClientSession] = None
        self.base_url: str = base_url

    def create_client(self) -> None:
        if not self._client_session:
            self._client_session = ClientSession(
                connector=self._connector,
                timeout=self._timeout,
                cookie_jar=DummyCookieJar()
            )

    async def close_client(self) -> None:
        if self._client_session:
            await self._client_session.close()
        self._client_session = None

    async def get_states(self) -> StatesResponse:
        response = await self._get("states")
        return StatesResponse(**response)

    async def get_districts(self) -> DistrictsResponse:
        response = await self._get("districts")
        return DistrictsResponse(**response)

    async def get_germany(self) -> GermanyResponse:
        response = await self._get("germany")
        return GermanyResponse(**response)

    async def get_district_map(self) -> bytes:
        return await self._get("map/districts")

    async def get_district_cases_history(self, district_id: str, days: int) -> HistoryDistrictCasesResponse:
        history = await self._get(f"districts/{district_id}/history/cases/{days}")
        history_object = InternalHistoryDistrictCasesResponse(**history)
        keys = list(history_object.data.keys())
        data = history_object.data[keys[0]]
        return HistoryDistrictCasesResponse(data=data.history, ags=data.ags, name=data.name)

    async def get_district_incidence_history(self, district_id: str, days: int) -> HistoryDistrictIncidenceResponse:
        history = await self._get(f"districts/{district_id}/history/incidence/{days}")
        history_object = InternalHistoryDistrictIncidenceResponse(**history)
        keys = list(history_object.data.keys())
        data = history_object.data[keys[0]]
        return HistoryDistrictIncidenceResponse(data=data.history, ags=data.ags, name=data.name)

    async def get_german_history(self, days: int) -> HistoryGermanIncidenceResponse:
        history = await self._get(f"germany/history/incidence/{days}")
        return HistoryGermanIncidenceResponse(**history)

    async def get_vaccination_history(self) -> VaccinationHistoryResponse:
        history = await self._get(f"vaccinations/history")
        return VaccinationHistoryResponse(**history)

    async def _get(self, path: str) -> Union[dict, bytes]:
        if not self._client_session:
            raise Exception("You have to create a client session before you can use the api client")

        async with self._client_session.get(f"{self.base_url}{path}", raise_for_status=True) as request:
            if request.content_type == "application/json":
                return await request.json()
            else:
                return await request.read()

    @staticmethod
    def create() -> ApiClient:
        client = ApiClient(SETTINGS.covid_api_url, request_timeout=10, request_limit=100)
        client.create_client()
        return client
