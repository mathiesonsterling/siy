from typing import Dict, Union, Iterable

from siy.entities import BaseDataTable
from siy.entities.sources.base_source import BaseSource
from siy.value_items import DockerTask


class AirbyteIngestSource(BaseSource):
    @property
    def produced_data_tables(self) -> Iterable[BaseDataTable]:
        raise NotImplementedError()

    @property
    def docker_tasks(self) -> Iterable[DockerTask]:
        raise NotImplementedError()

    def to_dict(self) -> Dict[str, Union[str, Dict[str, str]]]:
        raise NotImplementedError()