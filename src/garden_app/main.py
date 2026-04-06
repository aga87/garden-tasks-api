from importlib.metadata import version

from fastapi import FastAPI, Query

from garden_app.domain.types import Location
from garden_app.logging_config import setup_logging
from garden_app.models.health_response import HealthResponse
from garden_app.models.root_response import RootResponse
from garden_app.models.task_response import TasksResponse
from garden_app.services.task_service import get_visible_tasks

setup_logging()

app = FastAPI(
    title="Garden Tasks API",
    version="0.1.0",
    description="Backend API for managing community garden tasks",
    openapi_tags=[
        {"name": "Meta", "description": "Service info and health"},
        {"name": "Tasks", "description": "Garden tasks"},
    ],
)


@app.get("/", response_model=RootResponse, tags=["Meta"])
def root() -> RootResponse:
    return RootResponse(
        name="Garden Tasks API",
        version=version("garden-tasks-api"),
        status="ok",
    )


@app.get("/health", response_model=HealthResponse, tags=["Meta"])
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/tasks", response_model=TasksResponse, tags=["Tasks"])
def get_tasks(
    location: Location = Query(default=None),
) -> TasksResponse:
    tasks = get_visible_tasks(location)
    return TasksResponse(tasks=tasks)
