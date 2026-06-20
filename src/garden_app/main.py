from importlib.metadata import version
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from garden_app.domain.types import Category, Location
from garden_app.logging_config import setup_logging
from garden_app.models.health_response import HealthResponse
from garden_app.models.map_response import MapResponse
from garden_app.models.root_response import RootResponse
from garden_app.models.task_response import TasksResponse
from garden_app.services.map_layers import fetch_map_geojson_layers
from garden_app.services.task_service import get_visible_tasks

setup_logging()

app = FastAPI(
    title="Garden Tasks API",
    version="0.1.0",
    description="Backend API for managing community garden tasks",
    openapi_tags=[
        {"name": "Meta", "description": "Service info and health"},
        {"name": "Tasks", "description": "Garden tasks"},
        {"name": "Map", "description": "Garden map layers"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://garden-tasks-git-dev-aga87s-projects.vercel.app",
        "https://garden-tasks-eight.vercel.app",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
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
    location: Annotated[list[Location] | None, Query()] = None,
    category: Annotated[list[Category] | None, Query()] = None,
) -> TasksResponse:
    tasks = get_visible_tasks(location, category)
    return TasksResponse(tasks=tasks)


@app.get("/map", tags=["Map"])
def map_layers() -> MapResponse:
    geojsons = fetch_map_geojson_layers()
    return MapResponse(geojsons=geojsons)
