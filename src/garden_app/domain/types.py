from enum import Enum


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RecommendedMonthStage(str, Enum):
    early = "early"
    late = "late"
