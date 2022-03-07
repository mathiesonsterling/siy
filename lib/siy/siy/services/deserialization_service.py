from typing import Dict, Any

from siy.entities import BaseSource, BaseDestination, Connection


class DeserializationService:
    def deserialize_source(self, dict_: Dict[str, Any]) -> BaseSource:
        pass

    def deserialize_destination(self, dict_: Dict[str, Any]) -> BaseDestination:
        pass

    def deserialize_connection(self, dict_: Dict[str, Any]) -> Connection:
        # hydrate the sources
        sources = [self.deserialize_source(d) for d in dict_["sources"]]

        # hydrate the destinations
        destinations = [self.deserialize_destination(d) for d in dict_["destinations"]]

        return Connection(
            name=dict_["name"],
            sources=sources,
            destinations=destinations
        )