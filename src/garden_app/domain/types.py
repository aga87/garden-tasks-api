from enum import Enum
from typing import Any, TypedDict


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RecommendedMonthStage(str, Enum):
    early = "early"
    late = "late"


class Status(str, Enum):
    todo = "todo"
    doing = "doing"
    done = "done"
    skip = "skip"


class Location(str, Enum):
    garden = "garden"
    home = "home"


class DriveFile(TypedDict):
    id: str
    name: str


class NamedJSONs(TypedDict):
    json_name: str
    json: Any
