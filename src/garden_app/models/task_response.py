from pydantic import BaseModel

from garden_app.models.task import Task


class TasksResponse(BaseModel):
    tasks: list[Task]
