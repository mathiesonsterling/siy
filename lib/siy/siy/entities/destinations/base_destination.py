from abc import ABC, abstractmethod
from typing import Iterable, Optional
from datetime import timedelta

from siy.value_items import BaseDataTable, DockerTask


class BaseDestination(ABC):
    """
    A method to make data available to the outside world
    Note that these should work async - while connections will notify them of pending updates,
    the choice of how and when to update the output is up to the destination alone!
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def export_tables(self, tables: Iterable[BaseDataTable]) -> None:
        # note this works on tables, not connections, as some destinations might requires ALL connections at once!
        raise NotImplementedError()

    @property
    def update_frequency(self) -> Optional[timedelta]:
        return None

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError()