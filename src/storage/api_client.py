from __future__ import annotations

from typing import Optional, Dict

from aiohttp import ClientSession, TCPConnector, ClientTimeout, DummyCookieJar

from helpers.singleton import Singleton
from models.Districts import DistrictsResponse
from models.Germany import GermanyResponse
from models.States import StatesResponse


class ApiClient:
    __metaclass__ = Singleton

    def __init__(self, base_url: str, request_timeout: int, request_limit: int):
        self._timeout: ClientTimeout = ClientTimeout(total=request_timeout)
        self._connector: TCPConnector = TCPConnector(limit=request_limit, enable_cleanup_closed=True)
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
        async with self._client_session.get(f"{self.base_url}map/districts") as request:
            request.raise_for_status()
            return await request.read()

    async def _get(self, path: str) -> Dict:
        if not self._client_session:
            raise Exception("You have to create a client session before you can use the api client")

        async with self._client_session.get(f"{self.base_url}{path}") as request:
            request.raise_for_status()
            try:
                json = await request.json()
            except Exception as e:
                request.close()
                raise e

            return json

    @staticmethod
    def create() -> ApiClient:
        client = ApiClient("https://api.corona-zahlen.org/", 10, 10)
        client.create_client()
        return client
