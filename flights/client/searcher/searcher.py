import datetime
from typing import List

from client.searcher.base import BaseSearcher
from client.remote_api.base import RemoteAPIBaseClient
from client.models import FlightSearchParams, SkyPickerSearchParams
from client.utils import get_logger

logger = get_logger(__name__)


class Searcher(BaseSearcher):
    def __init__(self, remote_api_client: RemoteAPIBaseClient):
        self.remote_api_client = remote_api_client

    @staticmethod
    def generate_monthly_requests(directions: List[FlightSearchParams]):
        """
        Generate query list for SkyPicker and etc.
        :param directions:
        :return:
        """
        query_list = []
        start_date = datetime.datetime.today()
        end_date = start_date + datetime.timedelta(days=31)
        for direction in directions:
            query_list.append(
                SkyPickerSearchParams(
                    fly_from=direction.get("fly_from"),
                    fly_to=direction.get("fly_to"),
                    date_from=start_date.strftime('%d/%m/%Y'),
                    date_to=end_date.strftime('%d/%m/%Y'),
                    partner="picky",
                    partner_market="kz",
                    curr="KZT"
                )
            )
        return query_list

    def search(self, directions: List[FlightSearchParams]):
        query_list = self.generate_monthly_requests(directions)
        return self.remote_api_client.execute_requests(query_list)


# if __name__ == '__main__':
#     collector = Searcher(remote_api_client=SkyPickerFlightsSearcher())
#     result = collector.search(_directions=directions)
#
#     with open("../cf.json", "w+") as file:
#         file.write(json.dumps(result))
