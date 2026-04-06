import logging

from garden_app.domain.task_sorting import sort_tasks
from garden_app.domain.task_visibility import (
    filter_tasks_by_location,
    filter_tasks_for_current_window,
)
from garden_app.domain.time import get_current_month, get_month_window
from garden_app.domain.types import Location
from garden_app.models.task import Task
from garden_app.services.task_loader import load_tasks_from_sheet

logger = logging.getLogger(__name__)


def get_visible_tasks(location: Location | None) -> list[Task]:
    tasks = load_tasks_from_sheet()

    current_month = get_current_month()
    visible_months = get_month_window(current_month)

    visible_tasks = filter_tasks_for_current_window(tasks)
    visible_tasks = filter_tasks_by_location(visible_tasks, location)
    visible_tasks = sort_tasks(visible_tasks)

    logger.info(
        "Filtered %d tasks to %d tasks for months %s",
        len(tasks),
        len(visible_tasks),
        sorted(visible_months),
    )

    return visible_tasks
