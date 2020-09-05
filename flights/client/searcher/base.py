from abc import ABC, abstractmethod
from typing import List

from client.models import FlightSearchParams


class BaseSearcher(ABC):
    @abstractmethod
    def search(self, _directions: List[FlightSearchParams]):
        raise NotImplementedError
