from typing import Iterable, Dict, Union

from siy.entities.sources.base_source import BaseSource
from siy.value_items import DockerTask, BaseDataTable, URL, PublishedState


class CustomDockerImageSource(BaseSource):
    """
    Allows us to run any image in the repository
    """
    def __init__(
        self,
        name: str,
        docker_task: DockerTask,
        produced_tables: Iterable[BaseDataTable],
        state: PublishedState = PublishedState.DEVELOPMENT,
        depends_on_names: Iterable[str] = None
    ):
        super().__init__(name=name, state=state, depends_on_names=depends_on_names, data_lake=None)
        self.docker_task = docker_task
        self._produced_data_tables = produced_tables

    @property
    def produced_data_tables(self) -> Iterable[BaseDataTable]:
        return self._produced_data_tables

    @property
    def docker_tasks(self) -> Iterable[DockerTask]:
        return [self.docker_task]

    def to_dict(self) -> Dict[str, Union[str, Dict[str, str]]]:
        return {
            "name": self.name,
            "docker_task": self.docker_task.to_dict(),
            "produced_tables": [t.to_dict() for t in self.produced_data_tables],
            "state": str(self.state),
            "depends_on": [s.name for s in self.depends_on],
            "type": type(self)
        }
