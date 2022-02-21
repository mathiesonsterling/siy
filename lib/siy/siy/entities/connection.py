from dataclasses import dataclass, field
from typing import Iterable, Optional, Dict, Any
from datetime import timedelta

from siy.entities.sources.base_source import BaseSource
from siy.entities.destinations.base_destination import BaseDestination
from siy.entities.data_table import BaseDataTable


@dataclass(eq=True, frozen=True)
class Connection:
    name: str
    sources: Iterable[BaseSource] = field(default_factory=list)
    destinations: Iterable[BaseDestination] = field(default_factory=list)

    @property
    def produced_tables(self) -> Iterable[BaseDataTable]:
        for s in self.sources:
            yield from s.produced_data_tables

    @property
    def overall_update_frequency(self) -> Optional[timedelta]:
        updating_sources = [s.update_frequency for s in self.sources if s.update_frequency]

        if len(updating_sources) == 0:
            return None
        return min(updating_sources)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "sources": [s.to_dict() for s in self.sources],
            "destinations": [d.to_dict() for d in self.destinations]
        }
