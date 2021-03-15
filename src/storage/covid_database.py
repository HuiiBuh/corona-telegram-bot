import io
from typing import List, Union, Iterator

from matplotlib import pyplot
from matplotlib.ticker import FuncFormatter
from pycache import cache

from helpers.singleton import Singleton
from models.Districts import DistrictsResponse, Districts
from models.Germany import GermanyResponse
from models.History import HistoryDistrictIncidenceResponse, HistoryDistrictCasesResponse, \
    HistoryGermanIncidenceResponse, VaccinationHistoryResponse, VaccinationHistoryItem
from models.States import StatesResponse, States
from .api_client import ApiClient


class CovidDatabase(metaclass=Singleton):
    _api_client: ApiClient

    @cache("*:60:00")
    async def states(self) -> StatesResponse:
        return await self._api_client.get_states()

    @cache("*:60:00")
    async def districts(self) -> DistrictsResponse:
        return await self._api_client.get_districts()

    @cache("*:60:00")
    async def germany(self) -> GermanyResponse:
        return await self._api_client.get_germany()

    @cache("*:60:00")
    async def map(self) -> bytes:
        return await self._api_client.get_district_map()

    @cache("*:60:00")
    async def get_district_incidence_history(self, district_id: str,
                                             days: int = 42) -> HistoryDistrictIncidenceResponse:
        return await self._api_client.get_district_incidence_history(district_id, days)

    @cache("*:60:00")
    async def get_district_cases_history(self, district_id: str,
                                         days: int = 42) -> HistoryDistrictCasesResponse:
        return await self._api_client.get_district_cases_history(district_id, days)

    @cache("*:60:00")
    async def get_german_incidence_history(self, days: int = 42) -> HistoryGermanIncidenceResponse:
        return await self._api_client.get_german_history(days)

    @cache("*:60:00")
    async def get_vaccination_history(self) -> VaccinationHistoryResponse:
        return await self._api_client.get_vaccination_history()

    async def get_sorted_state_list(self) -> [States]:
        states = (await self.states()).data

        return_list = []
        for state in states.values():
            return_list.append(state)
        return_list.sort(key=lambda s: s.name)
        return return_list

    async def get_district_by_state_name(self, state_name: str) -> [Districts]:
        return_list = []
        for district in (await self.districts()).data.values():
            if state_name == district.state:
                return_list.append(district)
        return_list.sort(key=lambda k: k.name)
        return return_list

    async def get_district_by_id(self, ags: str) -> Districts:
        return (await self.districts()).data[ags]

    async def get_ordered_district_by_ids(self, ags_list: [str]) -> [Districts]:
        return_list = []
        district_dict = (await self.districts()).data
        for ags in ags_list:
            if ags in district_dict:
                return_list.append(district_dict[ags])

        return_list.sort(key=lambda k: k.name)
        return return_list

    async def get_incidence_plot(self, district_id: str = None, days: int = 42) -> bytes:
        if district_id:
            district_history = await self.get_district_incidence_history(district_id, days)
        else:
            district_history = await self.get_german_incidence_history()

        incidence_list = list(map(lambda x: x.week_incidence, district_history.data))
        return CovidDatabase._generate_plot(incidence_list)

    async def calculate_r(self, district_id: str, generation_time=7) -> float:
        district_history = (await self.get_district_cases_history(district_id))
        district_history.data.reverse()
        district_history = list(map(lambda x: x.cases, district_history.data))

        # Ignore the last four days
        relevant_data = district_history[4:]

        new_infections = 0
        old_infections = 0
        for i in range(generation_time):
            new_infections += relevant_data[i]
            old_infections += relevant_data[i + generation_time]

        return round(new_infections / old_infections, 2)

    async def get_vaccination_plot(self):
        history_list: List[VaccinationHistoryItem] = (await self.get_vaccination_history()).data.history
        vaccinated_list = CovidDatabase._accumulate_list(map(lambda item: item.vaccinated, history_list))
        second_list = CovidDatabase._accumulate_list(map(lambda item: item.secondVaccination, history_list))
        return CovidDatabase._generate_vaccination_plot(vaccinated_list, second_list)

    @staticmethod
    def _generate_vaccination_plot(vaccination_list: List[float], second_vaccination_list: List[float]) -> bytes:
        _, ax = pyplot.subplots()

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x / 1000000)}"))

        pyplot.plot(vaccination_list, label="People with one vaccination")
        pyplot.plot(second_vaccination_list, label="People with two vaccinations")
        pyplot.ylabel("Vaccinations in million")
        pyplot.ylim(0, max(vaccination_list) * 2)
        pyplot.legend(loc="upper left")
        buffer = CovidDatabase._to_buffer(pyplot)
        pyplot.close()
        return buffer

    @staticmethod
    def _generate_plot(y: [float], y_label="Incidence", x_label="Weeks", show_limits=True) -> bytes:
        x = []
        week_ticks = []
        for i in range(len(y)):
            x.append(i)
            if i % 7 == 0:
                week_ticks.append(-int(i / 7))
            else:
                week_ticks.append("")

        week_ticks.reverse()

        pyplot.xticks(x, week_ticks)

        pyplot.plot(x, y, color="black")

        if show_limits:
            pyplot.plot(x, [50] * len(y), color="#b9b922")

            if max(y) > 90:
                pyplot.plot(x, [100] * len(y), color="lightcoral")

        pyplot.ylabel(y_label)
        pyplot.xlabel(x_label)
        pyplot.ylim(0, max(y) + 10)
        buffer = CovidDatabase._to_buffer(pyplot)
        pyplot.close()
        return buffer

    @staticmethod
    def _accumulate_list(old_list: Union[List[float], Iterator]) -> List[float]:
        new_list = []
        last_value = 0
        for item in old_list:
            new_list.append(item + last_value)
            last_value = item + last_value

        return new_list

    @staticmethod
    def _to_buffer(plot: pyplot) -> bytes:
        buf = io.BytesIO()
        plot.savefig(buf, format='png')
        buf.seek(0)
        return buf.read()

    def initialize(self) -> None:
        self._api_client = ApiClient.create()

    async def close(self):
        await self._api_client.close_client()
