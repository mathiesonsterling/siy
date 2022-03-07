from typing import Iterable, Optional

from google.cloud import firestore

from siy.entities import Connection
from siy.repositories.connection_repository import BaseConnectionRepository
from siy.services import DeserializationService


class FirestoreConnectionRepository(BaseConnectionRepository):
    def __init__(self, project_id: str, deserialization_service: DeserializationService = None):
        self.db = firestore.Client(project=project_id)

        if not deserialization_service:
            deserialization_service = DeserializationService()
        self.deserialization_service = deserialization_service

    def _hydrate_connection(self, dict_) -> Connection:
        return self.deserialization_service.deserialize_connection(dict_)

    @property
    def _collection(self):
        return self.db.collection("connections")

    def get_all(self) -> Iterable[Connection]:
        for d in self._collection.stream():
            yield self._hydrate_connection(dict_=d.to_dict())

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
