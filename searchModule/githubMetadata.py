from dataclasses import dataclass
from datetime import datetime


@dataclass
class GithubMetadata:
    cloneUrl: str = None
    stars: int = 0
    pushDate: datetime = None
