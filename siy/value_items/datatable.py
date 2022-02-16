from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from siy.value_items.published_state import PublishedState


class BaseDataTable(ABC):
    def __init__(self, state: PublishedState = PublishedState.DEVELOPMENT):
        self._state = state

    @property
    def state(self) -> PublishedState:
        return self._state

    @abstractmethod
    def __eq__(self, other: "DataTable") -> bool:
        pass

    @abstractmethod
    def str(self) -> str:
        pass


@dataclass(frozen=True)
class BigQueryDataTable(BaseDataTable):
    project_id: str
    dataset: str
    table_name: str

    def __eq__(self, other: "DataTable") -> bool:
        if not isinstance(other, BigQueryDataTable):
            return False

        return self.project_id == other.project_id and self.dataset == other.dataset and self.table_name == other.table_name

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
