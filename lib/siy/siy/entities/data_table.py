from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Dict, Any

from siy.value_items.published_state import PublishedState
from siy.value_items.data_version import DataVersion


class BaseDataTable(ABC):
    def __init__(self, state: PublishedState = PublishedState.DEVELOPMENT, data_version: DataVersion = None):
        self._state = state

        if not data_version:
            data_version = DataVersion(value="v1")
        self._data_version = data_version

    @abstractmethod
    @property
    def id(self) -> str:
        raise NotImplementedError()

    @property
    def state(self) -> PublishedState:
        return self._state

    @property
    def data_version(self) -> DataVersion:
        return self._data_version

    def __eq__(self, other: "DataTable") -> bool:
        if not isinstance(other, BaseDataTable):
            raise ValueError("Can only equate data tables!")
        return self.id == other.id

    @abstractmethod
    def str(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError()


@dataclass(frozen=True)
class BigQueryDataTable(BaseDataTable):
    project_id: str
    dataset: str
    table_name: str

    def id(self) -> str:
        return str(self)

    def str(self) -> str:
        return f"{self.project_id}.{self.dataset}.{self.table_name}"

    @staticmethod
    def parse(string: str) -> "BigQueryDataTable":
        parts = string.split(".")
        if not len(parts) == 3:
            raise ValueError("String must be a fully qualitifed BigQueryTable proj.dataset.table")
        return BigQueryDataTable(
            project_id=parts[0],
            dataset=parts[1],
            table_name=parts[2]
        )

    def to_dict(self):
        return asdict(self)
