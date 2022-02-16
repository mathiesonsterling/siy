from abc import ABC, abstractmethod
from dataclasses import dataclass

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


@dataclass(frozen=True)
class BigQueryDataTable(BaseDataTable):
    project_id: str
    dataset: str
    table_name: str

    def __eq__(self, other: "DataTable") -> bool:
        if not isinstance(other, BigQueryDataTable):
            return False

        return self.project_id == other.project_id and self.dataset == other.dataset and self.table_name == other.table_name