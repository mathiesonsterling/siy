from dataclasses import dataclass, field
from typing import Dict

from siy.value_items.url import URL


@dataclass(eq=True, frozen=True)
class DockerTask:
    """
    Basic unit of work.  A single docker image, that includes the arguments to it, to run in the cloud
    """
    image_location: URL
    name: str
    env_vars: Dict[str, str] = field(default_factory={})
