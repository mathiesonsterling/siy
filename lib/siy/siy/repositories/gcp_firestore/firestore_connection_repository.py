from typing import Iterable, Optional

from google.cloud import firestore

from siy.entities import Connection
from siy.repositories.connection_repository import BaseConnectionRepository


class FirestoreConnectionRepository(BaseConnectionRepository):
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)

    def get_all(self) -> Iterable[Connection]:

    def get(self, connection_name: str) -> Optional[Connection]:
        pass

    def get_all_with_destination(self, destination_name: str) -> Iterable[Connection]:
        pass

    def create(self, connection: Connection) -> Connection:
        pass

    def update(self, connection: Connection) -> Connection:
        pass

    def delete(self, connection_name: str) -> bool:
        pass