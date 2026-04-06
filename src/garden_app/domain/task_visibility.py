from zoneinfo import ZoneInfo

from garden_app.domain.time import get_current_month, get_month_window
from garden_app.domain.types import Location
from garden_app.models.task import Task

APP_TIMEZONE = ZoneInfo("Europe/Amsterdam")

current = get_current_month()
prev, curr, next_ = get_month_window(current)


def filter_tasks_for_current_window(tasks: list[Task]) -> list[Task]:
    current_month = get_current_month()
    visible_months = get_month_window(current_month)

    return [task for task in tasks if task.recommended_month in visible_months]


HOME_TASK_TYPES = {"organization", "sowing at home"}


def filter_tasks_by_location(
    tasks: list[Task],
    location: Location | None,
) -> list[Task]:
    if location is None:
        return tasks

    def matches(task: Task) -> bool:
        if task.task_type is None:
            return True  # appears in both

        task_type = task.task_type.strip().lower()

        is_home = task_type in HOME_TASK_TYPES

        if location == Location.home:
            return is_home

        if location == Location.garden:
            return not is_home

        return True

    return [task for task in tasks if matches(task)]
