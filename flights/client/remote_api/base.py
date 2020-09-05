import json
import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict

import aiohttp


class RemoteAPIBaseClient(ABC):
    def __init__(self, url: str):
        self.headers = {"Content-Type": "application/json"}
        self.url = url

    """
    This is an abstract class, with the execute_requests pseudo-interface,
    which must be overwritten in the inherited classes for a specific implementation.
    """

    async def fetch_all(self, max_parallel_connections: int, url: str, params_list: List[Dict]):
        tasks = []
        connector = aiohttp.TCPConnector(limit=max_parallel_connections)
        async with aiohttp.ClientSession(connector=connector, headers=self.headers) as session:
            for params in params_list:
                tasks.append(self._fetch(session, url, params=params))
            ''' without return_exceptions parameter for avoid any exception on top level context '''
            result = await asyncio.gather(*tasks)
            return result

    @staticmethod
    async def _fetch(session: aiohttp.ClientSession, url: str, params: dict):
        async with session.get(url=url, params=params) as response:
            '''
            Do not use the response.json coroutine, the reason is that the check_flights endpoint has an error 
            associated with an invalid Content-Type header with the value text/html instead of application/json.
            '''
            resp = await response.read()
            resp = json.loads(resp)
            return resp

    @abstractmethod
    def execute_requests(self, query_list: List[Dict]) -> List[Dict]:
        raise NotImplementedError
