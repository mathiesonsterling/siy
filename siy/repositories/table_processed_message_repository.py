from abc import ABC, abstractmethod
from typing import Iterable

from siy.value_items import TableProcessedMessage


class BaseTableProcessedMessageRepository(ABC):
    """
    Holds all waiting messages for which tables need to be processed
    """
    @abstractmethod
    def get_pending_for_destination(self, destination_name: str) -> Iterable[TableProcessedMessage]:
        raise NotImplementedError()

    @abstractmethod
    def add(self, message: TableProcessedMessage) -> TableProcessedMessage:
        raise NotImplementedError()
