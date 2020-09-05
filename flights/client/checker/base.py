from abc import ABC, abstractmethod
from typing import List, Dict


class BaseChecker(ABC):
    @abstractmethod
    def check(self, _directions: List[Dict]):
        raise NotImplementedError
