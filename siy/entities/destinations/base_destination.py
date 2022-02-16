from abc import ABC, abstractmethod
from typing import Iterable

from siy.value_items import DataTable


class BaseDestination(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def export_tables(self, tables: Iterable[DataTable]) -> None:
        # note this works on tables, not connections, as some destinations might requires ALL connections at once!
        raise NotImplementedError()

    @abstractmethod
    @property
    def processes_all_connections(self) -> bool:
        raise NotImplementedError()