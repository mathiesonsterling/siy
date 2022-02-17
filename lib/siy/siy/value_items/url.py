from urllib.parse import urlparse, ParseResult
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class URL:
    value: ParseResult

    def str(self) -> str:
        return str(self.value)

    @staticmethod
    def parse(string: str) -> "URL":
        val = urlparse(string)
        return URL(value=val)
