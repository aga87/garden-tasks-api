from dotenv import load_dotenv
from fastapi import FastAPI

from garden_app.logging_config import setup_logging
from garden_app.services.task_service import get_visible_tasks

load_dotenv()
setup_logging()

app = FastAPI(
    title="Garden Tasks API",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Garden Tasks API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks() -> dict[str, list[dict[str, object]]]:
    tasks = get_visible_tasks()
    return {"tasks": [task.model_dump() for task in tasks]}
