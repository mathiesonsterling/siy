from abc import ABC, abstractmethod
from typing import Iterable, Optional
from datetime import timedelta

from siy.value_items import DataTable, DockerTask


class BaseSource(ABC):
    """
    Anything that adds data to the data lake, regardless of if it's an internal or external source, is a Source
    """
    def __init__(self, name: str, depends_on: Iterable["BaseSource"] = None):
        self.name = name

        if not depends_on:
            depends_on = []
        self.depends_on = depends_on

    @abstractmethod
    @property
    def produced_data_tables(self) -> Iterable[DataTable]:
        raise NotImplementedError()

    @property
    def update_frequency(self) -> Optional[timedelta]:
        return None

    @abstractmethod
    @property
    def docker_tasks(self) -> Iterable[DockerTask]:
        raise NotImplementedError()
