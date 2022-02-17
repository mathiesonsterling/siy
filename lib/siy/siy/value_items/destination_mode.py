from enum import Enum


class DestinationMode(Enum):
    OVERWRITE = 1
    INCREMENTAL = 2

    @staticmethod
    def parse(string: str) -> "DestinationMode":
        val = string.upper().strip()

        if val == "OVERWRITE":
            return DestinationMode.OVERWRITE
        elif val == "INCREMENTAL":
            return DestinationMode.INCREMENTAL
        else:
            raise ValueError(f"Invalid value of {val} is not a DestinationMode")
