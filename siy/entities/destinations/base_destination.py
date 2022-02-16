from abc import ABC, abstractmethod
from typing import Iterable, Optional
from datetime import timedelta

from siy.value_items import BaseDataTable, DockerTask


class BaseDestination(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def export_tables(self, tables: Iterable[BaseDataTable]) -> None:
        # note this works on tables, not connections, as some destinations might requires ALL connections at once!
        raise NotImplementedError()

    @abstractmethod
    @property
    def processes_all_connections(self) -> bool:
        """
        If true, this destination wants to take all tables in a single gulp, so it can make a larger answer
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    @property
    def docker_tasks(self) -> Iterable[DockerTask]:
        raise NotImplementedError()

    @property
    def update_frequency(self) -> Optional[timedelta]:
        return None
