from helpers.singleton import Singleton
from models.Districts import DistrictsResponse, Districts
from models.Germany import GermanyResponse
from models.States import StatesResponse, States
from storage.cache import cache
from .api_client import ApiClient


class CovidDatabase(metaclass=Singleton):
    _api_client: ApiClient

    @property
    @cache("*:*:10")
    async def states(self) -> StatesResponse:
        return await self._api_client.get_states()

    @property
    @cache("*:*:10")
    async def districts(self) -> DistrictsResponse:
        return await self._api_client.get_districts()

    @property
    @cache("*:*:10")
    async def germany(self) -> GermanyResponse:
        return await self._api_client.get_germany()

    @property
    @cache("*:*:50")
    async def map(self) -> bytes:
        return await self._api_client.get_district_map()

    async def get_sorted_state_list(self) -> [States]:
        states = (await self.states).data

        return_list = []
        for state in states.values():
            return_list.append(state)
        return_list.sort(key=lambda s: s.name)
        return return_list

    @cache("*:*:50")
    async def get_district_by_state_name(self, state_name: str) -> [Districts]:
        return_list = []
        for district in (await self.districts).data.values():
            if state_name == district.state:
                return_list.append(district)
        return_list.sort(key=lambda k: k.name)
        return return_list

    async def get_district_by_id(self, ags: int) -> Districts:
        if len(str(ags)) < 5:
            ags = f"0{ags}"

        return (await self.districts).data[str(ags)]

    def initialize(self) -> None:
        self._api_client = ApiClient.create()

    async def close(self):
        await self._api_client.close_client()
