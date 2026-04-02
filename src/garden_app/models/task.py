from pydantic import BaseModel

from garden_app.domain_types import Priority, RecommendedMonthStage


class Task(BaseModel):
    title: str
    recommended_month: int
    recommended_month_stage: RecommendedMonthStage | None = None
    priority: Priority | None = None
    area: str | None = None
    task_type: str | None = None
    notes: str | None = None
    done: bool
