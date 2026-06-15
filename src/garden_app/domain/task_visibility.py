from zoneinfo import ZoneInfo

from garden_app.domain.time import get_current_month, get_next_month
from garden_app.domain.types import Category, Location, Status
from garden_app.models.task import Task

APP_TIMEZONE = ZoneInfo("Europe/Amsterdam")

current = get_current_month()

HOME_TASK_TYPES = {"organization", "sowing at home", "promotion"}

TASK_TYPE_CATEGORIES = {
    "bed preparation": Category.cultivation,
    "sowing at home": Category.cultivation,
    "sowing outdoor in soil": Category.cultivation,
    "sowing on seedling table": Category.cultivation,
    "planting": Category.cultivation,
    "harvesting": Category.cultivation,
    "pruning": Category.cultivation,
    "maintenance": Category.maintenance,
    "sawing": Category.maintenance,
    "construction": Category.maintenance,
    "investigation": Category.maintenance,
    "organization": Category.admin,
    "promotion": Category.admin,
}


def filter_tasks_by_location(
    tasks: list[Task],
    locations: list[Location] | None,
) -> list[Task]:
    if not locations:
        return tasks

    selected_locations = set(locations)

    def matches(task: Task) -> bool:
        if task.task_type is None:
            return True  # appears in both

        task_type = task.task_type.strip().lower()

        is_home = task_type in HOME_TASK_TYPES

        if Location.home in selected_locations and is_home:
            return True

        if Location.garden in selected_locations and not is_home:
            return True

        return False

    return [task for task in tasks if matches(task)]


def filter_tasks_by_category(
    tasks: list[Task],
    category: Category | None,
) -> list[Task]:
    if category is None:
        return tasks

    def matches(task: Task) -> bool:
        if task.task_type is None:
            return False

        task_type = task.task_type.strip().lower()

        return TASK_TYPE_CATEGORIES.get(task_type) == category

    return [task for task in tasks if matches(task)]


def filter_tasks_by_status(tasks: list[Task]) -> list[Task]:
    return [task for task in tasks if task.status in {Status.todo, Status.doing}]


def filter_tasks_by_visible_months(tasks: list[Task]) -> list[Task]:
    current_month = get_current_month()
    next_month = get_next_month(current_month)

    return [
        task
        for task in tasks
        if (
            # include all past months from January up to current month,
            # plus the current month and the next month
            1 <= task.recommended_month <= current_month
            or task.recommended_month == next_month
        )
    ]
