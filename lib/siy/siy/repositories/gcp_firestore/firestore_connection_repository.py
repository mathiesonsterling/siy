from typing import Iterable, Optional, Dict, Any

from google.cloud import firestore

from siy.entities import Connection, BaseDestination, BaseSource
from siy.repositories.connection_repository import BaseConnectionRepository


class FirestoreConnectionRepository(BaseConnectionRepository):
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)

    def _hydrate_source(self, dict_: Dict[str, Any]) -> BaseSource:
        pass

    def _hydrate_destination(self, dict_: Dict[str, Any]) -> BaseDestination:
        pass

    def _hydrate_connection(self, dict_: Dict[str, Any]) -> Connection:
        # hydrate the sources
        sources = [self._hydrate_source(d) for d in dict_["sources"]]

        # hydrate the destinations
        destinations = [self._hydrate_destination(d) for d in dict_["destinations"]]

        return Connection(
            name=dict_["name"],
            sources=sources,
            destinations=destinations
        )

    @property
    def _collection(self):
        return self.db.collection("connections")

    def get_all(self) -> Iterable[Connection]:
        for d in self._collection.stream():
            yield self._hydrate_destination(dict_=d.to_dict())

    def get(self, connection_name: str) -> Optional[Connection]:
        doc_ref = self._collection.document(connection_name)
        doc = doc_ref.get()
        if doc.exists:
            return self._hydrate_connection(doc.to_dict())
        else:
            return None

    def create(self, connection: Connection) -> Connection:
        doc = self._collection.document(connection.name)
        doc.set(connection.to_dict())
        return self.get(connection.name)

    def update(self, connection: Connection) -> Connection:
        doc = self._collection.document(connection.name)
        doc.update(connection.to_dict())
        return self.get(connection.name)

    def delete(self, connection_name: str) -> bool:
        doc = self._collection.document(connection_name)
        doc.delete()
        return True
