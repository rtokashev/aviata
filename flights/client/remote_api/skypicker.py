import datetime
import asyncio
from typing import List, Dict

from client.remote_api.base import RemoteAPIBaseClient
from client.models import SkyPickerSearchParams, SkyPickerCheckParams
from client.utils import timeit, get_logger

logger = get_logger(__name__)


class SkyPickerFlightsSearcher(RemoteAPIBaseClient):
    def __init__(self):
        super().__init__(
            url='https://api.skypicker.com/flights',
        )

    @staticmethod
    def sort_by_price(item):
        return item["price"]

    def get_cheapest_flights(self, all_flights: List[Dict]) -> List[Dict]:
        """
        Flights is default sorted by price.
        Therefore, the price of the first ticket can be considered as the cheapest.
        :param all_flights:
        :return:
        """

        result = []
        # divide flights by date
        flights_by_direction_and_date = {}

        for flight in all_flights:
            direction = flight.get("flyFrom") + flight.get("flyTo")
            if direction not in flights_by_direction_and_date:
                flights_by_direction_and_date[direction] = {}
            date = datetime.datetime.fromtimestamp(flight.get("dTime")).strftime('%d/%m/%Y')
            if date not in flights_by_direction_and_date[direction]:
                flights_by_direction_and_date[direction][date] = []
            flights_by_direction_and_date[direction][date].append(flight)

        for direction, dates in flights_by_direction_and_date.items():
            for date in dates:
                flights_by_direction_and_date[direction][date].sort(key=self.sort_by_price)
                result.append(flights_by_direction_and_date[direction][date][0])

        return result

    async def find_flights(self, queries_list: List[SkyPickerSearchParams]) -> List[Dict]:
        max_parallel_connections = 10
        params_list = [SkyPickerSearchParams(**query) for query in queries_list]
        logger.info("Started searching all flights")
        all_flights = await self.fetch_all(
            max_parallel_connections=max_parallel_connections,
            url=self.url, params_list=params_list
        )
        logger.info("Getting all cheapest flights from all")
        result = []
        [result.extend(self.get_cheapest_flights(flights.get("data"))) for flights in all_flights]
        return result

    @timeit
    def execute_requests(self, query_list: List[Dict]) -> List[Dict]:
        available_flights = asyncio.run(self.find_flights(query_list))
        return available_flights


class SkyPickerFlightsChecker(RemoteAPIBaseClient):
    def __init__(self):
        super().__init__(
            url='https://api.skypicker.com/api/v0.1/check_flights'
        )

    @staticmethod
    def get_valid_flights(flights: List[Dict]) -> List[Dict]:
        valid_flights = []
        for flight in flights:
            if flight.get("flights_checked") and not flight.get("flights_invalid"):
                valid_flights.append(flight)
        return valid_flights

    async def check_flights(self, queries_list: List[Dict]) -> List[Dict]:
        max_parallel_connections = 10

        params_list = [
            SkyPickerCheckParams(
                v=3,
                booking_token=query.get("booking_token"),
                bnum=1,
                pnum=1,
                affily="picky_kz",
                currency="KZT"
            ) for query in queries_list
        ]

        logger.info("Started checking of all cheapest flights on check_flights endpoint")
        all_flights = await self.fetch_all(
            max_parallel_connections=max_parallel_connections,
            url=self.url, params_list=params_list
        )
        valid_flights = self.get_valid_flights(all_flights)
        logger.info("Getting all checked and valid cheapest flights")
        return valid_flights

    @timeit
    def execute_requests(self, queries_list: List[Dict]) -> List[Dict]:
        valid_flights = asyncio.run(self.check_flights(queries_list))
        return valid_flights

# TODO add logging
