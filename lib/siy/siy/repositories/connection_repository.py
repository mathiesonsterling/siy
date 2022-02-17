from abc import ABC, abstractmethod
from typing import Optional, Iterable, Dict

from siy.entities import Connection


class BaseConnectionRepository(ABC):
    @abstractmethod
    def get_all(self) -> Iterable[Connection]:
        raise NotImplementedError()

    @abstractmethod
    def get(self, connection_name: str) -> Optional[Connection]:
        raise NotImplementedError()

    def create(self, connection: Connection) -> Connection:
        raise NotImplementedError()

    def update(self, connection: Connection) -> Connection:
        raise NotImplementedError()
    
    def delete(self, connection_name: str) -> bool:
        raise NotImplementedError()


class MemoryConnectionRepository(BaseConnectionRepository):
    """
    Basic repo for in-memory, with no actual persistence
    """
    def __init__(self):
        self._items: Dict[str, Connection] = {}

    def get_all(self) -> Iterable[Connection]:
        return self._items.values()

    def get(self, connection_name: str) -> Optional[Connection]:
        if connection_name in self._items:
            return self._items[connection_name]
        return None

    def create(self, connection: Connection) -> Connection:
        if connection.name in self._items:
            raise ValueError(f"Connection {connection.name} exists, please ue update")
        self._items[connection.name] = connection
        return connection

    def update(self, connection: Connection) -> Connection:
        if connection.name not in self._items:
            raise ValueError(f"Connection {connection.name} does not exist, call create")
        self._items[connection.name] = connection
        return connection

    def delete(self, connection_name: str) -> bool:
        if connection_name in self._items:
            del self._items[connection_name]
        return True
