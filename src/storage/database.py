from helpers.singleton import Singleton
from models.Districts import DistrictsResponse
from models.Germany import GermanyResponse
from models.States import StatesResponse
from storage.cache import cache
from .api_client import ApiClient


class Database:
    __metaclass__ = Singleton

    _api_client: ApiClient

    @property
    @cache(10)
    async def states(self) -> StatesResponse:
        return await self._api_client.get_states()

    @property
    @cache(10)
    async def districts(self) -> DistrictsResponse:
        return await self._api_client.get_districts()

    @property
    @cache(10)
    async def germany(self) -> GermanyResponse:
        return await self._api_client.get_germany()

    def initialize(self) -> None:
        self._api_client = ApiClient.create()

    async def close(self):
        await self._api_client.close_client()
