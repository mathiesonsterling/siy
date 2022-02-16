from abc import ABC, abstractmethod
from dataclasses import dataclass


class DataTable(ABC):
    @abstractmethod
    def __eq__(self, other: "DataTable") -> bool:
        pass


@dataclass(frozen=True)
class BigQueryDataTable(DataTable):
    project_id: str
    dataset: str
    table_name: str

    def __eq__(self, other: "DataTable") -> bool:
        if not isinstance(other, BigQueryDataTable):
            return False

        return self.project_id == other.project_id and self.dataset == other.dataset and self.table_name == other.table_name