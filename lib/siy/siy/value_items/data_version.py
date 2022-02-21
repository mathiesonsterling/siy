from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class DataVersion:
    value: str

    def __gt__(self, other: "DataVersion") -> bool:
        return self.value > other.value

    def __ge__(self, other: "DataVersion") -> bool:
        return self.value >= other.value

    def __lt__(self, other: "DataVersion") -> bool:
        return self.value < other.value

    def __le__(self, other: "DataVersion") -> bool:
        return self.value <= other.value
