from typing import Literal

from pydantic import BaseModel, Field


class Task(BaseModel):
    title: str
    recommended_month: int = Field(ge=1, le=12)
    recommended_stage: Literal["early", "late"] | None = None
    priority: Literal["low", "medium", "high"] | None = None
    area: str | None = None
    task_type: str | None = None
    notes: str | None = None
    done: bool
