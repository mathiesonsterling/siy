from dataclasses import dataclass

from siy.entities.data_table import BaseDataTable


@dataclass(frozen=True, eq=True)
class TableProcessedMessage:
    """
    Describes a table being made ready for a destination.  Used to let the destinations work independently
    """
    table: BaseDataTable
    destination_name: str
    handled: bool = False
