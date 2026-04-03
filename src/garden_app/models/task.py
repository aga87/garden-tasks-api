from pydantic import BaseModel, Field

from garden_app.domain.types import Priority, RecommendedMonthStage


class Task(BaseModel):
    title: str
    recommended_month: int = Field(
        ...,
        ge=1,
        le=12,
        description="Month number (1=January, 12=December)",
    )
    recommended_month_stage: RecommendedMonthStage | None = None
    priority: Priority | None = Field(
        default=None,
        description="Priority of the task (optional)",
    )
    area: str | None = None
    task_type: str | None = None
    notes: str | None = None
    done: bool
