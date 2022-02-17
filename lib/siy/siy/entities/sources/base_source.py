from abc import ABC, abstractmethod
from typing import Iterable, Optional
from datetime import timedelta

from siy.value_items import BaseDataTable, DockerTask, PublishedState
from siy.entities.data_lakes import BaseDataLake


class BaseSource(ABC):
    """
    Anything that adds data to the data lake, regardless of if it's an internal or external source, is a Source
    """
    def __init__(self,
                 name: str,
                 data_lake: BaseDataLake,
                 state: PublishedState = PublishedState.DEVELOPMENT,
                 depends_on: Iterable["BaseSource"] = None):
        self.name = name
        self.data_lake = data_lake

        if not depends_on:
            depends_on = []
        self.depends_on = depends_on

        self._state = state

    @property
    @abstractmethod
    def produced_data_tables(self) -> Iterable[BaseDataTable]:
        raise NotImplementedError()

    @property
    def update_frequency(self) -> Optional[timedelta]:
        return None

    @property
    def state(self) -> PublishedState:
        return self._state

    @abstractmethod
    @property
    def docker_tasks(self) -> Iterable[DockerTask]:
        raise NotImplementedError()
