import logging

from garden_app.domain.task_sorting import sort_tasks
from garden_app.domain.task_visibility import (
    filter_tasks_by_category,
    filter_tasks_by_location,
    filter_tasks_by_status,
    filter_tasks_by_visible_months,
)
from garden_app.domain.types import Category, Location
from garden_app.models.task import Task
from garden_app.services.task_loader import load_tasks_from_sheet

logger = logging.getLogger(__name__)


def get_visible_tasks(
    locations: list[Location] | None,
    category: Category | None,
) -> list[Task]:
    tasks = load_tasks_from_sheet()

    visible_tasks = filter_tasks_by_status(tasks)
    visible_tasks = filter_tasks_by_visible_months(visible_tasks)
    visible_tasks = filter_tasks_by_location(visible_tasks, locations)
    visible_tasks = filter_tasks_by_category(visible_tasks, category)

    visible_tasks = sort_tasks(visible_tasks)

    logger.info(
        "Filtered %d tasks to %d visible tasks (locations=%s, category=%s)",
        len(tasks),
        len(visible_tasks),
        locations,
        category,
    )

    return visible_tasks
