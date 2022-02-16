from typing import Iterable

from siy.entities.sources.base_source import BaseSource


class DBTSource(BaseSource):
    """
    Source for running DBT models to create more data!
    """
    def __init__(self, end_models: Iterable[str]):
        self.end_models()