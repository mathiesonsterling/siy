from typing import Iterable

from siy.entities.sources.base_source import BaseSource
from siy.value_items import DockerTask, BaseDataTable, URL, PublishedState


class CustomDockerImageSource(BaseSource):
    def __init__(self, name: str, docker_task: DockerTask, produced_tables: Iterable[BaseDataTable],
                 state: PublishedState = PublishedState.DEVELOPMENT, depends_on: Iterable[BaseSource] = None):
        super().__init__(name=name, state=state, depends_on=depends_on)
        self.docker_task = docker_task
        self._produced_data_tables = produced_tables

    @property
    def produced_data_tables(self) -> Iterable[BaseDataTable]:
        return self._produced_data_tables

    @property
    def docker_tasks(self) -> Iterable[DockerTask]:
        return [self.docker_task]