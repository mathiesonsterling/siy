from enum import Enum


class PublishedState(Enum):
    DEVELOPMENT = 1
    TESTING = 2
    PUBLISHED = 3

    def __str__(self):
        return self.name
