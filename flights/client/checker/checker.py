from typing import List, Dict

from client.checker.base import BaseChecker
from client.remote_api.base import RemoteAPIBaseClient
from client.utils import get_logger

logger = get_logger(__name__)


class Checker(BaseChecker):
    def __init__(self, remote_api_client: RemoteAPIBaseClient):
        self.remote_api_client = remote_api_client

    def check(self, query_list: List[Dict]):
        return self.remote_api_client.execute_requests(query_list)


# if __name__ == '__main__':
#     collector = Checker(remote_api_client=SkyPickerFlightsChecker())
#     result = collector.check(query_list=[])
#
#     with open("../cf.json", "w+") as file:
#         file.write(json.dumps(result))
