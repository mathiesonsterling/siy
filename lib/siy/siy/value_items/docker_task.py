from dataclasses import dataclass, field, asdict
from typing import Dict, Union

from siy.value_items.url import URL


@dataclass(eq=True, frozen=True)
class DockerTask:
    """
    Basic unit of work.  A single docker image, that includes the arguments to it, to run in the cloud
    """
    image_location: URL
    name: str
    env_vars: Dict[str, str] = field(default_factory={})

    def to_dict(self) -> Dict[str, Union[str, Dict[str, str]]]:
        return asdict(self)
